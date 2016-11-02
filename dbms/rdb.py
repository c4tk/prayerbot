from flask import redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth

from werkzeug.exceptions import HTTPException

class AuthException(HTTPException):
    def __init__(self, message):
        super(AuthException, self).__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class ModelView(sqla.ModelView):
    @classmethod
    def setup_basic_auth(cls, basic_auth):
        cls.basic_auth = basic_auth
    def is_accessible(self):
        if not self.basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(self.basic_auth.challenge())

db = SQLAlchemy()

def register_admin(admin, app):
    from .models import Intent, BibleVerse, User
    basic_auth = BasicAuth(app)
    ModelView.setup_basic_auth(basic_auth)
    admin.add_view(ModelView(Intent, db.session))
    admin.add_view(ModelView(BibleVerse, db.session))
    admin.add_view(ModelView(User, db.session))

