import math
import copy
import traceback
from typing import Any


PRELUDE = """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals, node = [], self
        while node:
            vals.append(str(node.val))
            node = node.next
        return "->".join(vals)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"



def list_to_linked(lst):
    if not lst:
        return None
    head = ListNode(lst[0])
    cur = head
    for val in lst[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head



def linked_to_list(node):
    result, seen = [], set()
    while node:
        if id(node) in seen:
            result.append("...")
            break
        seen.add(id(node))
        result.append(node.val)
        node = node.next
    return result



def list_to_tree(lst):
    if not lst or lst[0] is None:
        return None
    root = TreeNode(lst[0])
    queue = [root]
    i = 1
    while queue and i < len(lst):
        node = queue.pop(0)
        if i < len(lst) and lst[i] is not None:
            node.left = TreeNode(lst[i])
            queue.append(node.left)
        i += 1
        if i < len(lst) and lst[i] is not None:
            node.right = TreeNode(lst[i])
            queue.append(node.right)
        i += 1
    return root



def tree_to_list(root):
    if not root:
        return []
    result, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result
"""



def _linked_to_list_safe(node):
    result, seen = [], set()
    while node:
        if id(node) in seen:
            result.append("...")
            break
        seen.add(id(node))
        result.append(node.val)
        node = node.next
    return result



def _tree_to_list_safe(root):
    if not root:
        return []
    result, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result



def _normalize(val: Any) -> Any:
    if val is None:
        return None
    if hasattr(val, "val") and hasattr(val, "next") and not hasattr(val, "left"):
        return _linked_to_list_safe(val)
    if hasattr(val, "val") and hasattr(val, "left") and hasattr(val, "right"):
        return _tree_to_list_safe(val)
    if isinstance(val, list):
        return [_normalize(v) for v in val]
    if isinstance(val, tuple):
        return tuple(_normalize(v) for v in val)
    if isinstance(val, dict):
        return {k: _normalize(v) for k, v in val.items()}
    return val



def compare_exact(got: Any, expected: Any) -> bool:
    return _normalize(got) == _normalize(expected)



def compare_unordered(got: Any, expected: Any) -> bool:
    g, e = _normalize(got), _normalize(expected)
    if not isinstance(g, list) or not isinstance(e, list):
        return g == e
    return sorted(g, key=str) == sorted(e, key=str)



def compare_unordered_nested(got: Any, expected: Any) -> bool:
    g, e = _normalize(got), _normalize(expected)
    if not isinstance(g, list) or not isinstance(e, list):
        return g == e

    sort_inner = lambda x: sorted(x, key=str) if isinstance(x, list) else x
    return sorted([sort_inner(r) for r in g], key=str) == sorted([sort_inner(r) for r in e], key=str)



def compare_float(got: Any, expected: Any, tol: float = 1e-5) -> bool:
    try:
        return math.isclose(float(got), float(expected), rel_tol=tol, abs_tol=tol)
    except (TypeError, ValueError):
        return False



def compare_set(got: Any, expected: Any) -> bool:
    g, e = _normalize(got), _normalize(expected)
    try:
        return set(g) == set(e)
    except TypeError:
        return g == e


COMPARISON_STRATEGIES = {
    "exact": compare_exact,
    "unordered": compare_unordered,
    "unordered_nested": compare_unordered_nested,
    "float": compare_float,
    "set": compare_set,
}


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.cases: list[dict] = []
        self.compile_error: str | None = None
        self.runtime_error: str | None = None

    @property
    def all_passed(self) -> bool:
        return self.compile_error is None and self.runtime_error is None and self.failed == 0

    def to_dict(self) -> dict:
        return {
            "all_passed": self.all_passed,
            "passed": self.passed,
            "failed": self.failed,
            "total": self.total,
            "compile_error": self.compile_error,
            "runtime_error": self.runtime_error,
            "cases": self.cases,
        }



def _convert_args(args: list, arg_types: list, namespace: dict) -> list:
    if not arg_types:
        return args

    converted = []
    list_to_linked = namespace.get("list_to_linked")
    list_to_tree = namespace.get("list_to_tree")

    for arg, atype in zip(args, arg_types + [None] * len(args)):
        if atype == "linked_list" and list_to_linked:
            converted.append(list_to_linked(arg))
        elif atype == "tree" and list_to_tree:
            converted.append(list_to_tree(arg))
        else:
            converted.append(arg)
    return converted



def run_tests(user_code: str, problem: dict) -> TestResult:
    result = TestResult()

    namespace: dict[str, Any] = {}
    if problem.get("prelude", False):
        try:
            exec(compile(PRELUDE, "<prelude>", "exec"), namespace)
        except Exception as e:
            result.compile_error = f"Internal prelude error: {e}"
            return result

    try:
        compiled = compile(user_code, "<user_code>", "exec")
    except SyntaxError as e:
        result.compile_error = f"SyntaxError on line {e.lineno}: {e.msg}"
        return result

    try:
        exec(compiled, namespace)
    except Exception:
        result.compile_error = traceback.format_exc()
        return result

    fn_name = problem.get("function_name", "solution")
    fn = namespace.get(fn_name)
    if fn is None or not callable(fn):
        result.compile_error = (
            f"Function '{fn_name}' not found. "
            f"Make sure you define 'def {fn_name}(...)' in your solution."
        )
        return result

    strategy_name = problem.get("comparison", "exact")
    compare_fn = COMPARISON_STRATEGIES.get(strategy_name, compare_exact)

    test_cases = problem.get("test_cases", [])
    result.total = len(test_cases)

    for i, tc in enumerate(test_cases):
        case_report: dict[str, Any] = {
            "case": i + 1,
            "passed": False,
            "input": tc.get("args", []),
            "expected": tc.get("expected"),
            "got": None,
            "error": None,
        }

        args = copy.deepcopy(tc.get("args", []))
        kwargs = copy.deepcopy(tc.get("kwargs", {}))
        args = _convert_args(args, tc.get("arg_types", []), namespace)

        try:
            got = fn(*args, **kwargs)
            passed = compare_fn(got, tc["expected"])
            case_report["got"] = _normalize(got)
            case_report["passed"] = passed
            if passed:
                result.passed += 1
            else:
                result.failed += 1
        except Exception:
            case_report["error"] = traceback.format_exc()
            case_report["passed"] = False
            result.failed += 1

        result.cases.append(case_report)

    return result
