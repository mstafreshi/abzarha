import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class DictLang(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    words: so.WriteOnlyMapped['Word'] = so.relationship(back_populates='lang')
