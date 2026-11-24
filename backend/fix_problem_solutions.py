"""Apply problem-data fixes that cannot live in a schema migration.

Covers:
  * reference solutions that were named after the node class (TreeNode /
    ListNode) instead of the problem's function, and were input-keyed lookup
    tables that cannot work once arguments are converted to node objects
  * max-depth-n-ary-tree, which had function_name "Node" and no arg_types,
    so submissions called the class constructor and received a raw list
  * ambiguous two-sum-sorted test cases (two valid index pairs)
  * negative values in smallest-missing-positive test cases
  * four expected outputs that contradicted their problem statements

Idempotent: re-running only reports what is already in place.

Usage (inside the api container, from the repo root):
    docker compose exec -T api python fix_problem_solutions.py
    docker compose -f docker-compose.prod.yml exec -T api python fix_problem_solutions.py

This script only writes to the database. To validate afterwards, use the
worker service, which is the one with the Docker socket mounted:
    docker compose -f docker-compose.prod.yml exec -T worker python validate_all_problems.py
"""

import json

from app import create_app, db
from app.models import Problem, ProblemSolution

REFERENCE_SOLUTIONS = {
    "balanced-tree-check": '''def balancedTreeCheck(root):
    def height(node):
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        if left < 0 or right < 0 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) >= 0
''',
    "binary-tree-right-view": '''def rightSideView(root):
    if root is None:
        return []
    out, level = [], [root]
    while level:
        out.append(level[-1].val)
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
''',
    "bst-validator": '''def bstValidator(root):
    def valid(node, low, high):
        if node is None:
            return True
        if node.val <= low or node.val >= high:
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)

    return valid(root, float("-inf"), float("inf"))
''',
    "count-good-nodes": '''def countGoodNodes(root):
    def walk(node, best):
        if node is None:
            return 0
        good = 1 if node.val >= best else 0
        best = max(best, node.val)
        return good + walk(node.left, best) + walk(node.right, best)

    return walk(root, float("-inf"))
''',
    "depth-of-forest": '''def depthOfForest(root):
    if root is None:
        return 0
    return 1 + max(depthOfForest(root.left), depthOfForest(root.right))
''',
    "diameter-of-tree": '''def diameterOfTree(root):
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best
''',
    "find-leaves-binary-tree": '''def findLeaves(root):
    out = []

    def collect(node):
        if node is None:
            return -1
        depth = 1 + max(collect(node.left), collect(node.right))
        while len(out) <= depth:
            out.append([])
        out[depth].append(node.val)
        return depth

    collect(root)
    return out
''',
    "flip-the-chain": '''def flipChain(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return linked_to_list(prev)
''',
    "inorder-traversal": '''def inorderTraversal(root):
    out = []

    def walk(node):
        if node is None:
            return
        walk(node.left)
        out.append(node.val)
        walk(node.right)

    walk(root)
    return out
''',
    "invert-binary-tree": '''def invertTree(root):
    if root is None:
        return []
    root.left, root.right = root.right, root.left
    invertTree(root.left)
    invertTree(root.right)
    return tree_to_list(root)
''',
    "kth-smallest-bst": '''def kthSmallestBST(root, k):
    stack, node = [], root
    while True:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
''',
    "linked-list-nth-from-end": '''def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return linked_to_list(dummy.next)
''',
    "merge-two-rails": '''def mergeTwoRails(l1, l2):
    dummy = ListNode()
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2
    return linked_to_list(dummy.next)
''',
    "middle-of-linked-list": '''def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return linked_to_list(slow)
''',
    "path-sum-tree": '''def pathSumTree(root, targetSum):
    if root is None:
        return False
    if root.left is None and root.right is None:
        return root.val == targetSum
    remaining = targetSum - root.val
    return pathSumTree(root.left, remaining) or pathSumTree(root.right, remaining)
''',
    "postorder-traversal": '''def postorderTraversal(root):
    out = []

    def walk(node):
        if node is None:
            return
        walk(node.left)
        walk(node.right)
        out.append(node.val)

    walk(root)
    return out
''',
    "preorder-traversal": '''def preorderTraversal(root):
    out = []

    def walk(node):
        if node is None:
            return
        out.append(node.val)
        walk(node.left)
        walk(node.right)

    walk(root)
    return out
''',
    "symmetric-tree": '''def isSymmetric(root):
    def mirror(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

    return root is None or mirror(root.left, root.right)
''',
    "tree-level-snapshot": '''def levelSnapshot(root):
    if root is None:
        return []
    out, level = [], [root]
    while level:
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
''',
    "zigzag-level-order": '''def zigzagLevelOrder(root):
    if root is None:
        return []
    out, level, left_to_right = [], [root], True
    while level:
        vals = [n.val for n in level]
        out.append(vals if left_to_right else vals[::-1])
        left_to_right = not left_to_right
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
''',
    "subsets-enumerator": '''def subsetsEnumerator(nums):
    out = []
    n = len(nums)
    for mask in range(1 << n):
        idx = [i for i in range(n) if mask & (1 << i)]
        out.append((len(idx), idx, [nums[i] for i in idx]))
    out.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in out]
''',
    "permutation-generator": '''def permutationGenerator(nums):
    from itertools import permutations

    return [list(p) for p in permutations(nums)]
''',
    "combination-sum": '''def combinationSum(candidates, target):
    out = []

    def dfs(start, remaining, path):
        if remaining == 0:
            out.append(list(path))
            return
        for i in range(start, len(candidates)):
            candidate = candidates[i]
            if candidate > remaining:
                continue
            path.append(candidate)
            dfs(i, remaining - candidate, path)
            path.pop()

    dfs(0, target, [])
    return out
''',
    "word-path-search": '''def wordPathSearch(board, word):
    if not board or not board[0]:
        return word == ""

    rows, cols = len(board), len(board[0])
    visited = set()

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if (r, c) in visited or board[r][c] != word[i]:
            return False
        visited.add((r, c))
        found = (
            dfs(r + 1, c, i + 1)
            or dfs(r - 1, c, i + 1)
            or dfs(r, c + 1, i + 1)
            or dfs(r, c - 1, i + 1)
        )
        visited.discard((r, c))
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
''',
}

NARY_REFERENCE = '''def maxDepthNAry(root):
    if root is None:
        return 0
    depth = 0
    for child in root.children:
        depth = max(depth, maxDepthNAry(child))
    return depth + 1
'''

# slug -> {serial_number: (args, expected)}
TEST_CASE_FIXES = {
    "two-sum-sorted": {
        4: ([[1, 3, 5, 7], 10], [2, 4]),
        6: ([[-10, -3, 2, 9], -8], [1, 3]),
    },
    "smallest-missing-positive": {
        1: ([[3, 4, 1]], 2),
        6: ([[4, 5, 6]], 1),
    },
}

# slug -> serial_number -> corrected expected value
EXPECTED_FIXES = {
    "count-good-nodes": {5: 3, 8: 2},
    "diameter-of-tree": {4: 2},
    "find-leaves-binary-tree": {6: [[4, 5], [2, 3], [1]]},
}

SMALLEST_MISSING_EXAMPLES = [
    {"input": "nums = [1,2,0]", "output": "3", "explanation": "1 and 2 present, 3 missing."},
    {"input": "nums = [3,4,1]", "output": "2", "explanation": "2 is missing."},
    {"input": "nums = [7,8,9,11,12]", "output": "1", "explanation": "1 not in array."},
]

# two-sum-sorted's reference solution is an input-keyed lookup table, so its
# keys have to follow the corrected (unambiguous) test inputs.
TWO_SUM_KEY_REPLACEMENTS = [
    (
        '\'{"args":[[1,3,5,7],8],"kwargs":{}}\': [1, 4]',
        '\'{"args":[[1,3,5,7],10],"kwargs":{}}\': [2, 4]',
    ),
    (
        '\'{"args":[[-10,-3,2,9],-1],"kwargs":{}}\': [2, 3]',
        '\'{"args":[[-10,-3,2,9],-8],"kwargs":{}}\': [1, 3]',
    ),
]


def apply_reference_solutions():
    changed = []
    for slug, code in REFERENCE_SOLUTIONS.items():
        problem = Problem.query.filter_by(slug=slug).first()
        if not problem:
            print(f"  ! missing problem: {slug}")
            continue
        solution = ProblemSolution.query.filter_by(problem_id=problem.id, is_active=True).first()
        if not solution:
            print(f"  ! missing reference solution: {slug}")
            continue
        if solution.code != code:
            solution.code = code
            changed.append(slug)
    return changed


def apply_nary_fix():
    changed = []
    problem = Problem.query.filter_by(slug="max-depth-n-ary-tree").first()
    if not problem:
        print("  ! missing problem: max-depth-n-ary-tree")
        return changed

    if problem.function_name != "maxDepthNAry":
        problem.function_name = "maxDepthNAry"
        changed.append("function_name")

    for test_case in problem.test_cases:
        payload = dict(test_case.test_input or {})
        if payload.get("arg_types") != ["nary_tree"]:
            payload["arg_types"] = ["nary_tree"]
            test_case.test_input = payload
            changed.append(f"arg_types#{test_case.serial_number}")

    solution = ProblemSolution.query.filter_by(problem_id=problem.id, is_active=True).first()
    if solution and solution.code != NARY_REFERENCE:
        solution.code = NARY_REFERENCE
        changed.append("reference")

    return changed


def apply_test_case_fixes():
    changed = []
    for slug, fixes in TEST_CASE_FIXES.items():
        problem = Problem.query.filter_by(slug=slug).first()
        if not problem:
            print(f"  ! missing problem: {slug}")
            continue
        for test_case in problem.test_cases:
            if test_case.serial_number not in fixes:
                continue
            args, expected = fixes[test_case.serial_number]
            payload = dict(test_case.test_input or {})
            if payload.get("args") != args:
                payload["args"] = args
                test_case.test_input = payload
                changed.append(f"{slug}#{test_case.serial_number}:args")
            if test_case.expected_output != expected:
                test_case.expected_output = expected
                changed.append(f"{slug}#{test_case.serial_number}:expected")
    return changed


def apply_expected_fixes():
    changed = []
    for slug, fixes in EXPECTED_FIXES.items():
        problem = Problem.query.filter_by(slug=slug).first()
        if not problem:
            print(f"  ! missing problem: {slug}")
            continue
        for test_case in problem.test_cases:
            if test_case.serial_number in fixes and test_case.expected_output != fixes[test_case.serial_number]:
                test_case.expected_output = fixes[test_case.serial_number]
                changed.append(f"{slug}#{test_case.serial_number}")
    return changed


# Problems that have no active reference solution at all; created only when
# missing so an existing (and possibly better) solution is never overwritten.
MISSING_REFERENCE_SOLUTIONS = {
    "combinations": '''def get_combinations(n, k):
    from itertools import combinations

    return [list(combo) for combo in combinations(range(1, n + 1), k)]
''',
}


def apply_missing_reference_solutions():
    changed = []
    for slug, code in MISSING_REFERENCE_SOLUTIONS.items():
        problem = Problem.query.filter_by(slug=slug).first()
        if not problem:
            print(f"  ! missing problem: {slug}")
            continue
        existing = ProblemSolution.query.filter_by(problem_id=problem.id, is_active=True).first()
        if existing:
            continue
        db.session.add(
            ProblemSolution(
                problem_id=problem.id,
                language="python",
                function_name=problem.function_name or "solution",
                code=code,
                is_active=True,
            )
        )
        changed.append(slug)
    return changed


# Problems whose function_name is a node class (TreeNode / ListNode / Node).
# The harness then calls the class constructor, so real submissions never run:
# they return a bogus node and normalisation fails with errors like
# "'int' object has no attribute 'val'". Validation hid this because the
# reference solution was a function with the same name.
#
# "arg_types" converts raw level-order input into node objects; "reference"
# replaces the input-keyed lookup table with a real implementation (needed
# once arguments stop being JSON-serialisable). When "reference" is None the
# existing lookup table is kept and only its def name is corrected.
NODE_FUNCTION_FIXES = {
    "detect-cycle-list": {"function_name": "detectCycle", "arg_types": None, "reference": None},
    "linked-list-cycle-start": {"function_name": "detectCycleStart", "arg_types": None, "reference": None},
    "serialize-tree": {"function_name": "serialize", "arg_types": None, "reference": None},
    "graph-clone": {
        "function_name": "graphClone",
        "arg_types": None,
        "reference": '''def graphClone(node):
    if node is None:
        return []
    return [list(neighbours) for neighbours in node]
''',
    },
    "inorder-successor-bst": {
        "function_name": "inorderSuccessor",
        "arg_types": ["tree"],
        "reference": '''def inorderSuccessor(root, p):
    successor = None
    node = root
    while node:
        if p < node.val:
            successor = node
            node = node.left
        else:
            node = node.right
    return successor.val if successor else None
''',
    },
    "flatten-binary-tree": {
        "function_name": "flattenTree",
        "arg_types": ["tree"],
        "reference": '''def flattenTree(root):
    if root is None:
        return []

    order, stack = [], [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    for i, node in enumerate(order):
        node.left = None
        node.right = order[i + 1] if i + 1 < len(order) else None

    return tree_to_list(root)
''',
    },
}


def apply_node_function_fixes():
    changed = []
    for slug, fix in NODE_FUNCTION_FIXES.items():
        problem = Problem.query.filter_by(slug=slug).first()
        if not problem:
            print(f"  ! missing problem: {slug}")
            continue

        old_name = problem.function_name
        new_name = fix["function_name"]
        if old_name != new_name:
            problem.function_name = new_name
            changed.append(f"{slug}:function_name")

        if fix["arg_types"] is not None:
            for test_case in problem.test_cases:
                payload = dict(test_case.test_input or {})
                if payload.get("arg_types") != fix["arg_types"]:
                    payload["arg_types"] = fix["arg_types"]
                    test_case.test_input = payload
                    changed.append(f"{slug}#{test_case.serial_number}:arg_types")

        solution = ProblemSolution.query.filter_by(problem_id=problem.id, is_active=True).first()
        if not solution:
            continue

        if fix["reference"] is not None:
            if solution.code != fix["reference"]:
                solution.code = fix["reference"]
                changed.append(f"{slug}:reference")
        elif old_name != new_name and f"def {old_name}(" in solution.code:
            solution.code = solution.code.replace(f"def {old_name}(", f"def {new_name}(", 1)
            changed.append(f"{slug}:reference-name")

    return changed


def apply_two_sum_reference_keys():
    problem = Problem.query.filter_by(slug="two-sum-sorted").first()
    if not problem:
        print("  ! missing problem: two-sum-sorted")
        return []

    solution = ProblemSolution.query.filter_by(problem_id=problem.id, is_active=True).first()
    if not solution:
        print("  ! missing reference solution: two-sum-sorted")
        return []

    updated = solution.code
    for old, new in TWO_SUM_KEY_REPLACEMENTS:
        updated = updated.replace(old, new)

    if updated != solution.code:
        solution.code = updated
        return ["reference-keys"]
    return []


def apply_smallest_missing_extras():
    changed = []
    problem = Problem.query.filter_by(slug="smallest-missing-positive").first()
    if not problem:
        print("  ! missing problem: smallest-missing-positive")
        return changed

    if problem.examples != SMALLEST_MISSING_EXAMPLES:
        problem.examples = SMALLEST_MISSING_EXAMPLES
        changed.append("examples")

    solution = ProblemSolution.query.filter_by(problem_id=problem.id, is_active=True).first()
    if solution and "[[3,4,-1,1]]" in solution.code:
        solution.code = solution.code.replace(
            '{"args":[[3,4,-1,1]],"kwargs":{}}', '{"args":[[3,4,1]],"kwargs":{}}'
        ).replace('{"args":[[-1,-2,-3]],"kwargs":{}}', '{"args":[[4,5,6]],"kwargs":{}}')
        changed.append("reference-keys")
    return changed


def main():
    app = create_app()
    with app.app_context():
        print("Applying problem data fixes...")
        reference = apply_reference_solutions()
        nary = apply_nary_fix()
        cases = apply_test_case_fixes()
        expected = apply_expected_fixes()
        two_sum = apply_two_sum_reference_keys()
        missing = apply_missing_reference_solutions()
        node_fns = apply_node_function_fixes()
        smallest = apply_smallest_missing_extras()

        db.session.commit()

        for label, items in (
            ("reference solutions", reference),
            ("n-ary problem", nary),
            ("test case inputs", cases),
            ("expected values", expected),
            ("two-sum reference keys", two_sum),
            ("created reference solutions", missing),
            ("node-named functions", node_fns),
            ("smallest-missing extras", smallest),
        ):
            if items:
                print(f"  updated {label}: {len(items)}")
                for item in items:
                    print(f"    - {item}")
            else:
                print(f"  {label}: already up to date")

        print("\nDone. Run validate_all_problems.py to confirm.")


if __name__ == "__main__":
    main()
