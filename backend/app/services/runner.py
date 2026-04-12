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
    # Test cases are now loaded from relationship, already ordered by serial_number
    for tc in problem.test_cases:
        expected = tc.expected_output
        if isinstance(expected, str):
            try:
                expected = json.loads(expected)
            except json.JSONDecodeError:
                pass  # Keep as string if not valid JSON
        converted_tc = {
            "function": tc.function or "solution",
            "expected": expected,
        }
        input_str = tc.input
        if input_str:
            try:
                args = json.loads("[" + input_str + "]")
                converted_tc["args"] = args
            except json.JSONDecodeError:
                converted_tc["args"] = [input_str]
        else:
            converted_tc["args"] = []

        converted_tc["kwargs"] = {}
        converted_test_cases.append(converted_tc)
    return converted_test_cases


def _run_tests_batch(client, code: str, test_cases: list) -> dict:
    """Run multiple test cases in sandbox."""
    payload = json.dumps({
        "code": code,
        "test_cases": test_cases,
    })

    start = time.monotonic()
    try:
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
        output_str = output_str.strip()
        
        if not output_str:
            return {
                "passed": 0,
                "total": len(test_cases),
                "error": "Sandbox produced no output (possible crash or timeout)",
                "output": "",
                "runtime_ms": int(elapsed_ms),
            }
        
        try:
            result = json.loads(output_str)
            result["runtime_ms"] = int(elapsed_ms)
            return result
        except json.JSONDecodeError as e:
            return {
                "passed": 0,
                "total": len(test_cases),
                "error": f"Invalid JSON output from sandbox: {e}",
                "output": output_str[:1000],
                "runtime_ms": int(elapsed_ms),
            }
    except docker.errors.ContainerError as e:
        return {
            "passed": 0,
            "total": len(test_cases),
            "error": f"Container error: {e.stderr.decode() if e.stderr else str(e)}",
            "output": "",
            "runtime_ms": None,
        }
    except Exception as e:
        elapsed_ms = (time.monotonic() - start) * 1000
        return {
            "passed": 0,
            "total": len(test_cases),
            "error": f"Execution error: {str(e)}",
            "output": "",
            "runtime_ms": int(elapsed_ms),
        }


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

        # Phase 1: Run first 3 tests
        first_batch_size = min(3, len(test_cases))
        first_batch = test_cases[:first_batch_size]
        first_result = _run_tests_batch(client, code, first_batch)

        first_passed = first_result.get("passed", 0)
        first_total = first_result.get("total", first_batch_size)
        first_error = first_result.get("error", "")

        # Build error output from first batch
        error_parts = []
        if first_result.get("output"):
            error_parts.append(f"Output:\n{first_result.get('output')}")
        if first_error:
            error_parts.append(f"Errors:\n{first_error}")

        # Check for runtime errors (container errors, execution errors)
        if first_error and ("Container error" in first_error or "execution timeout" in first_error.lower()):
            status = "time_limit" if "timeout" in first_error.lower() else "runtime_error"
            return {
                "status": status,
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "runtime_ms": None,
                "memory_kb": None,
                "error_output": "\n".join(error_parts),
            }

        # If any of first 3 failed, return early (showing results of first 3)
        if first_passed < first_total:
            return {
                "status": "wrong_answer",
                "passed_tests": first_passed,
                "total_tests": len(test_cases),
                "runtime_ms": first_result.get("runtime_ms"),
                "memory_kb": None,
                "error_output": "\n".join(error_parts) if error_parts else f"Failed {first_total - first_passed} of first {first_batch_size} tests",
            }

        # Phase 2: All first 3 passed - run remaining tests
        remaining_tests = test_cases[first_batch_size:]
        
        if not remaining_tests:
            # All tests were in first batch
            return {
                "status": "accepted",
                "passed_tests": first_passed,
                "total_tests": len(test_cases),
                "runtime_ms": first_result.get("runtime_ms"),
                "memory_kb": None,
                "error_output": "\n".join(error_parts) if error_parts else None,
            }

        # Run remaining tests
        remaining_result = _run_tests_batch(client, code, remaining_tests)
        
        # Combine results
        total_passed = first_passed + remaining_result.get("passed", 0)
        total_tests = len(test_cases)
        
        # Combine error outputs
        if remaining_result.get("output"):
            error_parts.append(f"Output:\n{remaining_result.get('output')}")
        if remaining_result.get("error"):
            error_parts.append(f"Errors:\n{remaining_result.get('error')}")

        return {
            "status": "accepted" if total_passed == total_tests else "wrong_answer",
            "passed_tests": total_passed,
            "total_tests": total_tests,
            "runtime_ms": first_result.get("runtime_ms", 0) + remaining_result.get("runtime_ms", 0),
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
