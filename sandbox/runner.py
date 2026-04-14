import json
import os
import signal
import resource
from test_runner import run_tests

TIMEOUT = 4  # seconds


def limit_resources():
    # Max CPU time
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT, TIMEOUT))
    # Max memory: 200MB
    resource.setrlimit(resource.RLIMIT_AS, (200 * 1024 * 1024, 200 * 1024 * 1024))
    # Keep FD usage very low but non-zero so Python runtime/module imports can function.
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))


def run_payload(payload: dict) -> dict:
    code = payload.get("code", "")
    problem = payload.get("problem") or {}
    return run_tests(code, problem).to_dict()


def handler(signum, frame):
    raise TimeoutError("Time limit exceeded")


signal.signal(signal.SIGALRM, handler)
signal.alarm(TIMEOUT)

try:
    limit_resources()
    payload = json.loads(os.environ.get("PAYLOAD", "{}"))
    result = run_payload(payload)
except TimeoutError:
    result = {
        "all_passed": False,
        "passed": 0,
        "failed": 0,
        "total": 0,
        "compile_error": None,
        "runtime_error": "Time limit exceeded",
        "cases": [],
        "error": "Time limit exceeded",
    }
except Exception as e:
    result = {
        "all_passed": False,
        "passed": 0,
        "failed": 0,
        "total": 0,
        "compile_error": None,
        "runtime_error": str(e),
        "cases": [],
        "error": str(e),
    }

print(json.dumps(result))
