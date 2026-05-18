# Execution Strategy System - Complete Guide

## Overview

The pypycode platform now uses a **Strategy Pattern** for executing different types of coding problems. This makes adding new problem types easy and keeps the codebase maintainable.

## Architecture

### 1. Problem Types

Problems are classified by their `execution_model`:

| Model | Description | Example |
|-------|-------------|---------|
| `function` | User implements a single function | Two Sum, Binary Search |
| `class` | User implements a class with methods | Range Sum Query, LRU Cache |
| `stateful` | Multiple operations on same object | (Future) |

### 2. Database Schema

#### Problem Model
```python
class Problem(db.Model):
    # ... existing fields ...
    execution_model = db.Column(db.String(32), default="function")
    function_name = db.Column(db.String(128), default="solution")
    class_name = db.Column(db.String(128), nullable=True)
    method_name = db.Column(db.String(128), nullable=True)
```

#### TestCase Model
```python
class TestCase(db.Model):
    # ... existing fields ...
    test_input = db.Column(db.JSON)  # Structured input
    expected_output = db.Column(db.JSON)  # Actual value
    comparison_strategy = db.Column(db.String(32), nullable=True)
```

### 3. Test Input Format

#### Function-Based
```json
{
  "args": [2, 7, 11, 15, 9],
  "kwargs": {}
}
```

#### Class-Based
```json
{
  "ctor_args": [[-2, 0, 3, -5, 2, -1]],
  "method": "sumRange",
  "method_args": [0, 2]
}
```

#### Stateful (Future)
```json
{
  "ctor_args": [...],
  "operations": [
    {"method": "put", "args": [1, 1]},
    {"method": "get", "args": [1]}
  ]
}
```

## Creating Problems

### Using the Helper Script

```bash
cd backend
python create_problems.py
```

This creates example problems for each type.

### Manual Creation

```python
from app import db
from app.models import Problem, TestCase, ProblemSolution

# Create function-based problem
problem = Problem(
    slug="two-sum",
    title="Two Sum",
    execution_model="function",
    function_name="solution",
    # ... other fields ...
)

test_cases = [
    TestCase(
        serial_number=0,
        test_input={"args": [[2, 7, 11, 15], 9]},
        expected_output=[0, 1],
    ),
]

problem.test_cases = test_cases
db.session.add(problem)
db.session.commit()
```

### Class-Based Problem

```python
problem = Problem(
    slug="range-sum-query",
    title="Range Sum Query",
    execution_model="class",
    function_name="RangeSumQuery",
    class_name="RangeSumQuery",
    method_name="sumRange",
    # ... other fields ...
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
]

problem.test_cases = test_cases
db.session.add(problem)
db.session.commit()
```

## Execution Flow

### 1. Backend (runner.py)

```
Problem → _convert_test_cases() → structured test cases
        ↓
    _build_problem_definition()
        ↓
    Docker sandbox with JSON payload
```

**Key function:**
```python
def _convert_test_cases(problem: Problem):
    converted_test_cases = []
    for tc in problem.test_cases:
        test_case = dict(tc.test_input)
        test_case["expected"] = tc.expected_output
        converted_test_cases.append(test_case)
    return converted_test_cases
```

### 2. Sandbox (test_runner.py)

```
problem_definition
        ↓
    get_strategy(execution_model)
        ↓
    strategy.execute(fn, test_case, namespace)
        ↓
    compare_fn(got, expected)
        ↓
    TestResult
```

**Key code:**
```python
execution_model = problem.get("execution_model", "function")
execution_strategy = get_strategy(execution_model)

for tc in test_cases:
    got = execution_strategy.execute(fn, tc, namespace)
    passed = compare_fn(got, tc["expected"])
```

## Adding New Problem Types

### Step 1: Create Strategy Class

In `sandbox/execution_strategies.py`:

```python
class MyCustomStrategy(ExecutionStrategy):
    def execute(self, fn, test_case, namespace):
        # Your execution logic here
        return result

STRATEGIES["my_custom"] = MyCustomStrategy()
```

### Step 2: Update Problem Model

Add fields to `Problem` model if needed:

```python
my_custom_field = db.Column(db.String(128), nullable=True)
```

### Step 3: Create Test Cases

Use appropriate `test_input` format for your strategy.

### Step 4: Test

```python
problem = Problem(
    execution_model="my_custom",
    # ... other fields ...
)
```

## Comparison Strategies

The system supports multiple comparison strategies:

- `exact`: Exact match (default)
- `unordered`: Order-independent list comparison
- `unordered_nested`: Order-independent nested list comparison
- `float`: Float comparison with tolerance
- `set`: Set comparison

Set per-problem or per-test-case:

```python
# Per-problem
problem.comparison_strategy = "unordered"

# Per-test-case (overrides problem setting)
test_case.comparison_strategy = "float"
```

## Special Features

### Tree/Linked-List Support

For problems using prebuilt structures:

```python
test_input = {
    "args": [[3, 9, 20, None, None, 15, 7]],
    "arg_types": ["tree"]
}
```

The `prelude` flag automatically includes helper classes:
- `ListNode`
- `TreeNode`
- Conversion functions: `list_to_tree()`, `list_to_linked()`, etc.

### Output Normalization

The `_normalize()` function handles:
- Linked lists → Python lists
- Trees → Python lists (level-order)
- Nested structures
- Fallback for arbitrary objects (repr)

## Testing

Run the test suite:

```bash
cd backend
python test_execution.py
```

Expected output:
```
SUMMARY:
  Function-based: ✓ PASS
  Class-based: ✓ PASS
```

## Migration Notes

### From Old System

Old format (string-based):
```
input: "[-2,0,3,-5,2,-1]; sumRange(0,2)"
expected_output: "1"
```

New format (structured):
```json
test_input: {
  "ctor_args": [[-2, 0, 3, -5, 2, -1]],
  "method": "sumRange",
  "method_args": [0, 2]
}
expected_output: 1
```

**Migration script:** `backend/migrations/versions/016_refactor_execution_model.py`

## Troubleshooting

### Problem: "Function 'X' not found"
- Check `function_name` matches user's code
- Verify `execution_model` is correct

### Problem: "Object of type X is not JSON serializable"
- Ensure `_normalize()` handles your return type
- Add custom normalization if needed

### Problem: Test cases not executing
- Verify `is_active=True` on TestCase
- Check `test_input` format matches execution_model
- Ensure `expected_output` is valid JSON

## Performance

- **Sandbox timeout**: 4 seconds per problem
- **Memory limit**: 200MB
- **CPU quota**: 0.5 CPU
- **File descriptors**: 64

Adjust in `backend/app/services/runner.py` and `sandbox/runner.py`.

## Future Enhancements

1. **Stateful Strategy**: Multiple operations on same object
2. **Interactive Strategy**: Real-time I/O testing
3. **Custom Validators**: Problem-specific validation logic
4. **Performance Profiling**: Runtime/memory tracking
5. **Parallel Test Execution**: Run tests concurrently
