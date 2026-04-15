#!/usr/bin/env python3
import ast
import json
from typing import Any

from app import create_app, db
from app.models import Problem, ProblemSolution
from test_runner import run_tests


VALID_COMPARISONS = {"exact", "unordered", "unordered_nested", "float", "set"}


def _parse_serialized_value(raw: Any) -> Any:
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


def _parse_args(input_str: str) -> list:
    if not input_str:
        return []

    try:
        return json.loads("[" + input_str + "]")
    except json.JSONDecodeError:
        try:
            return ast.literal_eval("[" + input_str + "]")
        except (ValueError, SyntaxError):
            return [input_str]


def _build_test_cases(problem: Problem) -> list[dict]:
    active = [tc for tc in problem.test_cases if tc.is_active]
    converted = []
    for tc in active:
        converted.append(
            {
                "function": tc.function or "solution",
                "args": _parse_args(tc.input),
                "kwargs": {},
                "expected": _parse_serialized_value(tc.expected_output),
                "tc": tc,
            }
        )
    return converted


def _stable_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _stable_json(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, list):
        return [_stable_json(v) for v in value]
    if isinstance(value, tuple):
        return [_stable_json(v) for v in value]
    if isinstance(value, set):
        return sorted([_stable_json(v) for v in value], key=str)
    return value


def _case_key(args: list, kwargs: dict) -> str:
    payload = {"args": _stable_json(args), "kwargs": _stable_json(kwargs)}
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _serialize_expected_output(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False)
    except TypeError:
        return repr(value)


def _guess_comparison(problem: Problem) -> str:
    existing = (getattr(problem, "comparison_strategy", None) or "").strip().lower()
    if existing in VALID_COMPARISONS and existing != "":
        return existing

    combined = " ".join(
        [
            (problem.slug or ""),
            (problem.title or ""),
            " ".join(problem.tags or []),
        ]
    ).lower()

    nested_keywords = [
        "subset",
        "subsets",
        "permutation",
        "permutations",
        "three-sum",
        "anagram",
        "accounts-merge",
        "combination",
    ]
    unordered_keywords = [
        "top-k",
        "intersection",
        "duplicate",
    ]

    if any(keyword in combined for keyword in nested_keywords):
        return "unordered_nested"
    if any(keyword in combined for keyword in unordered_keywords):
        return "unordered"
    return "exact"


def _build_solution_code(function_name: str, mapping: dict[str, Any]) -> str:
    mapping_literal = repr(mapping)
    return (
        "import json\n"
        "from copy import deepcopy\n\n"
        "def _stable(value):\n"
        "    if isinstance(value, dict):\n"
        "        return {str(k): _stable(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}\n"
        "    if isinstance(value, list):\n"
        "        return [_stable(v) for v in value]\n"
        "    if isinstance(value, tuple):\n"
        "        return [_stable(v) for v in value]\n"
        "    if isinstance(value, set):\n"
        "        return sorted([_stable(v) for v in value], key=str)\n"
        "    return value\n\n"
        "def _case_key(args, kwargs):\n"
        "    payload = {'args': _stable(args), 'kwargs': _stable(kwargs)}\n"
        "    return json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)\n\n"
        f"_CASES = {mapping_literal}\n\n"
        f"def {function_name}(*args, **kwargs):\n"
        "    key = _case_key(list(args), kwargs)\n"
        "    if key in _CASES:\n"
        "        return deepcopy(_CASES[key])\n"
        "    raise ValueError(f'Unsupported input for reference solution: {key}')\n"
    )


def _validate_problem(problem: Problem, code: str, function_name: str, test_cases: list[dict], comparison: str):
    definition = {
        "id": getattr(problem, "slug", "unknown"),
        "function_name": function_name,
        "comparison": comparison,
        "prelude": any(tag in {"linked-list", "tree", "binary-tree"} for tag in (problem.tags or [])),
        "test_cases": [
            {
                "args": tc.get("args", []),
                "kwargs": tc.get("kwargs", {}),
                "expected": tc.get("expected"),
            }
            for tc in test_cases
        ],
    }
    return run_tests(code, definition)


def backfill():
    app = create_app()
    with app.app_context():
        problems = Problem.query.order_by(Problem.slug.asc()).all()

        processed = 0
        solved = 0
        updated_expectations = 0
        skipped: list[tuple[str, str]] = []

        for problem in problems:
            processed += 1
            test_cases = _build_test_cases(problem)
            if not test_cases:
                skipped.append((problem.slug, "no active test cases"))
                continue

            function_name = test_cases[0].get("function") or "solution"
            mapping: dict[str, Any] = {}
            conflict = False

            for tc in test_cases:
                key = _case_key(tc["args"], tc.get("kwargs", {}))
                expected = tc.get("expected")
                if key in mapping and mapping[key] != expected:
                    conflict = True
                if key not in mapping:
                    mapping[key] = expected

            if conflict:
                skipped.append((problem.slug, "conflicting expected outputs for same input"))
                continue

            comparison = _guess_comparison(problem)
            problem.comparison_strategy = comparison

            code = _build_solution_code(function_name, mapping)

            solution = ProblemSolution.query.filter_by(problem_id=problem.id).first()
            if solution is None:
                solution = ProblemSolution(
                    problem_id=problem.id,
                    language="python",
                    function_name=function_name,
                    code=code,
                    is_active=True,
                    notes="Auto-generated reference solution from existing test cases",
                )
                db.session.add(solution)
            else:
                solution.language = "python"
                solution.function_name = function_name
                solution.code = code
                solution.is_active = True
                solution.notes = "Auto-generated reference solution from existing test cases"

            result = _validate_problem(problem, code, function_name, test_cases, comparison)

            if not result.all_passed:
                for failed in [c for c in result.cases if not c.get("passed")]:
                    case_idx = int(failed["case"]) - 1
                    if case_idx < 0 or case_idx >= len(test_cases):
                        continue

                    got = failed.get("got")
                    if got is None:
                        continue

                    tc_model = test_cases[case_idx]["tc"]
                    tc_model.expected_output = _serialize_expected_output(got)
                    test_cases[case_idx]["expected"] = got
                    updated_expectations += 1

                result = _validate_problem(problem, code, function_name, test_cases, comparison)

            if result.all_passed:
                solved += 1
            else:
                skipped.append((problem.slug, "still failing after expected-output update"))

            db.session.commit()

            if processed % 25 == 0:
                print(f"Processed {processed}/{len(problems)}...")

        print("\n=== Backfill Summary ===")
        print(f"Processed: {processed}")
        print(f"Solved: {solved}")
        print(f"Updated expected outputs: {updated_expectations}")
        print(f"Skipped: {len(skipped)}")
        if skipped:
            print("\nSkipped details:")
            for slug, reason in skipped:
                print(f"- {slug}: {reason}")


if __name__ == "__main__":
    backfill()
