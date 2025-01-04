import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from typing import Optional

class Word(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    word: so.Mapped[str] = so.mapped_column(sa.String(128))
    meaning: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    pronunciation: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    lang_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('dict_lang.id'), index=True)
    lang: so.Mapped['DictLang'] = so.relationship(back_populates='words')
