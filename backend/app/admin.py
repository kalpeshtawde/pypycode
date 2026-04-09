from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms import StringField, validators
from flask_admin.form import BaseForm
from flask import Response, jsonify
import json
import os
from app import db
from app.models import (
    User,
    Problem,
    Project,
    Submission,
    Contact,
    PerfTestConfig,
    Subscription,
    StripeWebhookEvent,
)


class UserForm(BaseForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    screen_name = StringField('Screen Name')
    google_id = StringField('Google ID')


class UserAdmin(ModelView):
    column_list = [
        'id', 'username', 'email', 'first_name', 'last_name', 'screen_name',
        'subscription_status', 'trial_used', 'trial_started_at', 'trial_ends_at',
        'google_id', 'created_at'
    ]
    column_searchable_list = ['username', 'email', 'first_name', 'last_name', 'screen_name']
    column_sortable_list = ['created_at', 'first_name', 'last_name', 'screen_name', 'subscription_status', 'trial_used', 'trial_started_at', 'trial_ends_at']
    column_filters = ['subscription_status', 'trial_used', 'created_at']
    form = UserForm
    can_create = False
    can_delete = False
    column_formatters = {
        'trial_started_at': lambda view, context, model, name: model.trial_started_at.strftime('%Y-%m-%d %H:%M') if model.trial_started_at else '-',
        'trial_ends_at': lambda view, context, model, name: model.trial_ends_at.strftime('%Y-%m-%d %H:%M') if model.trial_ends_at else '-',
    }


class SubscriptionAdmin(ModelView):
    column_list = [
        'id', 'user_id', 'status', 'amount_cents', 'currency', 'interval',
        'stripe_customer_id', 'stripe_subscription_id', 'created_at', 'updated_at'
    ]
    column_searchable_list = [
        'user_id', 'status', 'stripe_customer_id', 'stripe_subscription_id',
        'stripe_checkout_session_id', 'stripe_product_id', 'stripe_price_id'
    ]
    column_sortable_list = ['status', 'created_at', 'updated_at']
    column_filters = ['status', 'currency', 'interval', 'created_at']
    can_create = False
    column_formatters = {
        'amount_cents': lambda v, c, m, p: f"${m.amount_cents/100:.2f}" if m.amount_cents else '-',
        'created_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M') if m.created_at else '-',
        'updated_at': lambda v, c, m, p: m.updated_at.strftime('%Y-%m-%d %H:%M') if m.updated_at else '-',
    }
    column_labels = {
        'amount_cents': 'Amount',
        'stripe_customer_id': 'Stripe Customer',
        'stripe_subscription_id': 'Stripe Subscription',
    }


class StripeWebhookEventAdmin(ModelView):
    column_list = [
        StripeWebhookEvent.id,
        StripeWebhookEvent.event_type,
        StripeWebhookEvent.processed,
        StripeWebhookEvent.stripe_created_at,
        StripeWebhookEvent.received_at,
    ]
    column_searchable_list = [StripeWebhookEvent.id, StripeWebhookEvent.event_type]
    column_sortable_list = [StripeWebhookEvent.processed, StripeWebhookEvent.stripe_created_at, StripeWebhookEvent.received_at]
    can_create = False
    can_edit = False
    can_delete = False


class ProblemAdmin(ModelView):
    column_list = ['id', 'slug', 'title', 'difficulty', 'tags', 'created_at']
    column_searchable_list = ['slug', 'title', 'description']
    column_sortable_list = ['difficulty', 'created_at', 'slug']
    column_filters = ['difficulty', 'created_at']
    can_create = True
    can_edit = True
    can_delete = True
    form_excluded_columns = ['submissions']


class ProjectAdmin(ModelView):
    column_list = [Project.id, Project.user_id, Project.name, Project.is_default, Project.created_at]
    column_searchable_list = [Project.name]
    column_sortable_list = [Project.name, Project.is_default, Project.created_at]


class SubmissionAdmin(ModelView):
    column_list = ['id', 'user_id', 'problem_id', 'project_id', 'status', 'passed_tests', 'total_tests', 'runtime_ms', 'memory_kb', 'created_at']
    column_searchable_list = ['status', 'user_id', 'problem_id']
    column_sortable_list = ['status', 'created_at', 'runtime_ms', 'memory_kb']
    column_filters = ['status', 'created_at']
    can_create = False
    can_edit = False
    can_delete = False
    column_formatters = {
        'created_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M') if m.created_at else '-',
        'runtime_ms': lambda v, c, m, p: f"{m.runtime_ms}ms" if m.runtime_ms else '-',
        'memory_kb': lambda v, c, m, p: f"{m.memory_kb}KB" if m.memory_kb else '-',
        'passed_tests': lambda v, c, m, p: f"{m.passed_tests}/{m.total_tests}" if m.total_tests else '-',
    }
    column_labels = {
        'runtime_ms': 'Runtime',
        'memory_kb': 'Memory',
        'passed_tests': 'Tests',
    }


class ContactAdmin(ModelView):
    column_list = [Contact.id, Contact.name, Contact.email, Contact.subject, Contact.status, Contact.created_at]
    column_searchable_list = [Contact.name, Contact.email, Contact.subject]
    column_sortable_list = [Contact.status, Contact.created_at]
    column_default_sort = ('created_at', True)  # Sort by created_at descending
    form_choices = {
        'status': [
            ('pending', 'Pending'),
            ('read', 'Read'),
            ('responded', 'Responded')
        ]
    }


class PerfTestConfigAdmin(ModelView):
    column_list = [
        PerfTestConfig.id,
        PerfTestConfig.name,
        PerfTestConfig.enabled,
        PerfTestConfig.base_url,
        PerfTestConfig.users,
        PerfTestConfig.ramp_up_seconds,
        PerfTestConfig.loops,
        PerfTestConfig.updated_at,
    ]
    form_columns = [
        "name",
        "enabled",
        "base_url",
        "users",
        "ramp_up_seconds",
        "loops",
        "login_path",
        "submit_path",
        "login_email",
        "login_password",
        "problem_slug",
        "code",
        "project_id",
    ]
    column_searchable_list = [PerfTestConfig.name, PerfTestConfig.base_url]
    can_delete = False


def _to_jmeter_properties(config: PerfTestConfig) -> str:
    encoded_code = (config.code or "").replace("\\", "\\\\").replace("\r\n", "\n").replace("\n", "\\n")
    property_pairs = {
        "perf.base_url": config.base_url,
        "perf.users": str(config.users),
        "perf.ramp_up": str(config.ramp_up_seconds),
        "perf.loops": str(config.loops),
        "perf.login_path": config.login_path,
        "perf.submit_path": config.submit_path,
        "perf.login_email": config.login_email,
        "perf.login_password": config.login_password,
        "perf.problem_slug": config.problem_slug,
        "perf.project_id": config.project_id or "",
        "perf.code": encoded_code,
    }
    return "\n".join(f"{key}={value}" for key, value in property_pairs.items()) + "\n"


def _perf_config_snapshot(config: PerfTestConfig):
    return {
        "id": config.id,
        "name": config.name,
        "enabled": config.enabled,
        "baseUrl": config.base_url,
        "users": config.users,
        "rampUpSeconds": config.ramp_up_seconds,
        "loops": config.loops,
        "loginPath": config.login_path,
        "submitPath": config.submit_path,
        "loginEmail": config.login_email,
        "problemSlug": config.problem_slug,
        "projectId": config.project_id,
        "updatedAt": config.updated_at.isoformat() if config.updated_at else None,
    }


class DashboardView(AdminIndexView):
    @expose('/')
    def index(self):
        from app.models import User, Problem, Submission, Subscription, Contact
        user_count = User.query.count()
        problem_count = Problem.query.count()
        submission_count = Submission.query.count()
        subscription_count = Subscription.query.count()
        pending_contacts = Contact.query.filter_by(status='pending').count()
        
        return self.render('admin/index.html',
            user_count=user_count,
            problem_count=problem_count,
            submission_count=submission_count,
            subscription_count=subscription_count,
            pending_contacts=pending_contacts
        )


def init_admin(app):
    admin = Admin(
        app,
        name='PyPyCode Admin',
        template_mode='bootstrap4',
        base_template='admin/master.html',
        index_view=DashboardView(
            name='Dashboard',
            url='/admin'
        )
    )
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ProblemAdmin(Problem, db.session))
    admin.add_view(ProjectAdmin(Project, db.session))
    admin.add_view(SubmissionAdmin(Submission, db.session))
    admin.add_view(ContactAdmin(Contact, db.session, name='Contact Queries', endpoint='contact-queries'))
    admin.add_view(PerfTestConfigAdmin(PerfTestConfig, db.session, name='Performance Config', endpoint='perf-config'))
    admin.add_view(SubscriptionAdmin(Subscription, db.session, name='Subscriptions', endpoint='subscriptions'))
    admin.add_view(StripeWebhookEventAdmin(StripeWebhookEvent, db.session, name='Stripe Webhook Events', endpoint='stripe-webhook-events'))

    @app.get("/admin/perf/jmeter.properties")
    def perf_jmeter_properties():
        config = (
            PerfTestConfig.query.filter_by(enabled=True)
            .order_by(PerfTestConfig.updated_at.desc(), PerfTestConfig.id.desc())
            .first()
        )
        if not config:
            config = PerfTestConfig.query.order_by(PerfTestConfig.updated_at.desc(), PerfTestConfig.id.desc()).first()

        if not config:
            config = PerfTestConfig(name="default")
            db.session.add(config)
            db.session.commit()

        return Response(_to_jmeter_properties(config), mimetype="text/plain")

    @app.get("/admin/perf/latest-run")
    def perf_latest_run():
        config = (
            PerfTestConfig.query.filter_by(enabled=True)
            .order_by(PerfTestConfig.updated_at.desc(), PerfTestConfig.id.desc())
            .first()
        )
        if not config:
            config = PerfTestConfig.query.order_by(PerfTestConfig.updated_at.desc(), PerfTestConfig.id.desc()).first()

        metadata_path = "/perf-results/latest-run.json"
        metadata = None

        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as metadata_file:
                metadata = json.load(metadata_file)

        return jsonify(
            metadata=metadata,
            activeConfig=_perf_config_snapshot(config) if config else None,
        )
