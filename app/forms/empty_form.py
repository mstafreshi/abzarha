from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_babel import lazy_gettext as _l

class EmptyForm(FlaskForm):
    submit = SubmitField(_l('Submit'))