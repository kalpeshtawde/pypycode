import json
import os
import sys
import signal
import traceback
import resource
from io import StringIO

TIMEOUT = 4  # seconds


def limit_resources():
    # Max CPU time
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT, TIMEOUT))
    # Max memory: 200MB
    resource.setrlimit(resource.RLIMIT_AS, (200 * 1024 * 1024, 200 * 1024 * 1024))
    # No new files
    resource.setrlimit(resource.RLIMIT_NOFILE, (0, 0))


def run_tests(code: str, test_cases: list) -> dict:
    namespace = {}
    output_buffer = StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_buffer
    
    try:
        exec(compile(code, "<submission>", "exec"), namespace)
    except Exception as e:
        sys.stdout = old_stdout
        return {
            "passed": 0,
            "total": len(test_cases),
            "error": f"Compilation error: {e}",
            "output": output_buffer.getvalue()
        }

    passed = 0
    errors = []
    test_outputs = []

    for i, tc in enumerate(test_cases):
        start_pos = output_buffer.tell()
        try:
            fn_name = tc.get("function", "solution")
            fn = namespace.get(fn_name)
            if fn is None:
                errors.append(f"Test {i+1}: function '{fn_name}' not found")
                current_output = output_buffer.getvalue()[start_pos:].strip()
                test_outputs.append(current_output)
                continue
            args = tc.get("args", [])
            kwargs = tc.get("kwargs", {})
            expected = tc["expected"]
            result = fn(*args, **kwargs)
            if result == expected:
                passed += 1
            else:
                errors.append(f"Test {i+1}: expected {expected!r}, got {result!r}")
        except Exception as e:
            exc_str = traceback.format_exc(limit=3)
            errors.append(f"Test {i+1}: {exc_str}")

        current_output = output_buffer.getvalue()[start_pos:].strip()
        test_outputs.append(current_output)

    sys.stdout = old_stdout
    
    return {
        "passed": passed,
        "total": len(test_cases),
        "error": "\n".join(errors) if errors else None,
        "output": output_buffer.getvalue(),
        "test_outputs": test_outputs,
    }


def handler(signum, frame):
    raise TimeoutError("Time limit exceeded")


signal.signal(signal.SIGALRM, handler)
signal.alarm(TIMEOUT)

try:
    limit_resources()
    payload = json.loads(os.environ.get("PAYLOAD", "{}"))
    result = run_tests(payload.get("code", ""), payload.get("test_cases", []))
except TimeoutError:
    result = {"passed": 0, "total": 0, "error": "Time limit exceeded"}
except Exception as e:
    result = {"passed": 0, "total": 0, "error": str(e)}

print(json.dumps(result))
