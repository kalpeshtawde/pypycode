#!/usr/bin/env python
"""
Script to create problems with the new execution strategy system.
Usage: python create_problems.py
"""
import os
import sys
from app import create_app, db
from app.models import Problem, TestCase, ProblemSolution

app = create_app()

def create_function_problem():
    """Example: Two Sum - function-based problem"""
    problem = Problem(
        slug="two-sum",
        title="Two Sum",
        difficulty="easy",
        description="Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target.",
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
    
    test_cases = [
        TestCase(
            serial_number=0,
            test_input={"args": [[2, 7, 11, 15], 9]},
            expected_output=[0, 1],
        ),
        TestCase(
            serial_number=1,
            test_input={"args": [[3, 2, 4], 6]},
            expected_output=[1, 2],
        ),
        TestCase(
            serial_number=2,
            test_input={"args": [[3, 3], 6]},
            expected_output=[0, 1],
        ),
    ]
    
    solution = ProblemSolution(
        language="python",
        function_name="solution",
        code="def solution(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
        is_active=True,
        notes="Hash map approach",
    )
    
    problem.test_cases = test_cases
    problem.reference_solution = solution
    
    db.session.add(problem)
    db.session.commit()
    print(f"✓ Created function-based problem: {problem.slug}")


def create_class_problem():
    """Example: Range Sum Query - class-based problem"""
    problem = Problem(
        slug="range-sum-query",
        title="Range Sum Query - Immutable",
        difficulty="easy",
        description="Given an integer array nums, handle multiple queries of type: calculate the sum of the elements of nums between indices left and right (inclusive).",
        starter_code="class RangeSumQuery:\n    def __init__(self, nums):\n        pass\n    \n    def sumRange(self, left, right):\n        pass",
        examples=[
            {"input": "RangeSumQuery([-2,0,3,-5,2,-1]); sumRange(0,2)", "output": "1"},
            {"input": "sumRange(2,5)", "output": "-1"},
        ],
        tags=["array", "prefix-sum"],
        comparison_strategy="exact",
        execution_model="class",
        function_name="RangeSumQuery",
        class_name="RangeSumQuery",
        method_name="sumRange",
    )
    
    test_cases = [
        TestCase(
            serial_number=0,
            test_input={
                "ctor_args": [[-2, 0, 3, -5, 2, -1]],
                "method": "sumRange",
                "method_args": [0, 2],
            },
            expected_output=1,
        ),
        TestCase(
            serial_number=1,
            test_input={
                "ctor_args": [[-2, 0, 3, -5, 2, -1]],
                "method": "sumRange",
                "method_args": [2, 5],
            },
            expected_output=-1,
        ),
        TestCase(
            serial_number=2,
            test_input={
                "ctor_args": [[-2, 0, 3, -5, 2, -1]],
                "method": "sumRange",
                "method_args": [0, 5],
            },
            expected_output=-3,
        ),
    ]
    
    solution = ProblemSolution(
        language="python",
        function_name="RangeSumQuery",
        code="""class RangeSumQuery:
    def __init__(self, nums):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]""",
        is_active=True,
        notes="Prefix sum approach",
    )
    
    problem.test_cases = test_cases
    problem.reference_solution = solution
    
    db.session.add(problem)
    db.session.commit()
    print(f"✓ Created class-based problem: {problem.slug}")


def create_tree_problem():
    """Example: Binary Tree Level Order Traversal - tree-based problem"""
    problem = Problem(
        slug="binary-tree-level-order",
        title="Binary Tree Level Order Traversal",
        difficulty="medium",
        description="Given the root of a binary tree, return the level order traversal of its nodes' values.",
        starter_code="def levelOrder(root):\n    pass",
        examples=[
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"},
        ],
        tags=["tree", "binary-tree", "bfs"],
        comparison_strategy="exact",
        execution_model="function",
        function_name="levelOrder",
    )
    
    test_cases = [
        TestCase(
            serial_number=0,
            test_input={
                "args": [[3, 9, 20, None, None, 15, 7]],
                "arg_types": ["tree"],
            },
            expected_output=[[3], [9, 20], [15, 7]],
        ),
        TestCase(
            serial_number=1,
            test_input={
                "args": [[1]],
                "arg_types": ["tree"],
            },
            expected_output=[[1]],
        ),
    ]
    
    solution = ProblemSolution(
        language="python",
        function_name="levelOrder",
        code="""def levelOrder(root):
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        level = []
        next_queue = []
        for node in queue:
            level.append(node.val)
            if node.left:
                next_queue.append(node.left)
            if node.right:
                next_queue.append(node.right)
        result.append(level)
        queue = next_queue
    return result""",
        is_active=True,
        notes="BFS approach",
    )
    
    problem.test_cases = test_cases
    problem.reference_solution = solution
    
    db.session.add(problem)
    db.session.commit()
    print(f"✓ Created tree-based problem: {problem.slug}")


if __name__ == "__main__":
    with app.app_context():
        try:
            create_function_problem()
            create_class_problem()
            create_tree_problem()
            print("\n✓ All problems created successfully!")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            db.session.rollback()
            sys.exit(1)
