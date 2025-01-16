import sqlalchemy as sa
from app import db
from wtforms.validators import ValidationError
from flask_babel import _

class Unique():
    def __init__(self, class_, message = None):
        self.class_ = class_
        self.message = message

    def __call__(self, form, field):
        message = self.message
        if not message:
            message = _('%(v)s already exists.', v=field.data)

        to_edit = None
        if form.id.data and int(form.id.data) > 0:
            to_edit = db.session.get(self.class_, int(form.id.data))

        finded = db.session.scalar(
            sa.select(self.class_).where(
                eval(f'self.class_.{field.name}') == field.data
            )
        )

        if (finded and not to_edit) or (finded and finded.id != to_edit.id):
            raise ValidationError(message)

