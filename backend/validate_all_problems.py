#!/usr/bin/env python
"""
Validate all problems by running their test cases against their solutions.
This script:
1. Finds all problems with active solutions
2. Runs each solution against all its test cases
3. Reports pass/fail status for each problem
4. Can be run anytime to verify test case validity

Usage:
    python validate_all_problems.py                    # Validate all problems
    python validate_all_problems.py --problem two-sum  # Validate specific problem
"""
import sys
import argparse
from app import create_app, db
from app.models import Problem, ProblemSolution
from app.services.runner import run_code_against_problem

app = create_app()

def validate_problem(problem):
    """Validate a single problem against its solution"""
    # Get active solution
    solution = ProblemSolution.query.filter_by(
        problem_id=problem.id,
        is_active=True
    ).first()
    
    if not solution:
        return {
            'slug': problem.slug,
            'title': problem.title,
            'status': 'no_solution',
            'passed': 0,
            'total': 0,
            'error': 'No active solution found'
        }
    
    # Run the solution against test cases
    result = run_code_against_problem(problem, solution.code)
    
    return {
        'slug': problem.slug,
        'title': problem.title,
        'status': result['status'],
        'passed': result['passed_tests'],
        'total': result['total_tests'],
        'error': result.get('error_output')
    }

def validate_all_problems(problem_slug=None):
    """Validate all or specific problems"""
    with app.app_context():
        if problem_slug:
            problems = Problem.query.filter_by(slug=problem_slug).all()
            if not problems:
                print(f"✗ Problem '{problem_slug}' not found")
                return []
        else:
            problems = Problem.query.all()
        
        if not problems:
            print("✗ No problems found in database")
            return []
        
        print()
        print("=" * 80)
        print("PROBLEM VALIDATION REPORT")
        print("=" * 80)
        print()
        
        results = []
        passing = 0
        failing = 0
        no_solution = 0
        
        for problem in problems:
            result = validate_problem(problem)
            results.append(result)
            
            if result['status'] == 'accepted':
                status_icon = "✓"
                passing += 1
            elif result['status'] == 'no_solution':
                status_icon = "⊘"
                no_solution += 1
            else:
                status_icon = "✗"
                failing += 1
            
            # Print result
            if result['total'] > 0:
                print(f"{status_icon} {result['slug']}: {result['passed']}/{result['total']} tests passed")
            else:
                print(f"{status_icon} {result['slug']}: {result['status']}")
            
            # Show error if failed
            if result['error'] and result['status'] != 'accepted':
                error_preview = result['error'][:150].replace('\n', ' ')
                print(f"  Error: {error_preview}...")
        
        print()
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total Problems: {len(problems)}")
        print(f"✓ Passing: {passing}")
        print(f"✗ Failing: {failing}")
        print(f"⊘ No Solution: {no_solution}")
        print("=" * 80)
        print()
        
        return results

def main():
    parser = argparse.ArgumentParser(
        description='Validate all problems by running test cases against solutions'
    )
    parser.add_argument(
        '--problem',
        type=str,
        help='Validate specific problem by slug'
    )
    
    args = parser.parse_args()
    
    results = validate_all_problems(problem_slug=args.problem)
    
    # Exit with error code if any problems failed
    failing = sum(1 for r in results if r['status'] not in ['accepted', 'no_solution'])
    sys.exit(1 if failing > 0 else 0)

if __name__ == "__main__":
    main()
