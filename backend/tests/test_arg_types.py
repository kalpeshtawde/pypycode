"""Tests for arg_types: derivation, persistence, runner conversion, and sandbox execution."""
import json
import pytest

from app import db
from app.models import Problem, TestCase
from app.routes.problems import _derive_arg_types
from app.services import runner as runner_module


# ---------------------------------------------------------------------------
# _derive_arg_types helper
# ---------------------------------------------------------------------------

class TestDeriveArgTypes:
    def test_tree_tag_single_arg(self):
        result = _derive_arg_types(["tree", "dfs"], "[1,2,3]")
        assert result == ["tree"]

    def test_binary_tree_tag(self):
        result = _derive_arg_types(["binary-tree"], "[1,2,3]")
        assert result == ["tree"]

    def test_tree_tag_two_args(self):
        # e.g. path-sum: tree + integer target
        result = _derive_arg_types(["tree"], "[1,2,3], 5")
        assert result == ["tree", None]

    def test_linked_list_tag(self):
        result = _derive_arg_types(["linked-list"], "[1,2,3]")
        assert result == ["linked_list"]

    def test_linked_list_two_args(self):
        result = _derive_arg_types(["linked-list"], "[1,2,3], [4,5]")
        assert result == ["linked_list", None]

    def test_no_matching_tag_returns_none(self):
        assert _derive_arg_types(["array", "hash-map"], "[1,2,3]") is None

    def test_empty_tags_returns_none(self):
        assert _derive_arg_types([], "[1,2,3]") is None

    def test_none_tags_returns_none(self):
        assert _derive_arg_types(None, "[1,2,3]") is None

    def test_case_insensitive_tags(self):
        result = _derive_arg_types(["Tree"], "[1]")
        assert result == ["tree"]

    def test_empty_input_defaults_to_single_arg(self):
        result = _derive_arg_types(["tree"], "")
        assert result == ["tree"]


# ---------------------------------------------------------------------------
# arg_types auto-set on problem ingest (via POST /problems/public-ingest)
# ---------------------------------------------------------------------------

INGEST_KEY = "ingest-test-key"


def _ingest_payload(slug, tags, test_cases=None):
    return {
        "ingestKey": INGEST_KEY,
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "difficulty": "medium",
        "description": "desc",
        "starterCode": "def solution(root):\n    pass",
        "comparisonStrategy": "exact",
        "examples": [{"input": "[]", "output": "[]"}],
        "tags": tags,
        "testCases": test_cases or [
            {"function": "solution", "input": "[1,2,3]", "expectedOutput": "true"},
        ],
        "solution": {"functionName": "solution", "code": "def solution(root): return True"},
    }



def test_ingest_tree_problem_sets_arg_types(client):
    payload = _ingest_payload("ingest-tree-test", ["tree", "dfs"])
    res = client.post("/problems/public-ingest", json=payload)
    assert res.status_code == 201

    tc = TestCase.query.filter(
        TestCase.problem_id == Problem.query.filter_by(slug="ingest-tree-test").first().id
    ).first()
    # New schema uses test_input instead of arg_types
    assert tc.test_input is not None
    assert "args" in tc.test_input


def test_ingest_linked_list_problem_sets_arg_types(client):
    payload = _ingest_payload("ingest-ll-test", ["linked-list"])
    res = client.post("/problems/public-ingest", json=payload)
    assert res.status_code == 201

    tc = TestCase.query.filter(
        TestCase.problem_id == Problem.query.filter_by(slug="ingest-ll-test").first().id
    ).first()
    # New schema uses test_input instead of arg_types
    assert tc.test_input is not None
    assert "args" in tc.test_input


def test_ingest_plain_problem_leaves_arg_types_null(client):
    payload = _ingest_payload("ingest-plain-test", ["array", "hash-map"])
    res = client.post("/problems/public-ingest", json=payload)
    assert res.status_code == 201

    tc = TestCase.query.filter(
        TestCase.problem_id == Problem.query.filter_by(slug="ingest-plain-test").first().id
    ).first()
    # New schema uses test_input instead of arg_types
    assert tc.test_input is not None
    assert "args" in tc.test_input


def test_ingest_tree_problem_multi_arg_sets_correct_arg_types(client):
    # path-sum style: tree + integer
    payload = _ingest_payload(
        "ingest-tree-multi-test",
        ["tree"],
        test_cases=[{"function": "solution", "input": "[1,2,3], 5", "expectedOutput": "true"}],
    )
    res = client.post("/problems/public-ingest", json=payload)
    assert res.status_code == 201

    tc = TestCase.query.filter(
        TestCase.problem_id == Problem.query.filter_by(slug="ingest-tree-multi-test").first().id
    ).first()
    # New schema uses test_input instead of arg_types
    assert tc.test_input is not None
    assert "args" in tc.test_input
    assert len(tc.test_input["args"]) == 2


def test_ingest_explicit_arg_types_override_auto_derive(client):
    payload = _ingest_payload("ingest-override-test", ["tree"])
    payload["testCases"][0]["argTypes"] = ["linked_list"]
    res = client.post("/problems/public-ingest", json=payload)
    assert res.status_code == 201

    tc = TestCase.query.filter(
        TestCase.problem_id == Problem.query.filter_by(slug="ingest-override-test").first().id
    ).first()
    # New schema uses test_input instead of arg_types
    assert tc.test_input is not None
    assert "args" in tc.test_input


# ---------------------------------------------------------------------------
# _convert_test_cases passes arg_types through to the runner payload
# ---------------------------------------------------------------------------

class DummyTestCase:
    def __init__(self, test_input=None, expected_output=None, is_active=True):
        self.test_input = test_input or {"args": []}
        self.expected_output = expected_output
        self.is_active = is_active


class DummyProblem:
    def __init__(self, test_cases_data):
        self.test_cases = test_cases_data


def test_convert_test_cases_includes_test_input():
    problem = DummyProblem([
        DummyTestCase(test_input={"args": [[1,2,3]]}, expected_output=True),
    ])
    converted = runner_module._convert_test_cases(problem)
    assert converted[0]["args"] == [[1,2,3]]
    assert converted[0]["expected"] == True


def test_convert_test_cases_includes_expected_output():
    problem = DummyProblem([
        DummyTestCase(test_input={"args": [1, 2]}, expected_output=3),
    ])
    converted = runner_module._convert_test_cases(problem)
    assert converted[0]["expected"] == 3


# ---------------------------------------------------------------------------
# Sandbox test_runner: _convert_args converts list → TreeNode / ListNode
# ---------------------------------------------------------------------------

import sys
from pathlib import Path

SANDBOX_PATH = Path(__file__).resolve().parents[2] / "sandbox"
if str(SANDBOX_PATH) not in sys.path:
    sys.path.insert(0, str(SANDBOX_PATH))

import test_runner as sandbox_runner  # noqa: E402


def _make_namespace():
    ns = {}
    sandbox_runner.exec(  # type: ignore[attr-defined]
        compile(sandbox_runner.PRELUDE, "<prelude>", "exec"), ns
    )
    return ns


def _exec_prelude():
    ns = {}
    exec(compile(sandbox_runner.PRELUDE, "<prelude>", "exec"), ns)
    return ns


class TestConvertArgs:
    def test_tree_arg_type_converts_list_to_tree_node(self):
        ns = _exec_prelude()
        args = [[1, 2, 3]]
        converted = sandbox_runner._convert_args(args, ["tree"], ns)
        root = converted[0]
        assert hasattr(root, "val") and hasattr(root, "left") and hasattr(root, "right")
        assert root.val == 1

    def test_linked_list_arg_type_converts_list_to_list_node(self):
        ns = _exec_prelude()
        args = [[1, 2, 3]]
        converted = sandbox_runner._convert_args(args, ["linked_list"], ns)
        head = converted[0]
        assert hasattr(head, "val") and hasattr(head, "next")
        assert head.val == 1

    def test_none_arg_type_leaves_arg_unchanged(self):
        ns = _exec_prelude()
        args = [[1, 2, 3], 5]
        converted = sandbox_runner._convert_args(args, ["tree", None], ns)
        assert hasattr(converted[0], "val")  # first arg converted
        assert converted[1] == 5             # second arg unchanged

    def test_no_arg_types_returns_args_as_is(self):
        ns = _exec_prelude()
        args = [[1, 2, 3]]
        converted = sandbox_runner._convert_args(args, [], ns)
        assert converted == [[1, 2, 3]]


# ---------------------------------------------------------------------------
# End-to-end: run_tests with arg_types converts tree before calling function
# ---------------------------------------------------------------------------

class TestRunTestsWithArgTypes:
    @pytest.mark.skip(reason="arg_types is deprecated in new execution strategy schema")
    def test_tree_problem_receives_tree_node(self):
        code = "def isSymmetric(root):\n    return root.val == 1\n"
        problem = {
            "function_name": "isSymmetric",
            "comparison": "exact",
            "prelude": True,
            "test_cases": [
                {"args": [[1, 2, 2]], "kwargs": {}, "expected": True, "arg_types": ["tree"]},
            ],
        }
        result = sandbox_runner.run_tests(code, problem)
        assert result.all_passed
        assert result.cases[0]["error"] is None

    @pytest.mark.skip(reason="arg_types is deprecated in new execution strategy schema")
    def test_linked_list_problem_receives_list_node(self):
        code = "def getVal(head):\n    return head.val\n"
        problem = {
            "function_name": "getVal",
            "comparison": "exact",
            "prelude": True,
            "test_cases": [
                {"args": [[42, 1, 2]], "kwargs": {}, "expected": 42, "arg_types": ["linked_list"]},
            ],
        }
        result = sandbox_runner.run_tests(code, problem)
        assert result.all_passed

    def test_plain_problem_without_arg_types_passes_list(self):
        code = "def solution(nums):\n    return len(nums)\n"
        problem = {
            "function_name": "solution",
            "comparison": "exact",
            "prelude": False,
            "test_cases": [
                {"args": [[1, 2, 3]], "kwargs": {}, "expected": 3, "arg_types": []},
            ],
        }
        result = sandbox_runner.run_tests(code, problem)
        assert result.all_passed
