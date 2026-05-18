#!/usr/bin/env python
"""
Setup a test project with various problems for manual testing.
"""
import os
import sys
from app import create_app, db
from app.models import User, Project, Problem, TestCase, ProblemSolution

app = create_app()

def setup_test_project():
    with app.app_context():
        # Create or get test user
        user = User.query.filter_by(email='testuser@example.com').first()
        if not user:
            user = User(
                username='testuser2',
                email='testuser@example.com',
                screen_name='testuser2'
            )
            user.set_password('test1234')
            db.session.add(user)
            db.session.flush()
        else:
            print(f"✓ Using existing user: {user.email}")
        
        # Create test project
        project = Project(
            user=user,
            name='Test Project',
            is_default=False,
            goal='Test the new execution strategy system',
            strategy='comprehensive',
            level='intermediate'
        )
        db.session.add(project)
        db.session.flush()
        
        print(f"✓ Created project: {project.name} (ID: {project.id})")
        print(f"✓ Test user: testuser@example.com / test1234")
        print()
        
        # Problem 1: Function-based (Easy)
        print("Adding problems...")
        
        p1 = Problem(
            slug="add-two-numbers",
            title="Add Two Numbers",
            difficulty="easy",
            description="Given two integers, return their sum.",
            starter_code="def solution(a, b):\n    pass",
            examples=[
                {"input": "a = 5, b = 3", "output": "8"},
                {"input": "a = -1, b = 1", "output": "0"},
            ],
            tags=["math", "basic"],
            comparison_strategy="exact",
            execution_model="function",
            function_name="solution",
        )
        
        p1_tests = [
            TestCase(serial_number=0, test_input={"args": [5, 3]}, expected_output=8),
            TestCase(serial_number=1, test_input={"args": [-1, 1]}, expected_output=0),
            TestCase(serial_number=2, test_input={"args": [0, 0]}, expected_output=0),
            TestCase(serial_number=3, test_input={"args": [100, 200]}, expected_output=300),
        ]
        
        p1_solution = ProblemSolution(
            language="python",
            function_name="solution",
            code="def solution(a, b):\n    return a + b",
            is_active=True,
            notes="Simple addition"
        )
        
        p1.test_cases = p1_tests
        p1.reference_solution = p1_solution
        db.session.add(p1)
        print("  ✓ Add Two Numbers (function-based, easy)")
        
        # Problem 2: Function-based (Medium)
        p2 = Problem(
            slug="reverse-string",
            title="Reverse String",
            difficulty="medium",
            description="Given a string, return it reversed.",
            starter_code="def solution(s):\n    pass",
            examples=[
                {"input": "s = 'hello'", "output": "'olleh'"},
                {"input": "s = 'a'", "output": "'a'"},
            ],
            tags=["string"],
            comparison_strategy="exact",
            execution_model="function",
            function_name="solution",
        )
        
        p2_tests = [
            TestCase(serial_number=0, test_input={"args": ["hello"]}, expected_output="olleh"),
            TestCase(serial_number=1, test_input={"args": ["a"]}, expected_output="a"),
            TestCase(serial_number=2, test_input={"args": [""]}, expected_output=""),
            TestCase(serial_number=3, test_input={"args": ["racecar"]}, expected_output="racecar"),
        ]
        
        p2_solution = ProblemSolution(
            language="python",
            function_name="solution",
            code="def solution(s):\n    return s[::-1]",
            is_active=True,
            notes="String slicing"
        )
        
        p2.test_cases = p2_tests
        p2.reference_solution = p2_solution
        db.session.add(p2)
        print("  ✓ Reverse String (function-based, medium)")
        
        # Problem 3: Class-based (Medium)
        p3 = Problem(
            slug="counter-class",
            title="Simple Counter",
            difficulty="easy",
            description="Implement a Counter class that tracks increments.",
            starter_code="class Counter:\n    def __init__(self):\n        pass\n    \n    def increment(self):\n        pass\n    \n    def get(self):\n        pass",
            examples=[
                {"input": "Counter(); increment(); increment(); get()", "output": "2"},
            ],
            tags=["class", "design"],
            comparison_strategy="exact",
            execution_model="class",
            function_name="Counter",
            class_name="Counter",
            method_name="get",
        )
        
        p3_tests = [
            TestCase(
                serial_number=0,
                test_input={
                    "ctor_args": [],
                    "method": "get",
                    "method_args": [],
                },
                expected_output=0,
            ),
            TestCase(
                serial_number=1,
                test_input={
                    "ctor_args": [],
                    "method": "increment",
                    "method_args": [],
                },
                expected_output=None,
            ),
            TestCase(
                serial_number=2,
                test_input={
                    "ctor_args": [],
                    "method": "get",
                    "method_args": [],
                },
                expected_output=1,
            ),
        ]
        
        p3_solution = ProblemSolution(
            language="python",
            function_name="Counter",
            code="""class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def get(self):
        return self.count""",
            is_active=True,
            notes="Simple state management"
        )
        
        p3.test_cases = p3_tests
        p3.reference_solution = p3_solution
        db.session.add(p3)
        print("  ✓ Simple Counter (class-based, easy)")
        
        # Problem 4: Class-based (Medium) - Range Sum Query
        p4 = Problem(
            slug="range-sum-immutable",
            title="Range Sum Query - Immutable",
            difficulty="medium",
            description="Given an integer array nums, handle multiple range sum queries efficiently.",
            starter_code="class NumArray:\n    def __init__(self, nums):\n        pass\n    \n    def sumRange(self, left, right):\n        pass",
            examples=[
                {"input": "NumArray([1,2,3,4,5]); sumRange(0,2)", "output": "6"},
                {"input": "sumRange(1,3)", "output": "9"},
            ],
            tags=["array", "prefix-sum"],
            comparison_strategy="exact",
            execution_model="class",
            function_name="NumArray",
            class_name="NumArray",
            method_name="sumRange",
        )
        
        p4_tests = [
            TestCase(
                serial_number=0,
                test_input={
                    "ctor_args": [[1, 2, 3, 4, 5]],
                    "method": "sumRange",
                    "method_args": [0, 2],
                },
                expected_output=6,
            ),
            TestCase(
                serial_number=1,
                test_input={
                    "ctor_args": [[1, 2, 3, 4, 5]],
                    "method": "sumRange",
                    "method_args": [1, 3],
                },
                expected_output=9,
            ),
            TestCase(
                serial_number=2,
                test_input={
                    "ctor_args": [[1, 2, 3, 4, 5]],
                    "method": "sumRange",
                    "method_args": [0, 4],
                },
                expected_output=15,
            ),
        ]
        
        p4_solution = ProblemSolution(
            language="python",
            function_name="NumArray",
            code="""class NumArray:
    def __init__(self, nums):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]""",
            is_active=True,
            notes="Prefix sum optimization"
        )
        
        p4.test_cases = p4_tests
        p4.reference_solution = p4_solution
        db.session.add(p4)
        print("  ✓ Range Sum Query (class-based, medium)")
        
        # Problem 5: Function-based with array (Medium)
        p5 = Problem(
            slug="find-max",
            title="Find Maximum",
            difficulty="easy",
            description="Given an array of integers, return the maximum value.",
            starter_code="def solution(nums):\n    pass",
            examples=[
                {"input": "nums = [1, 5, 3, 9, 2]", "output": "9"},
                {"input": "nums = [-5, -2, -10]", "output": "-2"},
            ],
            tags=["array"],
            comparison_strategy="exact",
            execution_model="function",
            function_name="solution",
        )
        
        p5_tests = [
            TestCase(serial_number=0, test_input={"args": [[1, 5, 3, 9, 2]]}, expected_output=9),
            TestCase(serial_number=1, test_input={"args": [[-5, -2, -10]]}, expected_output=-2),
            TestCase(serial_number=2, test_input={"args": [[42]]}, expected_output=42),
            TestCase(serial_number=3, test_input={"args": [[100, 50, 75, 25]]}, expected_output=100),
        ]
        
        p5_solution = ProblemSolution(
            language="python",
            function_name="solution",
            code="def solution(nums):\n    return max(nums)",
            is_active=True,
            notes="Built-in max function"
        )
        
        p5.test_cases = p5_tests
        p5.reference_solution = p5_solution
        db.session.add(p5)
        print("  ✓ Find Maximum (function-based, easy)")
        
        # Problem 6: Function-based (Hard) - Two Sum
        p6 = Problem(
            slug="two-sum-test",
            title="Two Sum",
            difficulty="medium",
            description="Given an array of integers and a target, return indices of two numbers that add up to target.",
            starter_code="def solution(nums, target):\n    pass",
            examples=[
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"},
            ],
            tags=["array", "hash-table"],
            comparison_strategy="exact",
            execution_model="function",
            function_name="solution",
        )
        
        p6_tests = [
            TestCase(serial_number=0, test_input={"args": [[2, 7, 11, 15], 9]}, expected_output=[0, 1]),
            TestCase(serial_number=1, test_input={"args": [[3, 2, 4], 6]}, expected_output=[1, 2]),
            TestCase(serial_number=2, test_input={"args": [[3, 3], 6]}, expected_output=[0, 1]),
            TestCase(serial_number=3, test_input={"args": [[2, 5, 5, 11], 10]}, expected_output=[1, 2]),
        ]
        
        p6_solution = ProblemSolution(
            language="python",
            function_name="solution",
            code="""def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
            is_active=True,
            notes="Hash map approach - O(n) time"
        )
        
        p6.test_cases = p6_tests
        p6.reference_solution = p6_solution
        db.session.add(p6)
        print("  ✓ Two Sum (function-based, medium)")
        
        db.session.commit()
        
        print()
        print("=" * 60)
        print("TEST PROJECT SETUP COMPLETE")
        print("=" * 60)
        print()
        print("Project Details:")
        print(f"  Name: Test Project")
        print(f"  ID: {project.id}")
        print(f"  Problems: 6")
        print()
        print("Test User:")
        print(f"  Email: testuser@example.com")
        print(f"  Password: test1234")
        print()
        print("Problems Added:")
        print("  1. Add Two Numbers (function, easy)")
        print("  2. Reverse String (function, medium)")
        print("  3. Simple Counter (class, easy)")
        print("  4. Range Sum Query (class, medium)")
        print("  5. Find Maximum (function, easy)")
        print("  6. Two Sum (function, medium)")
        print()
        print("Next Steps:")
        print("  1. Login with testuser@example.com / test1234")
        print("  2. Navigate to 'Test Project'")
        print("  3. Try solving the problems")
        print("  4. Test both function-based and class-based problems")
        print()

if __name__ == '__main__':
    try:
        setup_test_project()
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        db.session.rollback()
        sys.exit(1)
