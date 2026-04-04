#!/usr/bin/env python3
"""
Script to import problems from problems.json into the database.
"""

import json
import os
import sys
from datetime import datetime, timezone

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import Problem

def import_problems():
    """Import problems from problems.json into the database."""
    app = create_app()
    
    with app.app_context():
        # Load problems from JSON file
        problems_file = os.path.join(os.path.dirname(__file__), 'problems.json')
        
        if not os.path.exists(problems_file):
            print(f"Error: {problems_file} not found!")
            return
        
        with open(problems_file, 'r') as f:
            problems_data = json.load(f)
        
        print(f"Found {len(problems_data['problems'])} problems to import...")
        
        imported_count = 0
        skipped_count = 0
        
        for problem_data in problems_data['problems']:
            # Check if problem already exists
            existing_problem = Problem.query.filter_by(slug=problem_data['slug']).first()
            
            if existing_problem:
                print(f"Skipping '{problem_data['slug']}' - already exists")
                skipped_count += 1
                continue
            
            # Create new problem
            problem = Problem(
                slug=problem_data['slug'],
                title=problem_data['title'],
                difficulty=problem_data['difficulty'],
                description=problem_data['description'],
                starter_code=problem_data['starterCode'],
                test_cases=problem_data['testCases'],
                examples=problem_data['examples'],
                tags=problem_data.get('tags', []),
                created_at=datetime.now(timezone.utc)
            )
            
            db.session.add(problem)
            db.session.commit()
            
            print(f"✓ Imported '{problem_data['slug']}'")
            imported_count += 1
        
        print(f"\nImport complete!")
        print(f"✓ Imported: {imported_count} problems")
        print(f"⚠ Skipped: {skipped_count} problems (already exist)")

if __name__ == "__main__":
    import_problems()
