from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_babel import lazy_gettext as _l
# from app.forms.validators import Unique
from app.models import NoteCategory
from flask_login import current_user
from app import db
import sqlalchemy as sa

class CategoryForm(FlaskForm):
    id = HiddenField()
    name = StringField(_l('Name'), validators=[DataRequired(), Length(min=2)])
    submit = SubmitField(_l('submit'))

    def validate_name(self, field):
        finded = db.session.scalar(
            sa.select(NoteCategory).where(
                NoteCategory.name == field.data,
                NoteCategory.owner == current_user
            )
        )

        message = _l("%(name)s already exists", name=field.data)

        # insert new record
        if finded and self.id.data == '':
            raise ValidationError(message)

        # update same record
        if finded and int(self.id.data) != finded.id:
            raise ValidationError(message)

