from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_babel import lazy_gettext as _l
from app import db
import sqlalchemy as sa
from app.models import DictLang

class LangForm(FlaskForm):
    name = StringField(_l('Lang name'), validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField(_l('submit'))

    def __init__(self, model = None):
        super().__init__()
        self.model = model

    def validate_name(self, field):
        record = db.session.scalar(sa.select(DictLang).where(DictLang.name == field.data))

        if not self.model and record:
             raise ValidationError(_l('This language already exists.'))

        if record and self.model and self.model.name != record.name:
            raise ValidationError(_l('This language already exists.'))