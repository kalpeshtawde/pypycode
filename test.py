import requests

BASE_URL = "https://pypycode.com/api/problems/public-ingest"
INGEST_KEY = "EMDgUmg7tzsgdf5r3eFd"

problems = [
    {
        "slug": "reverse-linked-list", "title": "Reverse Linked List", "difficulty": "easy",
        "description": "Given the head of a singly linked list, reverse it and return the reversed list.",
        "starterCode": "def reverseList(head):\n    pass",
        "examples": [{"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "Reverse the list."}],
        "testCases": [
            {"function": "reverseList", "input": "[1,2,3,4,5]", "expected": "[5,4,3,2,1]"},
            {"function": "reverseList", "input": "[1,2]", "expected": "[2,1]"}
        ],
        "tags": ["linked-list", "recursion"]
    },
    {
        "slug": "valid-parentheses", "title": "Valid Parentheses", "difficulty": "easy",
        "description": "Given a string of brackets, determine if it is valid (properly opened and closed).",
        "starterCode": "def isValid(s: str) -> bool:\n    pass",
        "examples": [{"input": "s = \"()[]{}\"", "output": "true", "explanation": "All brackets match."}],
        "testCases": [
            {"function": "isValid", "input": "\"()\"", "expected": "True"},
            {"function": "isValid", "input": "\"(]\"", "expected": "False"}
        ],
        "tags": ["string", "stack"]
    },
    {
        "slug": "climbing-stairs", "title": "Climbing Stairs", "difficulty": "easy",
        "description": "You can climb 1 or 2 steps at a time. How many distinct ways can you reach the top of n steps?",
        "starterCode": "def climbStairs(n: int) -> int:\n    pass",
        "examples": [{"input": "n = 3", "output": "3", "explanation": "1+1+1, 1+2, 2+1"}],
        "testCases": [
            {"function": "climbStairs", "input": "2", "expected": "2"},
            {"function": "climbStairs", "input": "5", "expected": "8"}
        ],
        "tags": ["dynamic-programming", "math"]
    },
    {
        "slug": "binary-search", "title": "Binary Search", "difficulty": "easy",
        "description": "Search a sorted array for a target in O(log n). Return its index or -1 if not found.",
        "starterCode": "def search(nums: list, target: int) -> int:\n    pass",
        "examples": [{"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 is at index 4."}],
        "testCases": [
            {"function": "search", "input": "[-1,0,3,5,9,12], 9", "expected": "4"},
            {"function": "search", "input": "[-1,0,3,5,9,12], 2", "expected": "-1"}
        ],
        "tags": ["array", "binary-search"]
    },
    {
        "slug": "maximum-subarray", "title": "Maximum Subarray", "difficulty": "medium",
        "description": "Find the contiguous subarray with the largest sum and return its sum.",
        "starterCode": "def maxSubArray(nums: list) -> int:\n    pass",
        "examples": [{"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "[4,-1,2,1] sums to 6."}],
        "testCases": [
            {"function": "maxSubArray", "input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected": "6"},
            {"function": "maxSubArray", "input": "[5,4,-1,7,8]", "expected": "23"}
        ],
        "tags": ["array", "dynamic-programming"]
    }
]

for p in problems:
    res = requests.post(BASE_URL, json={**p, "ingestKey": INGEST_KEY})
    print(f"{p['title']}: {res.status_code} — {res.text}")
