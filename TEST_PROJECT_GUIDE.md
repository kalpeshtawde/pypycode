# Test Project Guide

## Quick Start

A test project has been created with 6 problems to verify the new execution strategy system.

### Login Credentials
```
Email: testuser@example.com
Password: test1234
```

### Project Details
- **Name:** Test Project
- **ID:** b2176ec9-aa3f-4131-868b-6b977ad147f4
- **Problems:** 6 (mix of function-based and class-based)

---

## Problems in Test Project

### 1. **Add Two Numbers** (Function-based, Easy)
- **Slug:** `add-two-numbers`
- **Task:** Given two integers, return their sum
- **Test Cases:** 4
- **Expected:** All should pass with simple addition

**Sample Solution:**
```python
def solution(a, b):
    return a + b
```

---

### 2. **Reverse String** (Function-based, Medium)
- **Slug:** `reverse-string`
- **Task:** Given a string, return it reversed
- **Test Cases:** 4
- **Expected:** All should pass with string slicing

**Sample Solution:**
```python
def solution(s):
    return s[::-1]
```

---

### 3. **Simple Counter** (Class-based, Easy)
- **Slug:** `counter-class`
- **Task:** Implement a Counter class with increment() and get() methods
- **Test Cases:** 3
- **Expected:** Tests increment and retrieve counter value

**Sample Solution:**
```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def get(self):
        return self.count
```

---

### 4. **Range Sum Query** (Class-based, Medium)
- **Slug:** `range-sum-immutable`
- **Task:** Implement NumArray class with efficient range sum queries
- **Test Cases:** 3
- **Expected:** Uses prefix sum optimization

**Sample Solution:**
```python
class NumArray:
    def __init__(self, nums):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]
```

---

### 5. **Find Maximum** (Function-based, Easy)
- **Slug:** `find-max`
- **Task:** Given an array, return the maximum value
- **Test Cases:** 4
- **Expected:** All should pass with max() function

**Sample Solution:**
```python
def solution(nums):
    return max(nums)
```

---

### 6. **Two Sum** (Function-based, Medium)
- **Slug:** `two-sum-test`
- **Task:** Find indices of two numbers that add up to target
- **Test Cases:** 4
- **Expected:** Uses hash map for O(n) solution

**Sample Solution:**
```python
def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

---

## Testing Checklist

### Function-Based Problems
- [ ] Add Two Numbers - Test with positive, negative, zero values
- [ ] Reverse String - Test with empty, single char, palindrome
- [ ] Find Maximum - Test with positive, negative, single element
- [ ] Two Sum - Test with duplicates, different orderings

### Class-Based Problems
- [ ] Simple Counter - Test increment and get operations
- [ ] Range Sum Query - Test different ranges, edge cases

### Expected Results
- ✅ All test cases should pass with correct solutions
- ✅ Wrong solutions should fail with clear error messages
- ✅ Class instantiation should work correctly
- ✅ Method calls should execute properly

---

## Testing Scenarios

### Scenario 1: Correct Solution
1. Select "Add Two Numbers"
2. Enter the sample solution
3. Click "Run"
4. **Expected:** Status = "accepted", 4/4 tests pass

### Scenario 2: Incorrect Solution
1. Select "Two Sum"
2. Enter a wrong solution (e.g., just return [0, 1])
3. Click "Run"
4. **Expected:** Status = "wrong_answer", some tests fail

### Scenario 3: Class-Based Problem
1. Select "Simple Counter"
2. Enter the sample solution
3. Click "Run"
4. **Expected:** Status = "accepted", 3/3 tests pass

### Scenario 4: Syntax Error
1. Select any problem
2. Enter invalid Python code
3. Click "Run"
4. **Expected:** Status = "runtime_error", compile error message

### Scenario 5: Runtime Error
1. Select "Find Maximum"
2. Enter: `def solution(nums): return nums[10]`
3. Click "Run"
4. **Expected:** Status = "runtime_error", index out of range error

---

## Debugging Tips

### If tests don't pass:
1. Check the error message in the output
2. Verify the solution logic matches the problem description
3. Test edge cases (empty arrays, negative numbers, etc.)

### If class-based problem fails:
1. Ensure class name matches (e.g., `Counter`, `NumArray`)
2. Verify method names are correct
3. Check that __init__ properly initializes state

### If function-based problem fails:
1. Ensure function name is `solution`
2. Check parameter order matches test input
3. Verify return type matches expected output

---

## Performance Notes

- **Timeout:** 4 seconds per problem
- **Memory:** 200MB limit
- **CPU:** 0.5 CPU quota

All test problems should complete in < 100ms.

---

## Next Steps

After testing these problems:
1. Try creating your own problems
2. Test with different execution models
3. Add more complex test cases
4. Verify error handling

See `EXECUTION_STRATEGY_GUIDE.md` for detailed documentation on creating new problems.
