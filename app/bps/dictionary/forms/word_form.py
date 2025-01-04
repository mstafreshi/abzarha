from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_babel import lazy_gettext as _l
import sqlalchemy as sa
from app import db
from app.models import Word

class WordForm(FlaskForm):
    word = StringField(_l('Word'), validators=[DataRequired(), Length(min=2, max=128)])
    pronunciation = StringField(_l('Pronunciation'), validators=[Length(min=0, max=255)])
    meaning = TextAreaField(_l('Meaning'))
    submit = SubmitField(_l('submit'))

    def __init__(self, model = None):
        super().__init__()
        self.model = model

    def validate_word(self, field):
        record = db.session.scalar(sa.select(Word).where(Word.word == field.data))

        if not self.model and record:
            raise ValidationError(_l('This word already exists.'))

        if record and self.model and self.model.word != record.word:
            raise ValidationError(_l('This word already exists.'))
