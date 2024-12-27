from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_babel import lazy_gettext as _l

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=4)])
    password_confirmation = PasswordField(_l('Password confirmation'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset password'))    
