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
    subscription_status = db.Column(db.String(64), nullable=False, default="none")
    trial_started_at = db.Column(db.DateTime, nullable=True)
    trial_ends_at = db.Column(db.DateTime, nullable=True)
    trial_used = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    projects = db.relationship("Project", back_populates="user")
    submissions = db.relationship("Submission", back_populates="user")
    problem_project_stats = db.relationship("ProblemProjectStat", back_populates="user")
    subscriptions = db.relationship("Subscription", back_populates="user")
    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

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
    examples = db.Column(db.JSON, nullable=False)     # shown to user
    tags = db.Column(db.ARRAY(db.String), default=list)
    comparison_strategy = db.Column(db.String(32), nullable=False, default="exact")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    submissions = db.relationship("Submission", back_populates="problem")
    problem_project_stats = db.relationship("ProblemProjectStat", back_populates="problem")
    test_cases = db.relationship("TestCase", back_populates="problem", cascade="all, delete-orphan", order_by="TestCase.serial_number")
    reference_solution = db.relationship("ProblemSolution", back_populates="problem", uselist=False, cascade="all, delete-orphan")


class ProblemSolution(db.Model):
    __tablename__ = "problem_solutions"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_id = db.Column(db.String(36), db.ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    language = db.Column(db.String(16), nullable=False, default="python")
    function_name = db.Column(db.String(128), nullable=False, default="solution")
    code = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    problem = db.relationship("Problem", back_populates="reference_solution")


class TestCase(db.Model):
    __tablename__ = "test_cases"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_id = db.Column(db.String(36), db.ForeignKey("problems.id"), nullable=False, index=True)
    serial_number = db.Column(db.Integer, nullable=False)  # Starts from 0 for each problem
    function = db.Column(db.String(128), nullable=False, default="solution")
    input = db.Column(db.Text, nullable=False)  # Input as string representation
    expected_output = db.Column(db.Text, nullable=False)  # Expected output as JSON string
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    problem = db.relationship("Problem", back_populates="test_cases")


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(25), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user = db.relationship("User", back_populates="projects")
    submissions = db.relationship("Submission", back_populates="project")
    problem_project_stats = db.relationship("ProblemProjectStat", back_populates="project")


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


class ProblemProjectStat(db.Model):
    __tablename__ = "problem_project_stats"
    __table_args__ = (
        db.UniqueConstraint("user_id", "problem_id", "project_id", name="uix_problem_project_stats_user_problem_project"),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = db.Column(db.String(36), db.ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    attempted = db.Column(db.Boolean, nullable=False, default=False)
    submitted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="problem_project_stats")
    problem = db.relationship("Problem", back_populates="problem_project_stats")
    project = db.relationship("Project", back_populates="problem_project_stats")


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


class Subscription(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    stripe_customer_id = db.Column(db.String(255), nullable=True, index=True)
    stripe_subscription_id = db.Column(db.String(255), nullable=True, unique=True, index=True)
    stripe_checkout_session_id = db.Column(db.String(255), nullable=True, unique=True, index=True)
    stripe_product_id = db.Column(db.String(255), nullable=False)
    stripe_price_id = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(64), nullable=False, default="pending")
    amount_cents = db.Column(db.Integer, nullable=False, default=3000)
    currency = db.Column(db.String(16), nullable=False, default="usd")
    interval = db.Column(db.String(16), nullable=False, default="year")
    current_period_start = db.Column(db.DateTime, nullable=True)
    current_period_end = db.Column(db.DateTime, nullable=True)
    cancel_at_period_end = db.Column(db.Boolean, nullable=False, default=False)
    canceled_at = db.Column(db.DateTime, nullable=True)
    raw_payload = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="subscriptions")


class StripeWebhookEvent(db.Model):
    __tablename__ = "stripe_webhook_events"
    id = db.Column(db.String(255), primary_key=True)
    event_type = db.Column(db.String(128), nullable=False)
    stripe_created_at = db.Column(db.DateTime, nullable=True)
    payload = db.Column(db.JSON, nullable=False)
    processed = db.Column(db.Boolean, nullable=False, default=False)
    processing_error = db.Column(db.Text, nullable=True)
    received_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Favorite(db.Model):
    __tablename__ = "favorites"
    __table_args__ = (db.UniqueConstraint("user_id", "problem_id", name="uix_user_problem"),)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    problem_id = db.Column(db.String(36), db.ForeignKey("problems.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="favorites")
    problem = db.relationship("Problem")
