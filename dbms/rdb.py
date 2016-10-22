from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

def register_admin(admin):
    from .models import Intent
    admin.add_view(ModelView(Intent, db.session))
