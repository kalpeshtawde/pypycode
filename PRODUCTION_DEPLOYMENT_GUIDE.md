# Production Deployment Guide

## Overview

The execution strategy refactor introduces database schema changes. This guide covers safe deployment to production with existing data.

## Pre-Deployment Checklist

### 1. Backup Your Database
```bash
# Create a backup before any migration
pg_dump -U pypycode -d pypycode > pypycode_backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Review Migrations

Two migrations are available:

| Migration | Use Case | Risk |
|-----------|----------|------|
| **016** (old) | Fresh database, no existing data | ❌ Will fail with existing data |
| **017** (safe) | Production with existing data | ✅ Safe, preserves data |

## Deployment Steps

### Step 1: Rollback Old Migration (if applied)

If you already applied migration 016 to production:

```bash
# Downgrade to previous version
DATABASE_URL=postgresql://... python -m flask db downgrade 015

# Verify
DATABASE_URL=postgresql://... python -m flask db current
# Should show: 015
```

### Step 2: Delete Migration 016

Remove the old migration file:
```bash
rm backend/migrations/versions/016_refactor_execution_model.py
```

### Step 3: Apply Safe Migration

```bash
# Apply migration 017
DATABASE_URL=postgresql://... python -m flask db upgrade

# Verify
DATABASE_URL=postgresql://... python -m flask db current
# Should show: 017
```

### Step 4: Verify Data Integrity

```bash
# Check test_cases were migrated
psql -U pypycode -d pypycode -c "
  SELECT COUNT(*) as total,
         COUNT(test_input) as with_test_input,
         COUNT(expected_output) as with_expected
  FROM test_cases;
"

# Check a sample record
psql -U pypycode -d pypycode -c "
  SELECT id, test_input, expected_output 
  FROM test_cases 
  LIMIT 1;
"
```

### Step 5: Rebuild and Deploy

```bash
# Rebuild sandbox image
docker build -t pypycode-sandbox:latest ./sandbox/

# Restart services
docker compose restart api worker

# Verify health
curl http://localhost:5000/health
```

## What Migration 017 Does

### Data Preservation
- ✅ Converts existing `input` strings to `test_input` JSON
- ✅ Converts `expected_output` text to JSONB
- ✅ Keeps old columns for rollback safety
- ✅ Handles various data formats (JSON, strings, numbers)

### New Schema
```sql
-- Problems table gets:
- execution_model (default: 'function')
- function_name (default: 'solution')
- class_name (nullable)
- method_name (nullable)

-- TestCases table gets:
- test_input (JSON, required)
- comparison_strategy (nullable)
- expected_output (JSONB, required)

-- Old columns kept for safety:
- input (Text)
- function (String)
- arg_types (JSON)
```

## Rollback Plan

If something goes wrong:

```bash
# Downgrade to previous version
DATABASE_URL=postgresql://... python -m flask db downgrade 016

# Or all the way back
DATABASE_URL=postgresql://... python -m flask db downgrade 015

# Restore from backup if needed
psql -U pypycode -d pypycode < pypycode_backup_20260518_120000.sql
```

## Testing Before Production

### 1. Test on Staging
```bash
# Apply migration to staging database
DATABASE_URL=postgresql://staging_user:pass@staging_host/staging_db \
  python -m flask db upgrade

# Run tests
python test_execution.py

# Verify problems still work
curl http://staging:5000/problems/
```

### 2. Verify Data Conversion

```bash
# Check old data still accessible
psql -U pypycode -d pypycode -c "
  SELECT COUNT(*) FROM test_cases WHERE input IS NOT NULL;
"

# Check new data populated
psql -U pypycode -d pypycode -c "
  SELECT COUNT(*) FROM test_cases WHERE test_input != '{}';
"
```

### 3. Test Problem Execution

```bash
# Test function-based problem
curl -X POST http://localhost:5000/submissions/run \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"problemSlug":"two-sum","code":"def solution(nums, target):\n    return [0, 1]"}'

# Test class-based problem
curl -X POST http://localhost:5000/submissions/run \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"problemSlug":"range-sum-query","code":"class RangeSumQuery:\n    def __init__(self, nums):\n        pass\n    def sumRange(self, left, right):\n        return 0"}'
```

## Production Deployment Checklist

- [ ] Database backup created
- [ ] Migration 016 removed from codebase
- [ ] Migration 017 applied to staging
- [ ] Data integrity verified on staging
- [ ] Problem execution tested on staging
- [ ] Rollback plan documented
- [ ] Team notified of deployment
- [ ] Migration 017 applied to production
- [ ] Production health checks pass
- [ ] Sample problems tested in production
- [ ] Monitoring alerts configured

## Monitoring After Deployment

### Key Metrics to Watch
1. **Problem Execution Success Rate** - Should be > 99%
2. **Database Query Performance** - Should be < 100ms
3. **Sandbox Execution Time** - Should be < 4s
4. **Error Logs** - Watch for migration-related errors

### Queries to Monitor

```sql
-- Check for failed test executions
SELECT COUNT(*) FROM submissions 
WHERE status = 'runtime_error' 
AND created_at > NOW() - INTERVAL '1 hour';

-- Check for data inconsistencies
SELECT COUNT(*) FROM test_cases 
WHERE test_input = '{}' OR expected_output IS NULL;

-- Monitor execution times
SELECT AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) as avg_time
FROM submissions 
WHERE created_at > NOW() - INTERVAL '1 hour';
```

## Troubleshooting

### Issue: Migration fails with "column does not exist"

**Cause:** Migration 016 was partially applied

**Solution:**
```bash
# Downgrade completely
python -m flask db downgrade 015

# Remove migration 016
rm backend/migrations/versions/016_refactor_execution_model.py

# Apply safe migration
python -m flask db upgrade
```

### Issue: Test cases show empty test_input

**Cause:** Data conversion didn't work properly

**Solution:**
```bash
# Check what data exists
SELECT id, "input", test_input FROM test_cases LIMIT 5;

# Manually fix if needed
UPDATE test_cases 
SET test_input = jsonb_build_object('args', json_array_elements("input"::json))
WHERE test_input = '{}' AND "input" IS NOT NULL;
```

### Issue: Problems not executing after migration

**Cause:** execution_model not set correctly

**Solution:**
```bash
# Check execution_model values
SELECT DISTINCT execution_model FROM problems;

# Set defaults if missing
UPDATE problems SET execution_model = 'function' 
WHERE execution_model IS NULL;
```

## Long-Term Maintenance

### After 1 Month (Safe to Remove Old Columns)

Once you're confident the migration is stable:

```bash
# Create cleanup migration
python -m flask db migrate -m "cleanup old test_case columns"

# Edit migration to drop old columns:
# op.drop_column('test_cases', 'input')
# op.drop_column('test_cases', 'function')
# op.drop_column('test_cases', 'arg_types')

# Apply
python -m flask db upgrade
```

### Monitoring Script

Create a daily check:
```bash
#!/bin/bash
# check_migration_health.sh

DATABASE_URL=postgresql://... python << 'EOF'
from app import db
from app.models import TestCase, Problem

# Check data integrity
total = TestCase.query.count()
with_input = TestCase.query.filter(TestCase.test_input != {}).count()
with_output = TestCase.query.filter(TestCase.expected_output.isnot(None)).count()

print(f"Total test cases: {total}")
print(f"With test_input: {with_input}")
print(f"With expected_output: {with_output}")

if with_input < total * 0.95:
    print("WARNING: Some test_input values missing!")
    
if with_output < total * 0.95:
    print("WARNING: Some expected_output values missing!")
EOF
```

## Questions?

Refer to:
- `EXECUTION_STRATEGY_GUIDE.md` - Architecture details
- `ADD_NEW_PROBLEM_TYPE.md` - Extending the system
- Migration files - Exact SQL being applied
