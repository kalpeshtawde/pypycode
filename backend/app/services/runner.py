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

        try:
            client = docker.from_env()
            
            # Convert test cases from string format to args format
            converted_test_cases = []
            for tc in problem.test_cases:
                converted_tc = {
                    "function": tc.get("function", "solution"),
                    "expected": json.loads(tc["expected"]) if isinstance(tc["expected"], str) else tc["expected"]
                }
                # Parse input string as args list
                if "input" in tc:
                    input_str = tc["input"]
                    # Parse as Python literal - handles lists, strings, numbers, etc.
                    try:
                        # Try to parse as a tuple of arguments
                        # Input format: "[2, 7, 11, 15], 9" -> args: [[2, 7, 11, 15], 9]
                        args = json.loads("[" + input_str + "]")
                        converted_tc["args"] = args
                    except json.JSONDecodeError:
                        # Fallback: treat as single argument
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
            
            payload = json.dumps({
                "code": sub.code,
                "test_cases": converted_test_cases,
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
            sub.passed_tests = result.get("passed", 0)
            sub.total_tests = result.get("total", sub.total_tests)
            sub.runtime_ms = int(elapsed_ms)
            
            # Combine error output and print statements for debugging
            error_parts = []
            if result.get("output"):
                error_parts.append(f"Output:\n{result.get('output')}")
            if result.get("error"):
                error_parts.append(f"Errors:\n{result.get('error')}")
            
            sub.error_output = "\n".join(error_parts) if error_parts else None
            sub.status = "accepted" if result.get("passed") == result.get("total") else "wrong_answer"

        except docker.errors.ContainerError as e:
            sub.status = "runtime_error"
            sub.error_output = str(e)[:2000]
        except Exception as e:
            if "Timeout" in type(e).__name__ or "timeout" in str(e).lower():
                sub.status = "time_limit"
            else:
                sub.status = "runtime_error"
                sub.error_output = str(e)[:2000]

        db.session.commit()
