#!/usr/bin/env python3
"""Run inside the api container: python seed.py"""
import sys, os
sys.path.insert(0, "/app")
os.environ.setdefault("DATABASE_URL", "postgresql://pypycode:pypycode@db:5432/pypycode")
os.environ.setdefault("SECRET_KEY", "seed")
os.environ.setdefault("CELERY_BROKER_URL", "redis://redis:6379/1")
os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://redis:6379/2")

from app import create_app, db
from app.models import Problem, User, TestCase

PROBLEMS = [
    {
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "easy",
        "description": """Given a list of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Return the answer in any order.

**Constraints**
- `2 ≤ len(nums) ≤ 10⁴`
- `-10⁹ ≤ nums[i] ≤ 10⁹`
- Only one valid answer exists""",
        "starter_code": "def solution(nums: list[int], target: int) -> list[int]:\n    # Your code here\n    pass",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0, 1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1, 2]"},
        ],
        "test_cases": [
            {"function": "solution", "input": "[2,7,11,15], 9", "expectedOutput": "[0,1]"},
            {"function": "solution", "input": "[3,2,4], 6", "expectedOutput": "[1,2]"},
            {"function": "solution", "input": "[3,3], 6", "expectedOutput": "[0,1]"},
        ],
        "tags": ["array", "hash-table"],
    },
    {
        "slug": "reverse-string",
        "title": "Reverse a String",
        "difficulty": "easy",
        "description": """Write a function that reverses a string and returns it.

**Constraints**
- `1 ≤ len(s) ≤ 10⁵`
- `s` consists of printable ASCII characters""",
        "starter_code": "def solution(s: str) -> str:\n    pass",
        "examples": [
            {"input": 's = "hello"', "output": '"olleh"'},
            {"input": 's = "Python"', "output": '"nohtyP"'},
        ],
        "test_cases": [
            {"function": "solution", "input": "\"hello\"", "expectedOutput": "\"olleh\""},
            {"function": "solution", "input": "\"Python\"", "expectedOutput": "\"nohtyP\""},
            {"function": "solution", "input": "\"a\"", "expectedOutput": "\"a\""},
            {"function": "solution", "input": "\"abcd\"", "expectedOutput": "\"dcba\""},
        ],
        "tags": ["string"],
    },
    {
        "slug": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "easy",
        "description": """A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string `s`, return `True` if it is a palindrome, or `False` otherwise.""",
        "starter_code": "def solution(s: str) -> bool:\n    pass",
        "examples": [
            {"input": 's = "A man, a plan, a canal: Panama"', "output": "True", "explanation": "amanaplanacanalpanama is a palindrome"},
            {"input": 's = "race a car"', "output": "False"},
        ],
        "test_cases": [
            {"function": "solution", "input": "\"A man, a plan, a canal: Panama\"", "expectedOutput": "true"},
            {"function": "solution", "input": "\"race a car\"", "expectedOutput": "false"},
            {"function": "solution", "input": "\" \"", "expectedOutput": "true"},
            {"function": "solution", "input": "\"0P\"", "expectedOutput": "false"},
        ],
        "tags": ["string", "two-pointers"],
    },
    {
        "slug": "maximum-subarray",
        "title": "Maximum Subarray",
        "difficulty": "medium",
        "description": """Given an integer array `nums`, find the subarray with the largest sum and return its sum.

**Constraints**
- `1 ≤ len(nums) ≤ 10⁵`
- `-10⁴ ≤ nums[i] ≤ 10⁴`

**Follow up:** Can you solve it in O(n) time?""",
        "starter_code": "def solution(nums: list[int]) -> int:\n    pass",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "Subarray [4,-1,2,1] has sum 6"},
            {"input": "nums = [1]", "output": "1"},
        ],
        "test_cases": [
            {"function": "solution", "input": "[-2,1,-3,4,-1,2,1,-5,4]", "expectedOutput": "6"},
            {"function": "solution", "input": "[1]", "expectedOutput": "1"},
            {"function": "solution", "input": "[5,4,-1,7,8]", "expectedOutput": "23"},
            {"function": "solution", "input": "[-1,-2,-3]", "expectedOutput": "-1"},
        ],
        "tags": ["array", "dynamic-programming", "divide-and-conquer"],
    },
    {
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "medium",
        "description": """Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket.""",
        "starter_code": "def solution(s: str) -> bool:\n    pass",
        "examples": [
            {"input": 's = "()"', "output": "True"},
            {"input": 's = "()[]{}"', "output": "True"},
            {"input": 's = "(]"', "output": "False"},
        ],
        "test_cases": [
            {"function": "solution", "input": "\"()\"", "expectedOutput": "true"},
            {"function": "solution", "input": "\"()[]{}\"", "expectedOutput": "true"},
            {"function": "solution", "input": "\"(]\"", "expectedOutput": "false"},
            {"function": "solution", "input": "\"([)]\"", "expectedOutput": "false"},
            {"function": "solution", "input": "\"{[]}\"", "expectedOutput": "true"},
        ],
        "tags": ["string", "stack"],
    },
    {
        "slug": "binary-search",
        "title": "Binary Search",
        "difficulty": "easy",
        "description": """Given an array of integers `nums` sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists return its index. Otherwise return `-1`.

You must write an algorithm with `O(log n)` runtime complexity.""",
        "starter_code": "def solution(nums: list[int], target: int) -> int:\n    pass",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"},
        ],
        "test_cases": [
            {"function": "solution", "input": "[-1,0,3,5,9,12], 9", "expectedOutput": "4"},
            {"function": "solution", "input": "[-1,0,3,5,9,12], 2", "expectedOutput": "-1"},
            {"function": "solution", "input": "[5], 5", "expectedOutput": "0"},
            {"function": "solution", "input": "[1,3,5,7,9], 7", "expectedOutput": "3"},
        ],
        "tags": ["array", "binary-search"],
    },
    {
        "slug": "climbing-stairs",
        "title": "Climbing Stairs",
        "difficulty": "medium",
        "description": """You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can climb `1` or `2` steps. In how many distinct ways can you climb to the top?

**Constraints:** `1 ≤ n ≤ 45`""",
        "starter_code": "def solution(n: int) -> int:\n    pass",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "1+1, 2"},
            {"input": "n = 3", "output": "3", "explanation": "1+1+1, 1+2, 2+1"},
        ],
        "test_cases": [
            {"function": "solution", "args": [2], "expected": 2},
            {"function": "solution", "args": [3], "expected": 3},
            {"function": "solution", "args": [5], "expected": 8},
            {"function": "solution", "args": [10], "expected": 89},
        ],
        "tags": ["dynamic-programming", "math"],
    },
    {
        "slug": "merge-intervals",
        "title": "Merge Intervals",
        "difficulty": "hard",
        "description": """Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Constraints**
- `1 ≤ len(intervals) ≤ 10⁴`
- `intervals[i].length == 2`
- `0 ≤ start_i ≤ end_i ≤ 10⁴`""",
        "starter_code": "def solution(intervals: list[list[int]]) -> list[list[int]]:\n    pass",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"},
        ],
        "test_cases": [
            {"function": "solution", "args": [[[1,3],[2,6],[8,10],[15,18]]], "expected": [[1,6],[8,10],[15,18]]},
            {"function": "solution", "args": [[[1,4],[4,5]]], "expected": [[1,5]]},
            {"function": "solution", "args": [[[1,4],[2,3]]], "expected": [[1,4]]},
        ],
        "tags": ["array", "sorting"],
    },
]


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        for p in PROBLEMS:
            if not Problem.query.filter_by(slug=p["slug"]).first():
                # Extract test cases before creating problem
                test_cases = p.pop("test_cases", [])
                
                # Create problem without test_cases
                problem = Problem(**p)
                db.session.add(problem)
                db.session.flush()
                
                # Create test cases as separate records
                for idx, tc in enumerate(test_cases):
                    test_case = TestCase(
                        problem_id=problem.id,
                        serial_number=idx,
                        function=tc.get("function", "solution"),
                        input=tc.get("input", ""),
                        expected_output=tc.get("expectedOutput", ""),
                    )
                    db.session.add(test_case)
                
                print(f"  + {p['title']}")
            else:
                print(f"  ~ {p['title']} (already exists)")

        # Demo user
        if not User.query.filter_by(username="demo").first():
            u = User(username="demo", email="demo@pypycode.dev")
            u.set_password("demo1234")
            db.session.add(u)
            print("  + demo user (demo@pypycode.dev / demo1234)")

        db.session.commit()
        print("Seed complete.")


if __name__ == "__main__":
    seed()
