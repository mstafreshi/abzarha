import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from flask import current_app
from time import time
from hashlib import md5
from typing import Optional
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    username: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(80), unique=True, index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(120))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(280))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    lang: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), default='en')
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    notes: so.WriteOnlyMapped['Note'] = so.relationship(back_populates='author')
    note_categories: so.WriteOnlyMapped['NoteCategory'] = so.relationship(back_populates='owner')
    
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

    def avatar(self, size=64):
        hash = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{hash}?s={size}&d=identicon'

    def post_counts(self):
        return db.session.scalar(
            sa.select(sa.func.count()).select_from(self.posts.select().subquery())
        )


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))