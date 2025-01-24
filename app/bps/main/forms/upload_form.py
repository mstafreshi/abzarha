from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from wtforms.validators import Length
from flask_babel import lazy_gettext as _l

class UploadForm(FlaskForm):
    file = FileField(_l('Select image'))
    caption = StringField(_l("Caption"), validators=[Length(max=255)])
    submit = SubmitField(_l('Submit'))