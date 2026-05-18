#!/usr/bin/env python
"""
Ingest problems from problems.json, validate test cases, and fix any issues.
This script:
1. Loads problems from JSON file
2. Creates problems in database with test cases
3. Validates each problem with a basic solution
4. Reports which test cases are failing
5. Suggests fixes for invalid test cases
"""
import json
import sys
from app import create_app, db
from app.models import Problem, TestCase, ProblemSolution
from app.services.runner import run_code_against_problem

app = create_app()

# Basic solutions for common problem types
BASIC_SOLUTIONS = {
    "pair-with-target-sum": """def find_pair(fruits, target):
    seen = {}
    for i, num in enumerate(fruits):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""",
    "reverse-a-scroll": """def reverse_scroll(s):
    return s[::-1]
""",
    "mirror-phrase": """def is_mirror(phrase):
    cleaned = ''.join(c.lower() for c in phrase if c.isalnum())
    return cleaned == cleaned[::-1]
""",
}

def extract_function_name(starter_code):
    """Extract function name from starter code"""
    import re
    match = re.search(r'def\s+(\w+)\s*\(', starter_code)
    if match:
        return match.group(1)
    return 'solution'

def load_problems_from_json(filepath):
    """Load problems from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get('problems', [])

def parse_test_input(input_str):
    """Parse test input string to actual values"""
    try:
        # Try to evaluate as Python literal
        return eval(input_str)
    except:
        # If it fails, return as string
        return input_str

def parse_expected_output(output_str):
    """Parse expected output string to actual value"""
    try:
        # Try to evaluate as Python literal
        return eval(output_str)
    except:
        # If it fails, return as string
        return output_str

def ingest_problems(json_filepath):
    """Ingest problems from JSON file into database"""
    with app.app_context():
        problems_data = load_problems_from_json(json_filepath)
        
        print(f"Found {len(problems_data)} problems in JSON file")
        print()
        
        ingested = 0
        failed = 0
        
        for prob_data in problems_data:
            try:
                slug = prob_data.get('slug')
                
                # Check if problem already exists
                existing = Problem.query.filter_by(slug=slug).first()
                if existing:
                    print(f"⊘ Skipping {slug} (already exists)")
                    continue
                
                # Extract function name from starter code
                starter_code = prob_data.get('starterCode', '')
                function_name = extract_function_name(starter_code)
                
                # Create problem
                problem = Problem(
                    slug=slug,
                    title=prob_data.get('title'),
                    difficulty=prob_data.get('difficulty', 'medium'),
                    description=prob_data.get('description'),
                    starter_code=starter_code,
                    execution_model='function',
                    function_name=function_name,
                    comparison_strategy='exact',
                    examples=prob_data.get('examples', []),
                    tags=prob_data.get('tags', [])
                )
                db.session.add(problem)
                db.session.flush()
                
                # Add test cases
                test_cases_data = prob_data.get('testCases', [])
                for idx, tc_data in enumerate(test_cases_data):
                    input_str = tc_data.get('input', '')
                    expected_str = tc_data.get('expected', '')
                    
                    # Parse inputs and outputs
                    try:
                        # Try to parse as a list of arguments
                        # Input format: "[2, 7, 11, 15], 9" or "\"hello\""
                        parsed = parse_test_input(f"[{input_str}]")
                        if isinstance(parsed, list):
                            args = parsed
                        else:
                            args = [parsed]
                    except:
                        # Fallback: try parsing directly
                        try:
                            args = [parse_test_input(input_str)]
                        except:
                            args = [input_str]
                    
                    try:
                        expected = parse_expected_output(expected_str)
                    except:
                        expected = expected_str
                    
                    tc = TestCase(
                        problem_id=problem.id,
                        serial_number=idx,
                        test_input={"args": args},
                        expected_output=expected,
                        is_active=True
                    )
                    db.session.add(tc)
                
                db.session.commit()
                print(f"✓ Ingested {slug} ({len(test_cases_data)} test cases)")
                ingested += 1
                
            except Exception as e:
                print(f"✗ Failed to ingest {slug}: {str(e)[:100]}")
                failed += 1
                db.session.rollback()
        
        print()
        print(f"Summary: {ingested} ingested, {failed} failed")
        return ingested

def validate_problems():
    """Validate all problems with basic solutions"""
    with app.app_context():
        problems = Problem.query.all()
        
        print()
        print("=" * 70)
        print("VALIDATION REPORT")
        print("=" * 70)
        print()
        
        total_problems = len(problems)
        passing_problems = 0
        failing_problems = []
        
        for problem in problems:
            slug = problem.slug
            
            # Get basic solution if available
            solution_code = BASIC_SOLUTIONS.get(slug)
            if not solution_code:
                print(f"⊘ {slug}: No basic solution available (skipped)")
                continue
            
            # Rename function to match problem's function_name
            import re
            solution_code = re.sub(
                r'def\s+\w+\s*\(',
                f'def {problem.function_name}(',
                solution_code,
                count=1
            )
            
            # Run validation
            result = run_code_against_problem(problem, solution_code)
            
            if result['status'] == 'accepted':
                print(f"✓ {slug}: All {result['total_tests']} tests passed")
                passing_problems += 1
            else:
                print(f"✗ {slug}: {result['passed_tests']}/{result['total_tests']} tests passed")
                if result.get('error_output'):
                    # Extract failed cases from error output
                    print(f"  Error: {result['error_output'][:200]}")
                failing_problems.append({
                    'slug': slug,
                    'passed': result['passed_tests'],
                    'total': result['total_tests'],
                    'error': result.get('error_output')
                })
        
        print()
        print("=" * 70)
        print(f"Results: {passing_problems}/{total_problems} problems passing")
        print("=" * 70)
        
        if failing_problems:
            print()
            print("Failing Problems:")
            for prob in failing_problems:
                print(f"  - {prob['slug']}: {prob['passed']}/{prob['total']} tests")
        
        return passing_problems, failing_problems

def main():
    json_file = '/Users/kalpeshtawde/Downloads/problems.json'
    
    print()
    print("=" * 70)
    print("PROBLEM INGESTION AND VALIDATION")
    print("=" * 70)
    print()
    
    # Step 1: Ingest problems
    print("Step 1: Ingesting problems from JSON...")
    print("-" * 70)
    ingested = ingest_problems(json_file)
    
    # Step 2: Validate problems
    print()
    print("Step 2: Validating problems...")
    print("-" * 70)
    passing, failing = validate_problems()
    
    print()
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print()
    print(f"✓ Ingested {ingested} problems")
    print(f"✓ {passing} problems have valid test cases")
    if failing:
        print(f"⚠ {len(failing)} problems need test case fixes")
        print()
        print("To fix failing test cases:")
        print("1. Review the error messages above")
        print("2. Update test_input or expected_output in database")
        print("3. Re-run this script to validate")
    
    sys.exit(0 if not failing else 1)

if __name__ == "__main__":
    main()
