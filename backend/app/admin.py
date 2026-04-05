from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import db
from app.models import User, Problem, Submission, Contact


class UserAdmin(ModelView):
    column_list = [User.id, User.username, User.email, User.created_at]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.created_at]


class ProblemAdmin(ModelView):
    column_list = [Problem.id, Problem.slug, Problem.title, Problem.difficulty, Problem.created_at]
    column_searchable_list = [Problem.slug, Problem.title]
    column_sortable_list = [Problem.difficulty, Problem.created_at]


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


def init_admin(app):
    admin = Admin(app, name='PyPyCode Admin', template_mode='bootstrap4')
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ProblemAdmin(Problem, db.session))
    admin.add_view(SubmissionAdmin(Submission, db.session))
    admin.add_view(ContactAdmin(Contact, db.session, name='Contact Queries', endpoint='contact-queries'))
