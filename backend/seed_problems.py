#!/usr/bin/env python3
"""Seed the database with problem statements"""

from app import create_app, db
from app.models import Problem

app = create_app()

PROBLEMS = [
    {
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "easy",
        "description": """Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to the target.

You may assume that each input has exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

## Constraints

`2 ≤ len(nums) ≤ 10⁴`
`-10⁹ ≤ nums[i] ≤ 10⁹`
`-10⁹ ≤ target ≤ 10⁹`
`Only one valid answer exists.`""",
        "starter_code": """def twoSum(nums, target):
    # Write your solution here
    pass""",
        "test_cases": [
            {"function": "twoSum", "input": "[2, 7, 11, 15], 9", "expected": "[0, 1]"},
            {"function": "twoSum", "input": "[3, 2, 4], 6", "expected": "[1, 2]"},
            {"function": "twoSum", "input": "[3, 3], 6", "expected": "[0, 1]"},
        ],
        "examples": [
            {
                "input": "nums = [2, 7, 11, 15], target = 9",
                "output": "[0, 1]",
                "explanation": "nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": "nums = [3, 2, 4], target = 6",
                "output": "[1, 2]",
                "explanation": "nums[1] + nums[2] == 6, we return [1, 2]."
            }
        ],
        "tags": ["array", "hash-table"]
    },
    {
        "slug": "merge-sorted-array",
        "title": "Merge Sorted Array",
        "difficulty": "easy",
        "description": """You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and two integers `m` and `n`, representing the number of valid elements in `nums1` and `nums2` respectively.

Merge `nums2` into `nums1` as one sorted array.

Note: You may assume that `nums1` has a total length of `m + n`, that it has enough space to hold additional elements from `nums2`.

## Constraints

`nums1.length == m + n`
`nums2.length == n`
`0 ≤ m, n ≤ 200`
`1 ≤ m + n ≤ 200`
`-10⁹ ≤ nums1[i], nums2[j] ≤ 10⁹`""",
        "starter_code": """def merge(nums1, m, nums2, n):
    # Modify nums1 in-place
    pass""",
        "test_cases": [
            {"function": "merge", "input": "[1,2,3,0,0,0], 3, [2,5,6], 3", "expected": "[1,2,2,3,5,6]"},
            {"function": "merge", "input": "[1], 1, [], 0", "expected": "[1]"},
            {"function": "merge", "input": "[0], 0, [1], 1", "expected": "[1]"},
        ],
        "examples": [
            {
                "input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3",
                "output": "[1,2,2,3,5,6]",
                "explanation": "The arrays we are merging are [1,2,3] and [2,5,6]. The result of the merge is [1,2,2,3,5,6]."
            }
        ],
        "tags": ["array", "two-pointers"]
    },
    {
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "easy",
        "description": """Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

## Constraints

`1 ≤ s.length ≤ 10⁴`
`s consists of parentheses only '()[]{}' `""",
        "starter_code": """def isValid(s):
    # Write your solution here
    pass""",
        "test_cases": [
            {"function": "isValid", "args": ["()"], "expected": True},
            {"function": "isValid", "args": ["()[]{}"], "expected": True},
            {"function": "isValid", "args": ["(]"], "expected": False},
        ],
        "examples": [
            {
                "input": 's = "()"',
                "output": "true",
                "explanation": "The string contains matching parentheses."
            },
            {
                "input": 's = "()[]{}"',
                "output": "true",
                "explanation": "All brackets are properly closed."
            },
            {
                "input": 's = "(]"',
                "output": "false",
                "explanation": "The brackets do not match."
            }
        ],
        "tags": ["string", "stack"]
    },
    {
        "slug": "reverse-string",
        "title": "Reverse String",
        "difficulty": "easy",
        "description": """Write a function that reverses a string. The input string is given as an array of characters `s`.

You must do this by modifying the input array in-place with O(1) extra memory.

## Constraints

`1 ≤ s.length ≤ 10⁵`
`s[i] is a printable ascii character.`""",
        "starter_code": """def reverseString(s):
    # Modify s in-place
    pass""",
        "test_cases": [
            {"function": "reverseString", "input": '["h","e","l","l","o"]', "expected": '["o","l","l","e","h"]'},
            {"function": "reverseString", "input": '["H","a","n","n","a","h"]', "expected": '["h","a","n","n","a","H"]'},
        ],
        "examples": [
            {
                "input": 's = ["h","e","l","l","o"]',
                "output": '["o","l","l","e","h"]',
                "explanation": "The string is reversed in-place."
            }
        ],
        "tags": ["string", "two-pointers"]
    },
    {
        "slug": "longest-substring",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "medium",
        "description": """Given a string `s`, find the length of the longest substring without repeating characters.

## Constraints

`0 ≤ s.length ≤ 5 * 10⁴`
`s consists of English letters, digits, symbols and spaces.`""",
        "starter_code": """def lengthOfLongestSubstring(s):
    # Write your solution here
    pass""",
        "test_cases": [
            {"function": "lengthOfLongestSubstring", "input": '"abcabcbb"', "expected": "3"},
            {"function": "lengthOfLongestSubstring", "input": '"bbbbb"', "expected": "1"},
            {"function": "lengthOfLongestSubstring", "input": '"pwwkew"', "expected": "3"},
        ],
        "examples": [
            {
                "input": 's = "abcabcbb"',
                "output": "3",
                "explanation": "The answer is 'abc', with the length of 3."
            },
            {
                "input": 's = "bbbbb"',
                "output": "1",
                "explanation": "The answer is 'b', with the length of 1."
            }
        ],
        "tags": ["string", "sliding-window", "hash-table"]
    },
]

def seed_database():
    with app.app_context():
        # Clear existing data (submissions first due to foreign keys)
        from app.models import Submission
        Submission.query.delete()
        Problem.query.delete()
        
        # Add new problems
        for problem_data in PROBLEMS:
            problem = Problem(
                slug=problem_data["slug"],
                title=problem_data["title"],
                difficulty=problem_data["difficulty"],
                description=problem_data["description"],
                starter_code=problem_data["starter_code"],
                test_cases=problem_data["test_cases"],
                examples=problem_data["examples"],
                tags=problem_data["tags"]
            )
            db.session.add(problem)
        
        db.session.commit()
        print(f"✓ Seeded {len(PROBLEMS)} problems")

if __name__ == "__main__":
    seed_database()
