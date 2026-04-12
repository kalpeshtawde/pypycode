import docker

from app.services import runner


class DummyTestCase:
    def __init__(self, function="solution", input_str="", expected_output="", is_active=True):
        self.function = function
        self.input = input_str
        self.expected_output = expected_output
        self.is_active = is_active


class DummyProblem:
    def __init__(self, test_cases_data):
        # Convert dict test cases to DummyTestCase objects
        self.test_cases = []
        for tc in test_cases_data:
            self.test_cases.append(DummyTestCase(
                function=tc.get("function", "solution"),
                input_str=tc.get("input", ""),
                expected_output=tc.get("expectedOutput", tc.get("expected", "")),
                is_active=tc.get("isActive", True),
            ))


class DummySubmission:
    def __init__(self, output):
        self.output = output


def test_convert_test_cases_handles_input():
    problem = DummyProblem(
        [
            {"function": "solution", "input": "1, 2", "expectedOutput": "3"},
            {"input": "[1, 2]", "expectedOutput": "[1, 2]"},
        ]
    )
    converted = runner._convert_test_cases(problem)

    assert converted[0]["function"] == "solution"
    assert converted[0]["args"] == [1, 2]
    assert converted[1]["function"] == "solution"


def test_run_code_against_problem_accepts_all_passed(mocker):
    problem = DummyProblem([{"input": "1", "expectedOutput": "1"}])
    client = mocker.Mock()
    client.containers.run.return_value = '{"passed": 1, "total": 1, "output": "", "error": ""}'
    mocker.patch("docker.from_env", return_value=client)

    result = runner.run_code_against_problem(problem, "def solution(): return 1")
    assert result["status"] == "accepted"
    assert result["passed_tests"] == 1


def test_run_code_against_problem_handles_container_error(mocker):
    problem = DummyProblem([{"input": "1", "expectedOutput": "1"}])
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

    problem = DummyProblem([{"input": "1", "expectedOutput": "1"}])
    client = mocker.Mock()
    client.containers.run.side_effect = TimeoutException("execution timeout")
    mocker.patch("docker.from_env", return_value=client)

    result = runner.run_code_against_problem(problem, "def solution(): return 1")
    assert result["status"] == "time_limit"
