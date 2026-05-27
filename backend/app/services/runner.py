import time
import os
import json
import docker
import logging
from app import celery_app, db
from app.models import Submission, Problem

logger = logging.getLogger(__name__)

SANDBOX_IMAGE = os.environ.get("SANDBOX_IMAGE", "pypycode-sandbox:latest")
MEMORY_LIMIT = "256m"
CPU_QUOTA = 50000  # 0.5 CPU


def _parse_serialized_value(raw):
    if not isinstance(raw, str):
        return raw

    text = raw.strip()
    if text == "":
        return raw

    try:
        return json.loads(text)
    except (TypeError, json.JSONDecodeError):
        pass

    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return raw


def _convert_test_cases(problem: Problem):
    converted_test_cases = []
    active_test_cases = [tc for tc in problem.test_cases if tc.is_active]
    for tc in active_test_cases:
        test_case = dict(tc.test_input)
        test_case["expected"] = tc.expected_output
        converted_test_cases.append(test_case)
    return converted_test_cases

def _run_tests_in_sandbox(client, code: str, problem_definition: dict) -> dict:
    payload = json.dumps({
        "code": code,
        "problem": problem_definition,
    })

    start = time.monotonic()
    try:
        output = client.containers.run(
            SANDBOX_IMAGE,
            command=["python", "/runner/runner.py"],
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
        elapsed_ms = int((time.monotonic() - start) * 1000)
        output_str = output.decode() if isinstance(output, bytes) else output
        output_str = output_str.strip()

        if not output_str:
            return {
                "error": "Sandbox produced no output (possible crash or timeout)",
                "runtime_ms": elapsed_ms,
            }

        lines = output_str.splitlines()
        json_line = lines[-1].strip()

        try:
            result = json.loads(json_line)
            result["runtime_ms"] = elapsed_ms
            return result
        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON output from sandbox: {e}",
                "output": output_str[:1000],
                "runtime_ms": elapsed_ms,
            }
    except docker.errors.ContainerError as e:
        return {
            "error": f"Container error: {e.stderr.decode() if e.stderr else str(e)}",
            "runtime_ms": None,
        }
    except Exception as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return {
            "error": f"Execution error: {str(e)}",
            "runtime_ms": elapsed_ms,
        }


def _build_problem_definition(problem: Problem, test_cases: list[dict]) -> dict:
    tags = [str(tag).lower() for tag in (getattr(problem, "tags", []) or [])]
    prelude = any(tag in {"linked-list", "tree", "binary-tree"} for tag in tags)
    
    # Enable prelude if test cases explicitly use linked_list or tree types
    has_type_in_test_cases = False
    for tc in test_cases:
        arg_types = tc.get("arg_types", [])
        if arg_types and any(atype in {"linked_list", "tree"} for atype in arg_types):
            has_type_in_test_cases = True
            break
    prelude = prelude or has_type_in_test_cases
    
    return {
        "id": getattr(problem, "slug", "unknown"),
        "execution_model": getattr(problem, "execution_model", "function"),
        "function_name": getattr(problem, "function_name", "solution"),
        "class_name": getattr(problem, "class_name", None),
        "method_name": getattr(problem, "method_name", None),
        "comparison": getattr(problem, "comparison_strategy", "exact") or "exact",
        "prelude": prelude,
        "test_cases": test_cases,
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

        problem_definition = _build_problem_definition(problem, test_cases)
        sandbox_result = _run_tests_in_sandbox(client, code, problem_definition)

        if sandbox_result.get("error"):
            normalized_error = str(sandbox_result.get("error", "")).lower()
            if "timeout" in normalized_error or "time limit exceeded" in normalized_error:
                status = "time_limit"
            else:
                status = "runtime_error"
            return {
                "status": status,
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "runtime_ms": sandbox_result.get("runtime_ms"),
                "memory_kb": None,
                "error_output": str(sandbox_result.get("error"))[:2000],
            }

        error_parts = []
        compile_error = sandbox_result.get("compile_error")
        runtime_error = sandbox_result.get("runtime_error")
        if compile_error:
            error_parts.append(compile_error)
        if runtime_error:
            error_parts.append(runtime_error)

        cases = sandbox_result.get("cases", [])
        if cases:
            error_parts.append(f"FailedCases:\n{json.dumps(cases)}")

        # Per-test stdout (printed output from user code), one entry per case in order.
        per_test_outputs = [c.get("stdout", "") or "" for c in cases]
        if any(out for out in per_test_outputs):
            error_parts.append(f"PerTestOutputs:\n{json.dumps(per_test_outputs)}")

        if compile_error or runtime_error:
            re_lower = (runtime_error or "").lower()
            if "time limit" in re_lower or "timeout" in re_lower:
                status = "time_limit"
            else:
                status = "runtime_error"
        else:
            all_passed = sandbox_result.get("all_passed")
            if all_passed is None:
                all_passed = sandbox_result.get("passed", 0) == sandbox_result.get("total", len(test_cases))
            status = "accepted" if all_passed else "wrong_answer"

        return {
            "status": status,
            "passed_tests": sandbox_result.get("passed", 0),
            "total_tests": sandbox_result.get("total", len(test_cases)),
            "runtime_ms": sandbox_result.get("runtime_ms"),
            "memory_kb": None,
            "error_output": "\n".join(error_parts) if error_parts else None,
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
