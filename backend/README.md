# PyPyCode Backend - Problem Management & Validation

This document describes the problem management system and validation tools available in the PyPyCode backend.

## Overview

The backend provides tools to:
- Create problems with test cases and solutions
- Validate test cases against solutions
- Manage problem metadata and execution models
- Support multiple problem types (function-based, class-based, etc.)

## Problem Structure

### Database Models

#### Problem
Stores problem metadata:
- `slug` - Unique identifier (e.g., "longest-common-prefix")
- `title` - Problem title
- `description` - Problem description
- `difficulty` - Level (easy, medium, hard)
- `execution_model` - Type of execution ("function" or "class")
- `function_name` - Name of the function to call (for function-based problems)
- `class_name` - Name of the class (for class-based problems)
- `method_name` - Name of the method to call (for class-based problems)
- `starter_code` - Template code for users
- `comparison_strategy` - How to compare outputs ("exact", "fuzzy", etc.)
- `examples` - Example input/output pairs
- `tags` - Problem tags for categorization

#### TestCase
Stores individual test cases:
- `problem_id` - Reference to Problem
- `serial_number` - Order of test case
- `test_input` - Input as JSONB: `{"args": [arg1, arg2, ...]}`
- `expected_output` - Expected output as JSONB (actual value, not string)
- `is_active` - Whether test case is active
- `comparison_strategy` - Override problem's comparison strategy (optional)

#### ProblemSolution
Stores solutions:
- `problem_id` - Reference to Problem
- `code` - The actual solution code
- `language` - Programming language (e.g., "python")
- `function_name` - Name of the function in the code
- `is_active` - Whether this is the active solution
- `notes` - Description of the approach

## Validation Script

### Purpose

The `validate_all_problems.py` script validates that all test cases are correct by:
1. Running each problem's solution against all its test cases
2. Comparing actual output with expected output
3. Reporting pass/fail status
4. Identifying invalid test cases

### Usage

**Validate all problems:**
```bash
python validate_all_problems.py
```

**Validate specific problem:**
```bash
python validate_all_problems.py --problem longest-common-prefix
```

### Output Example

```
================================================================================
PROBLEM VALIDATION REPORT
================================================================================

✓ longest-common-prefix: 10/10 tests passed
✓ two-sum: 5/5 tests passed
✗ island-counter: 2/3 tests passed
  Error: Expected [1, 2] but got [2, 1]...

================================================================================
SUMMARY
================================================================================
Total Problems: 3
✓ Passing: 2
✗ Failing: 1
⊘ No Solution: 0
================================================================================
```

### Exit Codes

- `0` - All problems passed validation
- `1` - One or more problems failed validation

## Creating Problems

### Manual Creation

Use the database directly or create a script following this pattern:

```python
from app import create_app, db
from app.models import Problem, TestCase, ProblemSolution

app = create_app()

with app.app_context():
    # Create problem
    problem = Problem(
        slug="my-problem",
        title="My Problem",
        difficulty="easy",
        description="Problem description...",
        starter_code="def solution(...):\n    pass",
        execution_model="function",
        function_name="solution",
        comparison_strategy="exact",
        examples=[{"input": "...", "output": "..."}],
        tags=["tag1", "tag2"]
    )
    db.session.add(problem)
    db.session.flush()
    
    # Add test cases
    for idx, (input_val, expected) in enumerate(test_cases):
        tc = TestCase(
            problem_id=problem.id,
            serial_number=idx,
            test_input={"args": [input_val]},  # Wrap args in list
            expected_output=expected,
            is_active=True
        )
        db.session.add(tc)
    
    # Add solution
    solution = ProblemSolution(
        problem_id=problem.id,
        code="def solution(...):\n    ...",
        language="python",
        function_name="solution",
        is_active=True,
        notes="Solution approach description"
    )
    db.session.add(solution)
    db.session.commit()
```

## Test Case Format

### Input Format

Test inputs are stored as JSONB with arguments wrapped in a list:

```json
{
  "args": [arg1, arg2, ...]
}
```

**Examples:**
- Single argument: `{"args": ["hello"]}`
- Multiple arguments: `{"args": [[1, 2, 3], 5]}`
- No arguments: `{"args": []}`

### Output Format

Expected outputs are stored as JSONB with actual values (not strings):

```json
"hello"          // String
42               // Number
[1, 2, 3]        // Array
true             // Boolean
null             // Null
```

**NOT:**
```json
"\"hello\""      // Don't quote strings
"42"             // Don't quote numbers
```

## Problem Types

### Function-Based Problems

For problems that call a single function:

```python
problem = Problem(
    execution_model="function",
    function_name="twoSum",
    class_name=None,
    method_name=None
)
```

Test case:
```json
{
  "args": [[2, 7, 11, 15], 9]
}
```

### Class-Based Problems

For problems that instantiate a class and call a method:

```python
problem = Problem(
    execution_model="class",
    class_name="RangeSumQuery",
    method_name="sumRange",
    function_name="RangeSumQuery"  # Keep for compatibility
)
```

Test case:
```json
{
  "args": [[-2, 0, 3, -5, 2, -1], 0, 2]
}
```

## Workflow: Adding New Problems

1. **Create problem metadata:**
   - Define slug, title, description
   - Set execution_model and function/class names
   - Add starter code and examples

2. **Add test cases:**
   - Create 3-10 test cases with various inputs
   - Ensure expected outputs are correct
   - Use proper JSONB format

3. **Create solution:**
   - Write working solution code
   - Ensure function/class names match problem definition

4. **Validate:**
   ```bash
   python validate_all_problems.py --problem my-problem
   ```

5. **Verify all tests pass:**
   - If any fail, fix the test case or solution
   - Re-run validation until all pass

## Common Issues

### "Function 'solution' not found"
**Cause:** Function name in solution doesn't match `Problem.function_name`

**Fix:** Ensure solution code has:
```python
def longestCommonPrefix(strs):  # Must match function_name
    ...
```

### "Expected X but got Y"
**Cause:** Test case expected output is wrong

**Fix:** Verify expected output is correct and in proper JSONB format

### "No active solution found"
**Cause:** Problem has no active solution

**Fix:** Create a ProblemSolution with `is_active=True`

### Test input format errors
**Cause:** Test input not in proper JSONB format

**Fix:** Ensure test_input is: `{"args": [arg1, arg2, ...]}`

## Database Schema

### test_cases table columns
- `id` - UUID primary key
- `problem_id` - Foreign key to problems
- `serial_number` - Test case order (0-indexed)
- `test_input` - JSONB with args
- `expected_output` - JSONB with expected value
- `comparison_strategy` - Optional override
- `is_active` - Boolean flag
- `created_at` - Timestamp

**Note:** The legacy `function` column is deprecated and no longer used.

## Performance Considerations

- Validation runs sequentially (one problem at a time)
- Each test case runs in a Docker sandbox
- Typical validation time: 1-2 seconds per problem
- For 100+ problems, expect 2-3 minutes total

## Future Enhancements

- [ ] Parallel test execution
- [ ] Performance profiling (runtime/memory)
- [ ] Custom validators for complex outputs
- [ ] Test case generation from examples
- [ ] Bulk import from CSV
