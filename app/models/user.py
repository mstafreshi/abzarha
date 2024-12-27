import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from flask import current_app
from time import time

class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(80), unique=True, index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(80))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self):
        return jwt.encode(
            {'id': self.id, 'exp': time() + 12 * 60 * 60},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['id']
        except:
            return

        return db.session.get(User, int(id))

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))