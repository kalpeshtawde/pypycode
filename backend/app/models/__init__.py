from datetime import datetime, timezone
from app import db
import bcrypt
import uuid


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)
    google_id = db.Column(db.String(256), unique=True, nullable=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    screen_name = db.Column(db.String(64), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    projects = db.relationship("Project", back_populates="user")
    submissions = db.relationship("Submission", back_populates="user")

    def set_password(self, pw: str):
        self.password_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    def check_password(self, pw: str) -> bool:
        if not self.password_hash:
            return False
        return bcrypt.checkpw(pw.encode(), self.password_hash.encode())


class Problem(db.Model):
    __tablename__ = "problems"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = db.Column(db.String(128), unique=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    difficulty = db.Column(db.String(16), nullable=False)  # easy | medium | hard
    description = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=False)
    test_cases = db.Column(db.JSON, nullable=False)   # hidden from API
    examples = db.Column(db.JSON, nullable=False)     # shown to user
    tags = db.Column(db.ARRAY(db.String), default=list)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    submissions = db.relationship("Submission", back_populates="problem")


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(25), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user = db.relationship("User", back_populates="projects")
    submissions = db.relationship("Submission", back_populates="project")


class Submission(db.Model):
    __tablename__ = "submissions"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    problem_id = db.Column(db.String(36), db.ForeignKey("problems.id"), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(16), default="python")
    status = db.Column(db.String(32), default="pending")
    # pending | running | accepted | wrong_answer | time_limit | runtime_error
    passed_tests = db.Column(db.Integer, default=0)
    total_tests = db.Column(db.Integer, default=0)
    runtime_ms = db.Column(db.Integer, nullable=True)
    memory_kb = db.Column(db.Integer, nullable=True)
    error_output = db.Column(db.Text, nullable=True)
    task_id = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user = db.relationship("User", back_populates="submissions")
    project = db.relationship("Project", back_populates="submissions")
    problem = db.relationship("Problem", back_populates="submissions")


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), default="pending")  # pending | read | responded
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class PerfTestConfig(db.Model):
    __tablename__ = "perf_test_configs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, default="default")
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    base_url = db.Column(db.String(256), nullable=False, default="http://api_perf:5000")
    users = db.Column(db.Integer, nullable=False, default=100)
    ramp_up_seconds = db.Column(db.Integer, nullable=False, default=1)
    loops = db.Column(db.Integer, nullable=False, default=1)
    login_path = db.Column(db.String(128), nullable=False, default="/auth/login")
    submit_path = db.Column(db.String(128), nullable=False, default="/submissions/")
    login_email = db.Column(db.String(256), nullable=False, default="demo@pypycode.dev")
    login_password = db.Column(db.String(256), nullable=False, default="demo1234")
    problem_slug = db.Column(db.String(128), nullable=False, default="two-sum")
    code = db.Column(db.Text, nullable=False, default="def solution(nums, target):\n    return [0, 1]")
    project_id = db.Column(db.String(36), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
