#!/usr/bin/env python
"""
Link problems to the Gmail user's project
"""
import sys
from app import create_app, db
from app.models import User, Project, Problem, ProblemProjectStat

app = create_app()

def link_problems():
    with app.app_context():
        # Get Gmail user
        user = User.query.filter_by(email='kalpeshtawde@gmail.com').first()
        if not user:
            print("✗ User kalpeshtawde@gmail.com not found")
            return
        
        # Get the test project
        project = Project.query.filter_by(
            user_id=user.id,
            name='Execution Strategy Test Project'
        ).first()
        
        if not project:
            print("✗ Project 'Execution Strategy Test Project' not found")
            return
        
        print(f"✓ Found project: {project.name} (ID: {project.id})")
        
        # Get all problems with the gmail slugs
        problem_slugs = [
            'simple-add-gmail',
            'reverse-str-gmail',
            'calculator-gmail',
            'array-sum-gmail'
        ]
        
        problems = Problem.query.filter(Problem.slug.in_(problem_slugs)).all()
        print(f"✓ Found {len(problems)} problems")
        
        # Link each problem to the project
        linked = 0
        for problem in problems:
            # Check if already linked
            stat = ProblemProjectStat.query.filter_by(
                user_id=user.id,
                problem_id=problem.id,
                project_id=project.id
            ).first()
            
            if not stat:
                stat = ProblemProjectStat(
                    user_id=user.id,
                    problem_id=problem.id,
                    project_id=project.id
                )
                db.session.add(stat)
                linked += 1
                print(f"  ✓ Linked: {problem.title}")
            else:
                print(f"  ✓ Already linked: {problem.title}")
        
        db.session.commit()
        
        print()
        print("=" * 60)
        print(f"✓ Successfully linked {linked} problems to project")
        print("=" * 60)
        print()
        print("Problems are now visible in the project!")
        print()

if __name__ == '__main__':
    try:
        link_problems()
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
