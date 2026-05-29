#!/usr/bin/env python3
import sys
import os
import random
import string
from copy import deepcopy
from typing import Any

from app import create_app, db
from app.models import Problem, TestCase, ProblemSolution


def generate_new_input_arg(existing_values: list[Any]) -> Any:
    """
    Generates a new, realistic input argument based on a list of existing values
    for the same argument position across other test cases of the same problem.
    """
    if not existing_values:
        return None

    # Find the first non-None value to detect the expected type
    sample = next((x for x in existing_values if x is not None), None)
    if sample is None:
        return None

    if isinstance(sample, bool):
        return random.choice([True, False])

    elif isinstance(sample, int):
        ints = [x for x in existing_values if isinstance(x, int)]
        if not ints:
            return random.randint(1, 100)
        min_v, max_v = min(ints), max(ints)
        if random.random() < 0.5:
            base = random.choice(ints)
            # Add a small perturbation
            return base + random.choice([-3, -2, -1, 1, 2, 3, 5, 10])
        else:
            return random.randint(min_v - 2, max_v + 5)

    elif isinstance(sample, float):
        floats = [x for x in existing_values if isinstance(x, (int, float))]
        if not floats:
            return random.uniform(1.0, 100.0)
        min_v, max_v = min(floats), max(floats)
        return random.uniform(min_v - 1.0, max_v + 2.0)

    elif isinstance(sample, str):
        strs = [x for x in existing_values if isinstance(x, str)]
        if not strs:
            return "".join(random.choices(string.ascii_lowercase, k=5))
        base = random.choice(strs)
        if len(base) == 0:
            return "".join(random.choices(string.ascii_lowercase, k=5))

        strategy = random.choice(["reverse", "repeat", "shuffle", "case", "random_similar"])
        if strategy == "reverse":
            return base[::-1]
        elif strategy == "repeat":
            return base * 2
        elif strategy == "shuffle":
            chars = list(base)
            random.shuffle(chars)
            return "".join(chars)
        elif strategy == "case":
            return base.swapcase()
        else:
            # Generate random string using the same set of characters (alphabet)
            alphabet = "".join(set("".join(strs)))
            if not alphabet:
                alphabet = string.ascii_lowercase
            length = random.randint(max(1, len(base) - 2), len(base) + 3)
            return "".join(random.choices(alphabet, k=length))

    elif isinstance(sample, list):
        lists = [x for x in existing_values if isinstance(x, list)]
        if not lists:
            return []

        all_elements = []
        for lst in lists:
            all_elements.extend(lst)

        lens = [len(lst) for lst in lists]
        min_len = min(lens) if lens else 0
        max_len = max(lens) if lens else 10
        new_len = random.randint(min_len, max_len + 1)

        if all_elements:
            new_list = [generate_new_input_arg(all_elements) for _ in range(new_len)]
            is_sorted = False
            try:
                is_sorted = any(lst == sorted(lst) for lst in lists if len(lst) > 1)
            except TypeError:
                pass
            if is_sorted and random.random() < 0.8:
                try:
                    new_list.sort()
                except TypeError:
                    pass
            return new_list
        else:
            return []

    elif isinstance(sample, dict):
        dicts = [x for x in existing_values if isinstance(x, dict)]
        if not dicts:
            return {}
        base = deepcopy(random.choice(dicts))
        for k, v in base.items():
            all_vals_for_key = [d[k] for d in dicts if k in d]
            if all_vals_for_key:
                base[k] = generate_new_input_arg(all_vals_for_key)
        return base

    return sample


def is_json_serializable(value: Any) -> bool:
    """Checks if a given value is JSON-serializable."""
    try:
        import json
        json.dumps(value)
        return True
    except (TypeError, OverflowError):
        return False


def add_missing_test_cases(target_minimum_tests: int = 5):
    """
    Scans the database for problems with fewer than target_minimum_tests active test cases.
    For each problem, generates realistic test inputs based on existing test inputs,
    computes the correct expected outputs by executing the verified reference solution,
    and saves the new test cases to the database.
    """
    app = create_app()
    with app.app_context():
        problems = Problem.query.all()
        print(f"Total problems in database: {len(problems)}")

        updated_problems_count = 0
        total_test_cases_added = 0

        for problem in problems:
            active_tcs = [tc for tc in problem.test_cases if tc.is_active]
            num_active = len(active_tcs)

            if num_active >= target_minimum_tests:
                continue

            if problem.execution_model and problem.execution_model != "function":
                print(f"  [Skip] Non-function execution model '{problem.execution_model}' is not supported for auto-generation.")
                continue

            print(f"\nProblem '{problem.slug}' has only {num_active} active test cases.")

            # Load the reference solution
            solution = ProblemSolution.query.filter_by(problem_id=problem.id).first()
            if not solution or not solution.code:
                print(f"  [Skip] No verified reference solution found in database for '{problem.slug}'.")
                continue

            # Compile reference solution
            namespace = {}
            try:
                exec(solution.code, namespace)
            except Exception as e:
                print(f"  [Error] Failed to compile solution code for '{problem.slug}': {e}")
                continue

            func = namespace.get(solution.function_name)
            if not func or not callable(func):
                print(f"  [Error] Reference function '{solution.function_name}' not found or callable in solution code.")
                continue

            # Collect argument values from existing active test cases to learn types & ranges
            # active_tcs is guaranteed non-empty here (at least 1 or 2 test cases exist)
            if num_active == 0:
                print(f"  [Skip] Cannot auto-generate arguments without at least 1 existing test case to infer types.")
                continue

            # Group argument values by their position index
            # test_input is like {"args": [arg0, arg1, ...]}
            pos_args_history = []  # list of lists of values for each arg index
            num_args = len(active_tcs[0].test_input.get("args", []))

            for i in range(num_args):
                vals_at_index = []
                for tc in active_tcs:
                    args = tc.test_input.get("args", [])
                    if len(args) > i:
                        vals_at_index.append(args[i])
                pos_args_history.append(vals_at_index)

            # Determine the maximum serial number to avoid duplicate indices
            all_serials = [tc.serial_number for tc in problem.test_cases]
            max_serial = max(all_serials) if all_serials else -1

            num_needed = target_minimum_tests - num_active
            print(f"  Generating {num_needed} new test cases...")

            added_for_this_problem = 0
            attempts = 0
            # Generate until we reach the target, but prevent infinite loops
            while added_for_this_problem < num_needed and attempts < 100:
                attempts += 1

                # Generate args for new test case
                new_args = []
                for vals_at_index in pos_args_history:
                    new_args.append(generate_new_input_arg(vals_at_index))

                # Check for duplicates in existing active inputs to avoid redundant tests
                duplicate_input = False
                for tc in active_tcs:
                    if tc.test_input.get("args") == new_args:
                        duplicate_input = True
                        break
                if duplicate_input:
                    continue

                # Run reference solution to get the expected output
                try:
                    args_copy = deepcopy(new_args)
                    expected_output = func(*args_copy)
                except Exception as e:
                    # If it raises an exception (e.g. invalid inputs generated), skip this attempt
                    continue

                if not is_json_serializable(expected_output):
                    continue

                # Create and persist new test case
                max_serial += 1
                new_tc = TestCase(
                    problem_id=problem.id,
                    serial_number=max_serial,
                    test_input={"args": new_args},
                    expected_output=expected_output,
                    is_active=True,
                )
                db.session.add(new_tc)
                # Keep active list updated for duplicate check
                active_tcs.append(new_tc)
                added_for_this_problem += 1
                total_test_cases_added += 1

            if added_for_this_problem > 0:
                updated_problems_count += 1
                print(f"  [Success] Added {added_for_this_problem} new test cases.")
            else:
                print(f"  [Warning] Failed to generate any valid unique test cases after 100 attempts.")

        db.session.commit()
        print(f"\n==========================================")
        print(f"Add Missing Test Cases Script Executed Successfully!")
        print(f"Problems updated: {updated_problems_count}")
        print(f"Total test cases added: {total_test_cases_added}")
        print(f"==========================================\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add missing test cases to problems with fewer than N tests.")
    parser.add_argument(
        "--min-tests",
        type=int,
        default=5,
        help="The minimum number of active test cases required per problem (default: 5).",
    )
    args = parser.parse_args()

    add_missing_test_cases(args.min_tests)
