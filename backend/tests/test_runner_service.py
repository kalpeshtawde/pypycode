import docker

from app.services import runner


class DummyProblem:
    def __init__(self, test_cases):
        self.test_cases = test_cases


class DummySubmission:
    def __init__(self, output):
        self.output = output


def test_convert_test_cases_handles_input_and_kwargs():
    problem = DummyProblem(
        [
            {"function": "solution", "input": "1, 2", "expected": "3", "kwargs": {"x": 1}},
            {"args": [1, 2], "expected": 3},
        ]
    )
    converted = runner._convert_test_cases(problem)

    assert converted[0]["function"] == "solution"
    assert converted[0]["args"] == [1, 2]
    assert converted[0]["kwargs"] == {"x": 1}
    assert converted[1]["function"] == "solution"


def test_run_code_against_problem_accepts_all_passed(mocker):
    problem = DummyProblem([{"input": "1", "expected": "1"}])
    client = mocker.Mock()
    client.containers.run.return_value = '{"passed": 1, "total": 1, "output": "", "error": ""}'
    mocker.patch("docker.from_env", return_value=client)

    result = runner.run_code_against_problem(problem, "def solution(): return 1")
    assert result["status"] == "accepted"
    assert result["passed_tests"] == 1


def test_run_code_against_problem_handles_container_error(mocker):
    problem = DummyProblem([{"input": "1", "expected": "1"}])
    client = mocker.Mock()
    client.containers.run.side_effect = docker.errors.ContainerError(
        container=None,
        exit_status=1,
        command="python",
        image="img",
        stderr=b"boom",
    )
    mocker.patch("docker.from_env", return_value=client)

    result = runner.run_code_against_problem(problem, "def solution(): return 1")
    assert result["status"] == "runtime_error"


def test_run_code_against_problem_handles_timeout_like_error(mocker):
    class TimeoutException(Exception):
        pass

    problem = DummyProblem([{"input": "1", "expected": "1"}])
    client = mocker.Mock()
    client.containers.run.side_effect = TimeoutException("execution timeout")
    mocker.patch("docker.from_env", return_value=client)

    result = runner.run_code_against_problem(problem, "def solution(): return 1")
    assert result["status"] == "time_limit"
