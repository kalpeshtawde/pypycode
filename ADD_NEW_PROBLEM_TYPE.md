# How to Add a New Problem Type

This guide shows how to add a new execution strategy for a different problem type.

## Example: Adding "Stateful" Strategy

Stateful problems involve multiple operations on the same object instance.

### Step 1: Create the Strategy Class

**File:** `sandbox/execution_strategies.py`

Add to the file:

```python
class StatefulStrategy(ExecutionStrategy):
    """For problems with multiple operations on same state.
    
    Test input format:
    {
        "ctor_args": [...],
        "operations": [
            {"method": "put", "args": [1, 1]},
            {"method": "get", "args": [1]},
            {"method": "get", "args": [2]}
        ]
    }
    
    The last operation's return value is compared to expected_output.
    """
    def execute(self, fn, test_case, namespace):
        ctor_args = test_case.get("ctor_args", [])
        operations = test_case.get("operations", [])
        
        # Create instance
        instance = fn(*ctor_args)
        
        # Execute all operations
        result = None
        for op in operations:
            method_name = op.get("method")
            method_args = op.get("args", [])
            method = getattr(instance, method_name)
            result = method(*method_args)
        
        return result

# Register the strategy
STRATEGIES["stateful"] = StatefulStrategy()
```

### Step 2: Update the Problem Model

**File:** `backend/app/models/__init__.py`

If your strategy needs additional fields, add them to the Problem model:

```python
class Problem(db.Model):
    # ... existing fields ...
    
    # For stateful problems, track which method returns the final result
    final_method = db.Column(db.String(128), nullable=True)
```

Create a migration:

```bash
cd backend
python -m flask db migrate -m "add final_method to problems"
python -m flask db upgrade
```

### Step 3: Create Example Problem

**File:** `backend/create_problems.py`

Add a function to create an example:

```python
def create_stateful_problem():
    """Example: LRU Cache - stateful problem"""
    problem = Problem(
        slug="lru-cache",
        title="LRU Cache",
        difficulty="medium",
        description="Design and implement an LRU (Least Recently Used) cache.",
        starter_code="""class LRUCache:
    def __init__(self, capacity):
        pass
    
    def get(self, key):
        pass
    
    def put(self, key, value):
        pass""",
        examples=[
            {"input": "LRUCache(2); put(1,1); put(2,2); get(1); put(3,3); get(2)", "output": "1, -1"},
        ],
        tags=["design", "cache"],
        comparison_strategy="exact",
        execution_model="stateful",
        function_name="LRUCache",
        class_name="LRUCache",
    )
    
    test_cases = [
        TestCase(
            serial_number=0,
            test_input={
                "ctor_args": [2],
                "operations": [
                    {"method": "put", "args": [1, 1]},
                    {"method": "put", "args": [2, 2]},
                    {"method": "get", "args": [1]},
                    {"method": "put", "args": [3, 3]},
                    {"method": "get", "args": [2]},
                ]
            },
            expected_output=-1,  # Last operation returns -1
        ),
    ]
    
    solution = ProblemSolution(
        language="python",
        function_name="LRUCache",
        code="""class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)""",
        is_active=True,
    )
    
    problem.test_cases = test_cases
    problem.reference_solution = solution
    
    db.session.add(problem)
    db.session.commit()
    print(f"✓ Created stateful problem: {problem.slug}")
```

Then run:
```bash
cd backend
python -c "from create_problems import create_stateful_problem; from app import create_app, db; app = create_app(); db.init_app(app); app.app_context().push(); create_stateful_problem()"
```

### Step 4: Test the Strategy

**File:** `backend/test_execution.py`

Add a test function:

```python
def test_stateful_problem():
    """Test stateful problem (LRU Cache)"""
    print("\n=== Testing Stateful Problem (LRU Cache) ===")
    
    # ... login and get token ...
    
    run_resp = requests.post(f'{BASE_URL}/submissions/run', 
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json={
            'problemSlug': 'lru-cache',
            'projectId': project_id,
            'code': '''class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)'''
        }
    )
    
    result = run_resp.json()
    print(f"Status: {result.get('status')}")
    print(f"Passed: {result.get('passedTests')}/{result.get('totalTests')}")
    return result.get('status') == 'accepted'
```

Run tests:
```bash
cd backend
python test_execution.py
```

## Complete Checklist

- [ ] Create Strategy class in `sandbox/execution_strategies.py`
- [ ] Register strategy in `STRATEGIES` dict
- [ ] Update Problem model if needed
- [ ] Create database migration if added fields
- [ ] Create example problem in `backend/create_problems.py`
- [ ] Add test function in `backend/test_execution.py`
- [ ] Run tests and verify all pass
- [ ] Update `EXECUTION_STRATEGY_GUIDE.md` with new type
- [ ] Document test_input format

## Common Patterns

### Pattern 1: Multi-Return Operations

If operations return different types:

```python
class MultiReturnStrategy(ExecutionStrategy):
    def execute(self, fn, test_case, namespace):
        # ... setup ...
        results = []
        for op in operations:
            result = method(*method_args)
            results.append(result)
        return results  # Compare entire list
```

### Pattern 2: State Validation

If you need to validate internal state:

```python
class StateValidationStrategy(ExecutionStrategy):
    def execute(self, fn, test_case, namespace):
        # ... setup ...
        # Execute operations
        # Validate internal state
        return instance.__dict__  # Return state dict
```

### Pattern 3: Custom Comparison

If standard comparison doesn't work, use `comparison_strategy`:

```python
# In test_runner.py, add custom comparator
def compare_custom(got, expected):
    # Your custom logic
    return True/False

COMPARISON_STRATEGIES["custom"] = compare_custom
```

Then set on problem:
```python
problem.comparison_strategy = "custom"
```

## Troubleshooting

**Problem:** Strategy not found
- Check `STRATEGIES` dict has your strategy registered
- Verify `execution_model` value matches key in dict

**Problem:** Test input format error
- Ensure test_input has all required fields for your strategy
- Check field names match what strategy.execute() expects

**Problem:** Unexpected return value
- Verify last operation/return matches expected_output type
- Check _normalize() handles your return type

## Performance Tips

1. **Minimize object creation** in strategy.execute()
2. **Cache method lookups** if executing many operations
3. **Use generators** for large result sets
4. **Profile with cProfile** if strategy is slow

```python
import cProfile

def profile_strategy():
    pr = cProfile.Profile()
    pr.enable()
    # ... run strategy ...
    pr.disable()
    pr.print_stats()
```
