#!/usr/bin/env python
"""
Import problems from problems.txt, add solutions and test cases, then validate.
Format: title\tslug\tdifficulty\tdescription

This script:
1. Reads problems from problems.txt
2. Creates problem with appropriate starter_code based on problem type
3. Adds 5-10 test cases for each problem
4. Creates a solution
5. Validates using validate_all_problems.py
"""
import sys
import re
import subprocess
from app import create_app, db
from app.models import Problem, TestCase, ProblemSolution

app = create_app()

# Problem-specific solutions and test cases
PROBLEM_DATA = {
    "pair-sum-finder": {
        "function_name": "pairSum",
        "execution_model": "function",
        "starter_code": """def pairSum(nums: list, target: int) -> list:
    # Find two numbers that add up to target
    # Return their indices
    pass""",
        "solution": """def pairSum(nums: list, target: int) -> list:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []""",
        "test_cases": [
            ([2, 7, 11, 15], 9, [0, 1]),
            ([3, 2, 4], 6, [1, 2]),
            ([3, 3], 6, [0, 1]),
            ([1, 5, 3, 7], 8, [1, 3]),
            ([100, 200, 300, 400], 600, [1, 3]),  # 200 + 400 = 600
        ]
    },
    "island-counter": {
        "function_name": "islandCounter",
        "execution_model": "function",
        "starter_code": """def islandCounter(grid: list) -> int:
    # Count number of islands in grid
    # 1 = land, 0 = water
    pass""",
        "solution": """def islandCounter(grid: list) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count""",
        "test_cases": [
            ([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]], 2),
            ([["1", "1", "1"], ["0", "1", "0"]], 1),
            ([["0", "0"], ["0", "0"]], 0),
            ([["1"]], 1),
            ([["1", "0"], ["1", "0"]], 1),  # Connected vertically
        ]
    },
    "anagram-detective": {
        "function_name": "isAnagram",
        "execution_model": "function",
        "starter_code": """def isAnagram(s: str, t: str) -> bool:
    # Check if t is an anagram of s
    pass""",
        "solution": """def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    return sorted(s) == sorted(t)""",
        "test_cases": [
            ("anagram", "nagaram", True),
            ("rat", "car", False),
            ("a", "a", True),
            ("ab", "ba", True),
            ("abc", "def", False),
        ]
    },
    "palindrome-probe": {
        "function_name": "isPalindrome",
        "execution_model": "function",
        "starter_code": """def isPalindrome(x: int) -> bool:
    # Check if integer is palindrome
    # Negative numbers are not palindromes
    pass""",
        "solution": """def isPalindrome(x: int) -> bool:
    if x < 0:
        return False
    original = x
    reversed_num = 0
    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    return original == reversed_num""",
        "test_cases": [
            (121, True),
            (-121, False),
            (10, False),
            (0, True),
            (12321, True),
        ]
    },
    "bracket-harmony": {
        "function_name": "isValid",
        "execution_model": "function",
        "starter_code": """def isValid(s: str) -> bool:
    # Check if brackets are balanced and properly nested
    pass""",
        "solution": """def isValid(s: str) -> bool:
    stack = []
    pairs = {'(': ')', '{': '}', '[': ']'}
    for char in s:
        if char in pairs:
            stack.append(char)
        else:
            if not stack or pairs[stack.pop()] != char:
                return False
    return len(stack) == 0""",
        "test_cases": [
            ("()", True),
            ("()[]{}", True),
            ("(]", False),
            ("{[]}", True),
            ("", True),
        ]
    },
    "sorted-array-probe": {
        "function_name": "search",
        "execution_model": "function",
        "starter_code": """def search(nums: list, target: int) -> int:
    # Binary search for target in sorted array
    # Return index or -1 if not found
    pass""",
        "solution": """def search(nums: list, target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "test_cases": [
            ([-1, 0, 3, 5, 9, 12], 9, 4),
            ([-1, 0, 3, 5, 9, 12], 13, -1),
            ([5], 5, 0),
            ([1, 3], 3, 1),
            ([1, 3, 5, 7], 7, 3),
        ]
    },
    "peak-profit-window": {
        "function_name": "maxProfit",
        "execution_model": "function",
        "starter_code": """def maxProfit(prices: list) -> int:
    # Find max profit from one buy-sell transaction
    pass""",
        "solution": """def maxProfit(prices: list) -> int:
    if not prices:
        return 0
    min_price = prices[0]
    max_profit = 0
    for price in prices[1:]:
        max_profit = max(max_profit, price - min_price)
        min_price = min(min_price, price)
    return max_profit""",
        "test_cases": [
            ([7, 1, 5, 3, 6, 4], 5),
            ([7, 6, 4, 3, 1], 0),
            ([2, 4, 1], 2),
            ([1, 2, 3, 4, 5], 4),
            ([5, 1, 3, 4, 2], 3),
        ]
    },
    "ripple-sum": {
        "function_name": "maxSubArray",
        "execution_model": "function",
        "starter_code": """def maxSubArray(nums: list) -> int:
    # Find maximum sum of contiguous subarray
    pass""",
        "solution": """def maxSubArray(nums: list) -> int:
    max_sum = nums[0]
    current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum""",
        "test_cases": [
            ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
            ([5], 5),
            ([-1], -1),
            ([-2, -1], -1),
            ([1, 2, 3, 4], 10),
        ]
    },
    "staircase-paths": {
        "function_name": "climbStairs",
        "execution_model": "function",
        "starter_code": """def climbStairs(n: int) -> int:
    # Count ways to climb n stairs (1 or 2 steps at a time)
    pass""",
        "solution": """def climbStairs(n: int) -> int:
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b""",
        "test_cases": [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 5),
            (5, 8),
        ]
    },
    "two-sum-hash": {
        "function_name": "twoSum",
        "execution_model": "function",
        "starter_code": """def twoSum(nums: list, target: int) -> list:
    # Find two numbers that add up to target
    # Return their indices
    pass""",
        "solution": """def twoSum(nums: list, target: int) -> list:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
        "test_cases": [
            ([2, 7, 11, 15], 9, [0, 1]),
            ([3, 2, 4], 6, [1, 2]),
            ([3, 3], 6, [0, 1]),
            ([1, 5, 3, 7], 8, [1, 3]),
            ([100, 200, 300, 400], 600, [1, 3]),  # 200 + 400 = 600
        ]
    },
}

def create_problem_with_tests(title, slug, difficulty, description):
    """Create a problem with tests and solution"""
    if slug not in PROBLEM_DATA:
        print(f"⊘ {slug}: No test data defined, skipping")
        return False
    
    data = PROBLEM_DATA[slug]
    
    with app.app_context():
        # Delete existing problem if it exists
        existing = Problem.query.filter_by(slug=slug).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
        
        # Create problem
        problem = Problem(
            slug=slug,
            title=title,
            difficulty=difficulty,
            description=description,
            starter_code=data["starter_code"],
            execution_model=data["execution_model"],
            function_name=data["function_name"],
            comparison_strategy="exact",
            examples=[],
            tags=[]
        )
        db.session.add(problem)
        db.session.flush()
        
        problem_id = problem.id
        
        # Add test cases
        for idx, test_case in enumerate(data["test_cases"]):
            if len(test_case) == 3:
                arg1, arg2, expected = test_case
                test_input = {"args": [arg1, arg2]}
            else:
                arg, expected = test_case
                test_input = {"args": [arg]}
            
            tc = TestCase(
                problem_id=problem_id,
                serial_number=idx,
                test_input=test_input,
                expected_output=expected,
                is_active=True
            )
            db.session.add(tc)
        
        # Add solution
        solution = ProblemSolution(
            problem_id=problem_id,
            code=data["solution"],
            language="python",
            function_name=data["function_name"],
            is_active=True,
            notes="Imported solution"
        )
        db.session.add(solution)
        db.session.commit()
        
        return True

def import_problems_from_file(filename):
    """Import problems from txt file"""
    problems = []
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Parse tab-separated values
                parts = line.split('\t')
                if len(parts) >= 4:
                    title = parts[0].strip('"')
                    slug = parts[1].strip('"')
                    difficulty = parts[2].strip('"')
                    description = parts[3].strip('"')
                    
                    problems.append({
                        'title': title,
                        'slug': slug,
                        'difficulty': difficulty,
                        'description': description
                    })
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return []
    
    return problems

def main():
    print()
    print("=" * 80)
    print("IMPORT PROBLEMS FROM problems.txt")
    print("=" * 80)
    print()
    
    # Read problems from file
    problems = import_problems_from_file('/Users/kalpeshtawde/workdir/pypycode/backend/problems.txt')
    
    if not problems:
        print("✗ No problems found in file")
        return
    
    print(f"Found {len(problems)} problems in file")
    print()
    
    # Import only problems we have test data for
    imported = 0
    skipped = 0
    
    for prob in problems:
        slug = prob['slug']
        
        if slug not in PROBLEM_DATA:
            print(f"⊘ {slug}: No test data defined, skipping")
            skipped += 1
            continue
        
        try:
            if create_problem_with_tests(prob['title'], slug, prob['difficulty'], prob['description']):
                print(f"✓ {slug}: Created with tests and solution")
                imported += 1
            else:
                print(f"✗ {slug}: Failed to create")
        except Exception as e:
            print(f"✗ {slug}: {str(e)[:100]}")
    
    print()
    print("=" * 80)
    print(f"IMPORT SUMMARY")
    print("=" * 80)
    print(f"Total in file: {len(problems)}")
    print(f"✓ Imported: {imported}")
    print(f"⊘ Skipped: {skipped}")
    print("=" * 80)
    print()
    
    if imported > 0:
        print("Running validation...")
        print()
        result = subprocess.run(
            ['python', 'validate_all_problems.py'],
            cwd='/Users/kalpeshtawde/workdir/pypycode/backend',
            capture_output=False
        )
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
