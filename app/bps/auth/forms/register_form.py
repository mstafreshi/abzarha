from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from flask_babel import lazy_gettext as _l
import sqlalchemy as sa
from app.models import User
from app import db

class RegisterForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired(), Length(min=4, max=20), Regexp('[A-Za-z_]+', message=_l('Just latin letters and _'))])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(), Length(max=80)])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=4)])
    password_confirmation = PasswordField(_l('Password confirmation'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('submit'))

    def validate_username(self, field):
        user = db.session.scalar(sa.select(User).where(User.username == field.data))
        if user:
            raise ValidationError(_l('This username is taken.'))

    def validate_email(self, field):
        user = db.session.scalar(sa.select(User).where(User.email == field.data))
        if user:
            raise ValidationError(_l('This email is takken.'))