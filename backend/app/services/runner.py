import time
import os
import json
import docker
from app import celery_app, db
from app.models import Submission, Problem

SANDBOX_IMAGE = os.environ.get("SANDBOX_IMAGE", "pypycode-sandbox:latest")
TIMEOUT_SECONDS = 5
MEMORY_LIMIT = "256m"
CPU_QUOTA = 50000  # 0.5 CPU


@celery_app.task(bind=True, max_retries=2)
def run_submission(self, submission_id: int):
    sub = Submission.query.get(submission_id)
    if not sub:
        return
    problem = Problem.query.get(sub.problem_id)

    sub.status = "running"
    db.session.commit()

    try:
        client = docker.from_env()
        payload = json.dumps({
            "code": sub.code,
            "test_cases": problem.test_cases,
        })

        start = time.monotonic()
        container = client.containers.run(
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
            timeout=TIMEOUT_SECONDS + 2,
        )
        elapsed_ms = (time.monotonic() - start) * 1000

        result = json.loads(container.decode())
        sub.passed_tests = result.get("passed", 0)
        sub.total_tests = result.get("total", sub.total_tests)
        sub.runtime_ms = elapsed_ms
        sub.error_output = result.get("error")
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
