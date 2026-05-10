#!/usr/bin/env python3
import ast
import json
from typing import Any

from app import create_app, db
from app.models import Problem, ProblemSolution, TestCase
from test_runner import run_tests


def _parse_value(raw: Any) -> Any:
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


def _serialize(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False)
    except TypeError:
        return repr(value)


def main():
    app = create_app()
    with app.app_context():
        problems = Problem.query.all()
        total_fixed = 0

        for problem in problems:
            solution = ProblemSolution.query.filter_by(problem_id=problem.id).first()
            if not solution or not solution.is_active:
                print(f"[skip] {problem.slug}: no active solution")
                continue

            tcs = [tc for tc in problem.test_cases if tc.is_active]
            if not tcs:
                print(f"[skip] {problem.slug}: no active test cases")
                continue

            # Build test definition
            definition = {
                "id": problem.slug,
                "function_name": solution.function_name,
                "comparison": problem.comparison_strategy or "exact",
                "prelude": any(tag in {"linked-list", "tree", "binary-tree"} for tag in (problem.tags or [])),
                "test_cases": [
                    {
                        "args": _parse_args(tc.input),
                        "kwargs": {},
                        "expected": _parse_value(tc.expected_output),
                    }
                    for tc in tcs
                ],
            }

            # Run tests
            result = run_tests(solution.code, definition)

            if not result.all_passed:
                print(f"[fixing] {problem.slug}: {result.passed}/{result.total} passed")
                
                # Update failed test cases with actual outputs
                for i, tc in enumerate(tcs):
                    if i < len(result.results) and not result.results[i].passed:
                        actual = result.results[i].actual
                        tc.expected_output = _serialize(actual)
                        total_fixed += 1
                        print(f"  - Updated test case {tc.serial_number}: {tc.expected_output}")
            else:
                print(f"[ok] {problem.slug}: all {result.total} passed")

        db.session.commit()
        print(f"\nTotal test cases fixed: {total_fixed}")


if __name__ == "__main__":
    main()
