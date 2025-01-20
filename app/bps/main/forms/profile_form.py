from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import Length, ValidationError
from flask_babel import lazy_gettext as _l
from flask import current_app

class ProfileForm(FlaskForm):
    name = StringField(_l('Name'), validators=[Length(max=128)])
    lang = SelectField(_l('Language'), coerce=str)
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=280)])
    per_page = IntegerField(_l('Per page'))
    submit = SubmitField(_l('Submit'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang.choices = [(code, code) for code, options in current_app.config['LANGS'].items()]

    def validate_per_page(self, field):
        data = int(field.data)

        if data <= 0:
            raise ValidationError(_l('This field must be greater than zero'))