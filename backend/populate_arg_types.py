#!/usr/bin/env python3
"""Populate arg_types on test cases for tree and linked-list problems.

Rules:
- tags contain 'tree' or 'binary-tree'  → first arg is "tree"
- tags contain 'linked-list'            → first arg is "linked_list"
- If a test case has multiple args the first is typed, the rest are left None.
"""
import ast
import json
from app import create_app, db
from app.models import Problem, TestCase


def _arg_count(input_str: str) -> int:
    if not input_str:
        return 0
    try:
        return len(json.loads("[" + input_str + "]"))
    except Exception:
        try:
            return len(ast.literal_eval("[" + input_str + "]"))
        except Exception:
            return 1


def main():
    app = create_app()
    with app.app_context():
        updated = 0
        skipped = 0

        problems = Problem.query.all()
        for problem in problems:
            tags = [t.lower() for t in (problem.tags or [])]
            if any(t in {"tree", "binary-tree"} for t in tags):
                first_type = "tree"
            elif "linked-list" in tags:
                first_type = "linked_list"
            else:
                skipped += 1
                continue

            for tc in problem.test_cases:
                n = _arg_count(tc.input)
                arg_types = [first_type] + [None] * max(0, n - 1)
                tc.arg_types = arg_types
                updated += 1

        db.session.commit()
        print(f"Updated {updated} test cases across tree/linked-list problems")
        print(f"Skipped {skipped} problems (no tree/linked-list tag)")


if __name__ == "__main__":
    main()
