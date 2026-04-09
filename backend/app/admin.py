from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
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
    column_list = ['id', 'username', 'email', 'first_name', 'last_name', 'screen_name', 'google_id', 'created_at']
    column_searchable_list = ['username', 'email', 'first_name', 'last_name', 'screen_name']
    column_sortable_list = ['created_at', 'first_name', 'last_name', 'screen_name']
    form = UserForm
    can_create = False
    can_delete = False


class SubscriptionAdmin(ModelView):
    column_list = [
        Subscription.id,
        Subscription.user_id,
        Subscription.status,
        Subscription.amount_cents,
        Subscription.currency,
        Subscription.interval,
        Subscription.stripe_customer_id,
        Subscription.stripe_subscription_id,
        Subscription.created_at,
        Subscription.updated_at,
    ]
    column_searchable_list = [
        Subscription.user_id,
        Subscription.status,
        Subscription.stripe_customer_id,
        Subscription.stripe_subscription_id,
        Subscription.stripe_checkout_session_id,
        Subscription.stripe_product_id,
        Subscription.stripe_price_id,
    ]
    column_sortable_list = [Subscription.status, Subscription.created_at, Subscription.updated_at]
    can_create = False


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
    column_list = [Problem.id, Problem.slug, Problem.title, Problem.difficulty, Problem.created_at]
    column_searchable_list = [Problem.slug, Problem.title]
    column_sortable_list = [Problem.difficulty, Problem.created_at]


class ProjectAdmin(ModelView):
    column_list = [Project.id, Project.user_id, Project.name, Project.is_default, Project.created_at]
    column_searchable_list = [Project.name]
    column_sortable_list = [Project.name, Project.is_default, Project.created_at]


class SubmissionAdmin(ModelView):
    column_list = [Submission.id, Submission.user_id, Submission.problem_id, Submission.status, Submission.created_at]
    column_searchable_list = [Submission.status]
    column_sortable_list = [Submission.status, Submission.created_at]


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


def init_admin(app):
    admin = Admin(app, name='PyPyCode Admin', template_mode='bootstrap4')
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
