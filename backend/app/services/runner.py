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
    # Filter only active test cases, ordered by serial_number
    active_test_cases = [tc for tc in problem.test_cases if tc.is_active]
    for tc in active_test_cases:
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
    logger.info(f"[BATCH] Sending {len(test_cases)} test cases to sandbox: {[tc.get('function', 'solution') for tc in test_cases]}")
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
        
        # The sandbox always ends with print(json.dumps(result)).
        # Any lines before the last are user print() output leaking to container stdout.
        lines = output_str.splitlines()
        json_line = lines[-1].strip()
        user_output = "\n".join(lines[:-1]).strip()

        try:
            result = json.loads(json_line)
            result["runtime_ms"] = int(elapsed_ms)
            # Merge any leaked stdout with buffer-captured output
            if user_output:
                existing = result.get("output") or ""
                result["output"] = (user_output + "\n" + existing).strip() if existing else user_output
            error_val = result.get('error')
            error_str = error_val[:100] if error_val else 'None'
            logger.info(f"[BATCH] Sandbox result: passed={result.get('passed')}, total={result.get('total')}, error={error_str}")
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
        import traceback
        logger.error(f"[BATCH] Exception in _run_tests_batch: {str(e)}")
        logger.error(f"[BATCH] Traceback: {traceback.format_exc()}")
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
        problem_slug = getattr(problem, 'slug', None) if problem else None
        logger.info(f"[RUNNER] Problem: {problem_slug or 'unknown'}, code length: {len(code) if code else 0}")
        test_cases = _convert_test_cases(problem)
        
        logger.info(f"[RUNNER] Total active test cases: {len(test_cases)}")
        if not test_cases:
            logger.error("[RUNNER] No test cases found - check is_active flags in database")

        if not test_cases:
            return {
                "status": "runtime_error",
                "passed_tests": 0,
                "total_tests": 0,
                "runtime_ms": None,
                "memory_kb": None,
                "error_output": "No test cases found",
            }

        # Run all test cases at once
        logger.info(f"[RUNNER] Running all {len(test_cases)} test cases")
        result = _run_tests_batch(client, code, test_cases)
        logger.info(f"[RUNNER] Result: passed={result.get('passed')}, total={result.get('total')}")

        passed = result.get("passed", 0)
        total = result.get("total", len(test_cases))
        error = result.get("error", "")

        # Build error output
        error_parts = []
        if result.get("test_outputs") is not None:
            error_parts.append(f"PerTestOutputs:\n{json.dumps(result.get('test_outputs'))}")
        if result.get("output"):
            error_parts.append(f"Output:\n{result.get('output')}")
        if error:
            error_parts.append(f"Errors:\n{error}")

        # Check for runtime errors
        if error and ("Container error" in error or "execution timeout" in error.lower()):
            status = "time_limit" if "timeout" in error.lower() else "runtime_error"
            return {
                "status": status,
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "runtime_ms": None,
                "memory_kb": None,
                "error_output": "\n".join(error_parts),
            }

        return {
            "status": "accepted" if passed == total else "wrong_answer",
            "passed_tests": passed,
            "total_tests": len(test_cases),
            "runtime_ms": result.get("runtime_ms"),
            "memory_kb": None,
            "error_output": "\n".join(error_parts) if error_parts else None,
        }
    except docker.errors.ContainerError as e:
        active_count = len([tc for tc in problem.test_cases if tc.is_active])
        return {
            "status": "runtime_error",
            "passed_tests": 0,
            "total_tests": active_count,
            "runtime_ms": None,
            "memory_kb": None,
            "error_output": str(e)[:2000],
        }
    except Exception as e:
        active_count = len([tc for tc in problem.test_cases if tc.is_active])
        status = "time_limit" if "Timeout" in type(e).__name__ or "timeout" in str(e).lower() else "runtime_error"
        return {
            "status": status,
            "passed_tests": 0,
            "total_tests": active_count,
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
