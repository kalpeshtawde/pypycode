#!/usr/bin/env python
"""
Create a problem with 10 test cases and a solution, then validate all tests pass.
This script:
1. Creates 1 problem (Two Sum)
2. Adds 10 test cases
3. Adds 1 solution
4. Runs unit tests to validate all test cases pass against the solution
"""
import sys
import json
from app import create_app, db
from app.models import Problem, TestCase, ProblemSolution
from app.services.runner import run_code_against_problem

app = create_app()

def create_problem_with_test_cases():
    """Create a problem with 10 test cases and return problem ID and solution code"""
    with app.app_context():
        # Delete existing problem if it exists
        existing = Problem.query.filter_by(slug="two-sum-validation").first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            print("✓ Deleted existing problem")
        
        # Create problem
        problem = Problem(
            slug="two-sum-validation",
            title="Two Sum - Validation Test",
            difficulty="easy",
            description="Given an array of integers nums and an integer target, return the indices of the two numbers that add up to the target. You may assume each input has exactly one solution, and you cannot use the same element twice.",
            starter_code="def twoSum(nums, target):\n    # Your solution here\n    pass",
            execution_model="function",
            function_name="twoSum",
            comparison_strategy="exact",
            examples=[
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"}
            ],
            tags=["array", "hash-map", "two-pointers"]
        )
        db.session.add(problem)
        db.session.flush()
        
        problem_id = problem.id
        print(f"✓ Created problem: {problem.title} (ID: {problem_id})")
        print()
        
        # Create 10 test cases
        test_cases_data = [
            # Basic cases
            ([2, 7, 11, 15], 9, [0, 1]),
            ([3, 2, 4], 6, [1, 2]),
            ([3, 3], 6, [0, 1]),
            
            # Edge cases
            ([2, 3], 5, [0, 1]),
            ([1, 2, 3, 4, 5], 9, [3, 4]),
            
            # Negative numbers
            ([-1, -2, -3, 5, 10], 7, [2, 4]),
            ([0, 0, 3, 4], 0, [0, 1]),
            
            # Larger numbers
            ([1000000, 1000001], 2000001, [0, 1]),
            ([100, 200, 300, 400], 500, [1, 2]),  # 200 + 300 = 500
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 17, [7, 8]),
        ]
        
        print("Adding 10 test cases:")
        for idx, (nums, target, expected) in enumerate(test_cases_data):
            tc = TestCase(
                problem_id=problem_id,
                serial_number=idx,
                test_input={"args": [nums, target]},
                expected_output=expected,
                is_active=True
            )
            db.session.add(tc)
            print(f"  {idx + 1}. nums={nums}, target={target} → expected={expected}")
        
        db.session.commit()
        print(f"\n✓ Created 10 test cases")
        print()
        
        # Create solution
        solution_code = """def twoSum(nums, target):
    # Use a hash map to store value -> index
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
        
        solution = ProblemSolution(
            problem_id=problem_id,
            code=solution_code,
            language="python",
            function_name="twoSum",
            is_active=True,
            notes="Optimal O(n) solution using hash map"
        )
        db.session.add(solution)
        db.session.commit()
        
        print("✓ Created solution")
        print(f"  Language: Python")
        print(f"  Function: twoSum")
        print(f"  Approach: Hash map (O(n) time, O(n) space)")
        print()
        
        return problem_id, solution_code


def validate_solution(problem_id, solution_code):
    """Run the solution against all test cases"""
    print("=" * 70)
    print("VALIDATION: Running solution against all test cases")
    print("=" * 70)
    print()
    
    with app.app_context():
        # Get problem from DB to get test cases
        problem = Problem.query.get(problem_id)
        
        # Run the solution
        result = run_code_against_problem(problem, solution_code)
        
        print(f"Status: {result['status']}")
        print(f"Total Tests: {result['total_tests']}")
        print(f"Passed: {result['passed_tests']}")
        print(f"Failed: {result['total_tests'] - result['passed_tests']}")
        print()
        
        if result.get('error_output'):
            print("Error Output:")
            print("-" * 70)
            print(result['error_output'])
        
        print()
        print("=" * 70)
        
        if result['status'] == 'accepted':
            print("✓ SUCCESS! All test cases passed!")
            print("=" * 70)
            return True
        else:
            print("✗ FAILURE! Some test cases failed.")
            print("=" * 70)
            return False


def main():
    print()
    print("=" * 70)
    print("PROBLEM VALIDATION SETUP")
    print("=" * 70)
    print()
    
    # Step 1: Create problem with test cases
    problem_id, solution_code = create_problem_with_test_cases()
    
    # Step 2: Validate solution
    success = validate_solution(problem_id, solution_code)
    
    if success:
        print()
        print("✓ Problem is ready for use!")
        print(f"  Slug: two-sum-validation")
        print(f"  ID: {problem_id}")
        print(f"  Test Cases: 10")
        print(f"  Solution: Validated ✓")
        sys.exit(0)
    else:
        print()
        print("✗ Problem validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
