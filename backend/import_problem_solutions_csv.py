#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

from app import create_app, db
from app.models import Problem, ProblemSolution


def _default_csv_path() -> Path:
    return Path(__file__).resolve().parents[1] / "problems_with_solutions.csv"


def _pick_function_name(problem: Problem, existing: ProblemSolution | None) -> str:
    if existing and existing.function_name:
        return existing.function_name

    active_cases = [tc for tc in (problem.test_cases or []) if tc.is_active]
    if active_cases and active_cases[0].function:
        return active_cases[0].function

    return "solution"


def import_problem_solutions(csv_path: Path) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    app = create_app()
    with app.app_context():
        inserted = 0
        updated = 0
        skipped_missing_problem = 0
        skipped_missing_solution = 0

        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            required_columns = {"id", "slug", "solution"}
            missing = required_columns - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"Missing required CSV columns: {sorted(missing)}")

            for row in reader:
                problem_id = (row.get("id") or "").strip()
                slug = (row.get("slug") or "").strip()
                code = row.get("solution") or ""

                if not code.strip():
                    skipped_missing_solution += 1
                    continue

                problem = None
                if problem_id:
                    problem = Problem.query.filter_by(id=problem_id).first()
                if problem is None and slug:
                    problem = Problem.query.filter_by(slug=slug).first()

                if problem is None:
                    skipped_missing_problem += 1
                    continue

                existing = ProblemSolution.query.filter_by(problem_id=problem.id).first()
                function_name = _pick_function_name(problem, existing)

                if existing is None:
                    solution = ProblemSolution(
                        problem_id=problem.id,
                        language="python",
                        function_name=function_name,
                        code=code,
                        is_active=True,
                        notes=f"Imported from {csv_path.name}",
                    )
                    db.session.add(solution)
                    inserted += 1
                else:
                    existing.language = "python"
                    existing.function_name = function_name
                    existing.code = code
                    existing.is_active = True
                    existing.notes = f"Imported from {csv_path.name}"
                    updated += 1

        db.session.commit()

        print("\n=== ProblemSolution CSV Import Summary ===")
        print(f"CSV: {csv_path}")
        print(f"Inserted: {inserted}")
        print(f"Updated: {updated}")
        print(f"Skipped (missing problem): {skipped_missing_problem}")
        print(f"Skipped (empty solution): {skipped_missing_solution}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import ProblemSolution.code from CSV")
    parser.add_argument(
        "--csv",
        default=str(_default_csv_path()),
        help="Path to CSV with id, slug, solution columns",
    )
    args = parser.parse_args()
    import_problem_solutions(Path(args.csv).expanduser().resolve())


if __name__ == "__main__":
    main()
