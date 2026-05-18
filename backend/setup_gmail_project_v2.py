#!/usr/bin/env python
"""
Setup a test project for Gmail user with unique problems
"""
import os
import sys
from app import create_app, db
from app.models import User, Project, Problem, TestCase, ProblemSolution

app = create_app()

def setup_gmail_project():
    with app.app_context():
        # Get Gmail user
        user = User.query.filter_by(email='kalpeshtawde@gmail.com').first()
        if not user:
            print("✗ User kalpeshtawde@gmail.com not found")
            return
        
        print(f"✓ Using user: kalpeshtawde@gmail.com")
        
        # Create test project
        project = Project(
            user=user,
            name='Execution Strategy Test Project',
            is_default=False,
            goal='Test the new execution strategy system',
            strategy='comprehensive',
            level='intermediate'
        )
        db.session.add(project)
        db.session.flush()
        
        print(f"✓ Created project: {project.name} (ID: {project.id})")
        print()
        print("Adding problems...")
        
        # Problem 1: Simple Math
        p1 = Problem(
            slug="simple-add-gmail",
            title="Simple Addition",
            difficulty="easy",
            description="Add two numbers together.",
            starter_code="def solution(a, b):\n    pass",
            examples=[
                {"input": "a = 10, b = 20", "output": "30"},
            ],
            tags=["math"],
            comparison_strategy="exact",
            execution_model="function",
            function_name="solution",
        )
        
        p1_tests = [
            TestCase(serial_number=0, test_input={"args": [10, 20]}, expected_output=30),
            TestCase(serial_number=1, test_input={"args": [5, 5]}, expected_output=10),
        ]
        
        p1_solution = ProblemSolution(
            language="python",
            function_name="solution",
            code="def solution(a, b):\n    return a + b",
            is_active=True,
        )
        
        p1.test_cases = p1_tests
        p1.reference_solution = p1_solution
        db.session.add(p1)
        print("  ✓ Simple Addition (function-based)")
        
        # Problem 2: String Reverse
        p2 = Problem(
            slug="reverse-str-gmail",
            title="Reverse a String",
            difficulty="easy",
            description="Reverse the input string.",
            starter_code="def solution(s):\n    pass",
            examples=[
                {"input": "s = 'hello'", "output": "'olleh'"},
            ],
            tags=["string"],
            comparison_strategy="exact",
            execution_model="function",
            function_name="solution",
        )
        
        p2_tests = [
            TestCase(serial_number=0, test_input={"args": ["hello"]}, expected_output="olleh"),
            TestCase(serial_number=1, test_input={"args": ["test"]}, expected_output="tset"),
        ]
        
        p2_solution = ProblemSolution(
            language="python",
            function_name="solution",
            code="def solution(s):\n    return s[::-1]",
            is_active=True,
        )
        
        p2.test_cases = p2_tests
        p2.reference_solution = p2_solution
        db.session.add(p2)
        print("  ✓ Reverse a String (function-based)")
        
        # Problem 3: Class-based Calculator
        p3 = Problem(
            slug="calculator-gmail",
            title="Simple Calculator",
            difficulty="easy",
            description="Implement a Calculator class with add and multiply methods.",
            starter_code="class Calculator:\n    def __init__(self, value):\n        pass\n    \n    def add(self, x):\n        pass\n    \n    def multiply(self, x):\n        pass\n    \n    def get(self):\n        pass",
            examples=[
                {"input": "Calculator(5); add(3); multiply(2); get()", "output": "16"},
            ],
            tags=["class"],
            comparison_strategy="exact",
            execution_model="class",
            function_name="Calculator",
            class_name="Calculator",
            method_name="get",
        )
        
        p3_tests = [
            TestCase(
                serial_number=0,
                test_input={
                    "ctor_args": [5],
                    "method": "add",
                    "method_args": [3],
                },
                expected_output=None,
            ),
            TestCase(
                serial_number=1,
                test_input={
                    "ctor_args": [5],
                    "method": "multiply",
                    "method_args": [2],
                },
                expected_output=None,
            ),
            TestCase(
                serial_number=2,
                test_input={
                    "ctor_args": [5],
                    "method": "get",
                    "method_args": [],
                },
                expected_output=5,
            ),
        ]
        
        p3_solution = ProblemSolution(
            language="python",
            function_name="Calculator",
            code="""class Calculator:
    def __init__(self, value):
        self.value = value
    
    def add(self, x):
        self.value += x
    
    def multiply(self, x):
        self.value *= x
    
    def get(self):
        return self.value""",
            is_active=True,
        )
        
        p3.test_cases = p3_tests
        p3.reference_solution = p3_solution
        db.session.add(p3)
        print("  ✓ Simple Calculator (class-based)")
        
        # Problem 4: Array Sum
        p4 = Problem(
            slug="array-sum-gmail",
            title="Sum of Array",
            difficulty="easy",
            description="Return the sum of all elements in an array.",
            starter_code="def solution(arr):\n    pass",
            examples=[
                {"input": "arr = [1, 2, 3, 4]", "output": "10"},
            ],
            tags=["array"],
            comparison_strategy="exact",
            execution_model="function",
            function_name="solution",
        )
        
        p4_tests = [
            TestCase(serial_number=0, test_input={"args": [[1, 2, 3, 4]]}, expected_output=10),
            TestCase(serial_number=1, test_input={"args": [[5, 5, 5]]}, expected_output=15),
        ]
        
        p4_solution = ProblemSolution(
            language="python",
            function_name="solution",
            code="def solution(arr):\n    return sum(arr)",
            is_active=True,
        )
        
        p4.test_cases = p4_tests
        p4.reference_solution = p4_solution
        db.session.add(p4)
        print("  ✓ Sum of Array (function-based)")
        
        db.session.commit()
        
        print()
        print("=" * 60)
        print("GMAIL PROJECT SETUP COMPLETE")
        print("=" * 60)
        print()
        print("User: kalpeshtawde@gmail.com")
        print()
        print("Project Details:")
        print(f"  Name: Execution Strategy Test Project")
        print(f"  ID: {project.id}")
        print(f"  Problems: 4")
        print()
        print("Problems Added:")
        print("  1. Simple Addition (function, easy)")
        print("  2. Reverse a String (function, easy)")
        print("  3. Simple Calculator (class, easy)")
        print("  4. Sum of Array (function, easy)")
        print()
        print("Ready to test! Login with Gmail and navigate to the project.")
        print()

if __name__ == '__main__':
    try:
        setup_gmail_project()
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
