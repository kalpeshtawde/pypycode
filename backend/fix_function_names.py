#!/usr/bin/env python
"""
Fix all problems' function_name field by extracting from starter_code.
This script reads the starter_code and extracts the actual function name.
"""
import re
from app import create_app, db
from app.models import Problem

app = create_app()

def extract_function_name(starter_code):
    """Extract function name from starter code"""
    if not starter_code:
        return 'solution'
    
    # Look for 'def function_name('
    match = re.search(r'def\s+(\w+)\s*\(', starter_code)
    if match:
        return match.group(1)
    
    return 'solution'

def fix_all_function_names():
    """Fix function_name for all problems"""
    with app.app_context():
        problems = Problem.query.all()
        
        print(f"Found {len(problems)} problems")
        print()
        
        fixed = 0
        errors = 0
        
        for problem in problems:
            try:
                old_name = problem.function_name
                new_name = extract_function_name(problem.starter_code)
                
                if old_name != new_name:
                    problem.function_name = new_name
                    db.session.add(problem)
                    print(f"✓ {problem.slug}: '{old_name}' → '{new_name}'")
                    fixed += 1
                else:
                    print(f"⊘ {problem.slug}: already '{new_name}'")
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
    print("FIX FUNCTION NAMES")
    print("=" * 70)
    print()
    
    fixed, errors = fix_all_function_names()
    
    print()
    print("=" * 70)
    if errors == 0:
        print(f"✓ All {fixed} problems fixed!")
    else:
        print(f"⚠ {fixed} fixed, {errors} errors")
    print("=" * 70)
