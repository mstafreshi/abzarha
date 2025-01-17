from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_babel import lazy_gettext as _l
import sqlalchemy as sa
from app import db
from app.models import NoteCategory
from flask_login import current_user
from flask import current_app

class NoteForm(FlaskForm):
    title = StringField(_l('Title'), validators=[Length(max=255)])
    body = TextAreaField(_l('Body'), validators=[DataRequired()])
    category_id = SelectField(_l('Category'), coerce=int, validators=[DataRequired()])
    lang = SelectField(_l('Language'), coerce=str)

    submit = SubmitField(_l('Submit'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id.choices = [
            (r.id, r.name) for r in db.session.scalars(
                sa.select(NoteCategory)
                    .where(NoteCategory.owner == current_user)
                    .order_by(NoteCategory.id.desc())
            )
        ]
        self.lang.choices = [(code, code) for code, options in current_app.config['LANGS'].items()]

    def validate_category_id(self, field):
        r = db.session.scalar(
            sa.select(NoteCategory).where(
                sa.and_(
                    NoteCategory.id == int(field.data),
                    NoteCategory.owner == current_user
                )
            )
        )

        # must change with name of selected category
        message = _l('category not exists')

        if not r:
            raise ValidationError(message)