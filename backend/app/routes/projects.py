from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Project, Submission, Problem, ProblemProjectStat
from app.services.runner import run_submission


projects_bp = Blueprint("projects", __name__)
MAX_PROJECT_NAME_LENGTH = 25


def _upsert_problem_project_stat(user_id: str, problem_id: str, project_id: str):
    stat = ProblemProjectStat.query.filter_by(
        user_id=user_id,
        problem_id=problem_id,
        project_id=project_id,
    ).first()
    if not stat:
        stat = ProblemProjectStat(
            user_id=user_id,
            problem_id=problem_id,
            project_id=project_id,
            attempted=True,
            submitted=True,
        )
        db.session.add(stat)
        return

    if not stat.attempted:
        stat.attempted = True
    if not stat.submitted:
        stat.submitted = True


def project_to_dict(project: Project):
    return {
        "id": project.id,
        "name": project.name,
        "isDefault": project.is_default,
        "createdAt": project.created_at.isoformat() if project.created_at else None,
    }


@projects_bp.get("/")
@jwt_required()
def list_projects():
    user_id = get_jwt_identity()
    projects = (
        Project.query.filter_by(user_id=user_id)
        .order_by(Project.is_default.desc(), Project.created_at.asc())
        .all()
    )
    return jsonify([project_to_dict(project) for project in projects])


@projects_bp.post("/")
@jwt_required()
def create_project():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify(error="Project name is required"), 400
    if len(name) > MAX_PROJECT_NAME_LENGTH:
        return jsonify(error="Project name must be at most 25 characters"), 400

    existing = Project.query.filter_by(user_id=user_id, name=name).first()
    if existing:
        return jsonify(error="Project name already exists"), 409

    has_projects = Project.query.filter_by(user_id=user_id).first() is not None
    project = Project(user_id=user_id, name=name, is_default=not has_projects)
    db.session.add(project)
    db.session.commit()

    return jsonify(project_to_dict(project)), 201


@projects_bp.post("/<project_id>/set-default")
@jwt_required()
def set_default_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    Project.query.filter_by(user_id=user_id).update({"is_default": False})
    project.is_default = True
    db.session.commit()

    return jsonify(project_to_dict(project)), 200


@projects_bp.delete("/<project_id>")
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    was_default = project.is_default
    deleted_submissions = Submission.query.filter_by(
        user_id=user_id,
        project_id=project.id,
    ).delete(synchronize_session=False)
    db.session.delete(project)
    db.session.flush()

    if was_default:
        next_project = (
            Project.query.filter_by(user_id=user_id)
            .order_by(Project.created_at.asc())
            .first()
        )
        if next_project:
            next_project.is_default = True

    db.session.commit()

    return jsonify(
        deletedProjectId=project_id,
        deletedSubmissions=deleted_submissions,
    ), 200


@projects_bp.post("/<project_id>/submit")
@jwt_required()
def submit_to_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    data = request.get_json() or {}
    problem_slug = data.get("problemSlug") or data.get("problem_slug")
    problem = Problem.query.filter_by(slug=problem_slug).first_or_404()

    code = data.get("code")
    if not isinstance(code, str) or not code.strip():
        return jsonify(error="Code is required"), 400

    sub = Submission(
        user_id=user_id,
        project_id=project.id,
        problem_id=problem.id,
        code=code,
        total_tests=len(problem.test_cases),
    )
    db.session.add(sub)
    _upsert_problem_project_stat(user_id, problem.id, project.id)
    db.session.commit()

    task = run_submission.delay(sub.id)
    sub.task_id = task.id
    db.session.commit()
    return jsonify(id=sub.id, taskId=task.id, status="pending"), 202
