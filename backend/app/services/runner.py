import time
import os
import json
import docker
import logging
from app import celery_app, db
from app.models import Submission, Problem

logger = logging.getLogger(__name__)

SANDBOX_IMAGE = os.environ.get("SANDBOX_IMAGE", "pypycode-sandbox:latest")
TIMEOUT_SECONDS = 5
MEMORY_LIMIT = "256m"
CPU_QUOTA = 50000  # 0.5 CPU


def _convert_test_cases(problem: Problem):
    converted_test_cases = []
    for tc in problem.test_cases:
        expected = tc.get("expected")
        if isinstance(expected, str):
            try:
                expected = json.loads(expected)
            except json.JSONDecodeError:
                pass  # Keep as string if not valid JSON
        converted_tc = {
            "function": tc.get("function", "solution"),
            "expected": expected,
        }
        if "input" in tc:
            input_str = tc["input"]
            try:
                args = json.loads("[" + input_str + "]")
                converted_tc["args"] = args
            except json.JSONDecodeError:
                converted_tc["args"] = [input_str]
        elif "args" in tc:
            converted_tc["args"] = tc["args"]
        else:
            converted_tc["args"] = []

        if "kwargs" in tc:
            converted_tc["kwargs"] = tc["kwargs"]
        else:
            converted_tc["kwargs"] = {}

        converted_test_cases.append(converted_tc)
    return converted_test_cases


def _run_single_test(client, code: str, test_case: dict) -> dict:
    """Run a single test case in sandbox."""
    payload = json.dumps({
        "code": code,
        "test_cases": [test_case],
    })

    start = time.monotonic()
    output = client.containers.run(
        SANDBOX_IMAGE,
        command=["python", "/runner/runner.py"],
        stdin_open=True,
        environment={"PAYLOAD": payload},
        network_disabled=True,
        mem_limit=MEMORY_LIMIT,
        cpu_quota=CPU_QUOTA,
        cpu_period=100000,
        read_only=True,
        remove=True,
        detach=False,
        stdout=True,
        stderr=True,
    )
    elapsed_ms = (time.monotonic() - start) * 1000

    output_str = output.decode() if isinstance(output, bytes) else output
    result = json.loads(output_str)
    result["runtime_ms"] = int(elapsed_ms)
    return result


def run_code_against_problem(problem: Problem, code: str):
    try:
        client = docker.from_env()
        test_cases = _convert_test_cases(problem)

        if not test_cases:
            return {
                "status": "runtime_error",
                "passed_tests": 0,
                "total_tests": 0,
                "runtime_ms": None,
                "memory_kb": None,
                "error_output": "No test cases found",
            }

        # Phase 1: Run first test only
        first_test_result = _run_single_test(client, code, test_cases[0])

        # Check if first test passed
        first_passed = first_test_result.get("passed", 0) == 1

        if not first_passed:
            # First test failed - return early with failure
            error_parts = []
            if first_test_result.get("output"):
                error_parts.append(f"Output:\n{first_test_result.get('output')}")
            if first_test_result.get("error"):
                error_parts.append(f"Errors:\n{first_test_result.get('error')}")

            return {
                "status": "wrong_answer",
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "runtime_ms": first_test_result.get("runtime_ms"),
                "memory_kb": None,
                "error_output": "\n".join(error_parts) if error_parts else "First test case failed",
            }

        # Phase 2: First test passed - run full suite
        all_test_cases = test_cases
        payload = json.dumps({
            "code": code,
            "test_cases": all_test_cases,
        })

        start = time.monotonic()
        output = client.containers.run(
            SANDBOX_IMAGE,
            command=["python", "/runner/runner.py"],
            stdin_open=True,
            environment={"PAYLOAD": payload},
            network_disabled=True,
            mem_limit=MEMORY_LIMIT,
            cpu_quota=CPU_QUOTA,
            cpu_period=100000,
            read_only=True,
            remove=True,
            detach=False,
            stdout=True,
            stderr=True,
        )
        elapsed_ms = (time.monotonic() - start) * 1000

        output_str = output.decode() if isinstance(output, bytes) else output
        result = json.loads(output_str)

        error_parts = []
        if result.get("output"):
            error_parts.append(f"Output:\n{result.get('output')}")
        if result.get("error"):
            error_parts.append(f"Errors:\n{result.get('error')}")

        passed_tests = result.get("passed", 0)
        total_tests = result.get("total", len(all_test_cases))
        return {
            "status": "accepted" if passed_tests == total_tests else "wrong_answer",
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "runtime_ms": int(elapsed_ms),
            "memory_kb": None,
            "error_output": "\n".join(error_parts) if error_parts else None,
        }
    except docker.errors.ContainerError as e:
        return {
            "status": "runtime_error",
            "passed_tests": 0,
            "total_tests": len(problem.test_cases),
            "runtime_ms": None,
            "memory_kb": None,
            "error_output": str(e)[:2000],
        }
    except Exception as e:
        status = "time_limit" if "Timeout" in type(e).__name__ or "timeout" in str(e).lower() else "runtime_error"
        return {
            "status": status,
            "passed_tests": 0,
            "total_tests": len(problem.test_cases),
            "runtime_ms": None,
            "memory_kb": None,
            "error_output": str(e)[:2000] if status == "runtime_error" else None,
        }


@celery_app.task(bind=True, max_retries=1)
def run_code_for_problem(self, problem_id: str, code: str):
    from app import create_app
    app = create_app()
    with app.app_context():
        problem = Problem.query.get(problem_id)
        if not problem:
            return {
                "status": "runtime_error",
                "passed_tests": 0,
                "total_tests": 0,
                "runtime_ms": None,
                "memory_kb": None,
                "error_output": "Problem not found",
            }
        return run_code_against_problem(problem, code)


@celery_app.task(bind=True, max_retries=2)
def run_submission(self, submission_id: str):
    from app import create_app
    app = create_app()
    with app.app_context():
        sub = Submission.query.get(submission_id)
        if not sub:
            return
        problem = Problem.query.get(sub.problem_id)

        sub.status = "running"
        db.session.commit()

        run_result = run_code_against_problem(problem, sub.code)
        sub.status = run_result["status"]
        sub.passed_tests = run_result["passed_tests"]
        sub.total_tests = run_result["total_tests"]
        sub.runtime_ms = run_result["runtime_ms"]
        sub.memory_kb = run_result["memory_kb"]
        sub.error_output = run_result["error_output"]

        db.session.commit()
