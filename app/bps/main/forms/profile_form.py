from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length
from flask_babel import lazy_gettext as _l

class ProfileForm(FlaskForm):
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=280)])
    submit = SubmitField(_l('Submit'))