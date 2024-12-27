from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

class PostForm(FlaskForm):
    text = TextAreaField(_l('Text'), validators=[DataRequired()])
    submit = SubmitField(_l('Send'))