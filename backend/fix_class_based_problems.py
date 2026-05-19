#!/usr/bin/env python
"""
Fix class-based problems by:
1. Changing execution_model from 'function' to 'class'
2. Extracting class_name from starter_code
3. Extracting method_name from the class methods
"""
import re
from app import create_app, db
from app.models import Problem

app = create_app()

def extract_class_name(starter_code):
    """Extract class name from starter code"""
    if not starter_code:
        return None
    
    match = re.search(r'class\s+(\w+)', starter_code)
    if match:
        return match.group(1)
    return None

def extract_method_name(starter_code):
    """Extract the main method name (not __init__)"""
    if not starter_code:
        return None
    
    # Find all method definitions
    methods = re.findall(r'def\s+(\w+)\s*\(', starter_code)
    
    # Return first non-dunder method
    for method in methods:
        if not method.startswith('_'):
            return method
    
    return None

def fix_class_based_problems():
    """Fix execution_model and extract class/method names"""
    with app.app_context():
        # Find all problems with __init__ as function_name
        problems = Problem.query.filter_by(function_name='__init__').all()
        
        print(f"Found {len(problems)} class-based problems")
        print()
        
        fixed = 0
        errors = 0
        
        for problem in problems:
            try:
                class_name = extract_class_name(problem.starter_code)
                method_name = extract_method_name(problem.starter_code)
                
                if not class_name:
                    print(f"✗ {problem.slug}: Could not extract class name")
                    errors += 1
                    continue
                
                problem.execution_model = 'class'
                problem.class_name = class_name
                problem.method_name = method_name or 'solution'
                problem.function_name = class_name  # Keep class_name as function_name for compatibility
                
                db.session.add(problem)
                print(f"✓ {problem.slug}: class={class_name}, method={method_name or 'solution'}")
                fixed += 1
                
            except Exception as e:
                print(f"✗ {problem.slug}: {str(e)[:100]}")
                errors += 1
        
        db.session.commit()
        print()
        print(f"Summary: {fixed} fixed, {errors} errors")
        return fixed, errors

if __name__ == "__main__":
    print()
    print("=" * 70)
    print("FIX CLASS-BASED PROBLEMS")
    print("=" * 70)
    print()
    
    fixed, errors = fix_class_based_problems()
    
    print()
    print("=" * 70)
    if errors == 0:
        print(f"✓ All {fixed} class-based problems fixed!")
    else:
        print(f"⚠ {fixed} fixed, {errors} errors")
    print("=" * 70)
