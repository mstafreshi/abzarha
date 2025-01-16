import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone

class NoteCategory(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    notes: so.WriteOnlyMapped['Note'] = so.relationship(back_populates='category')
    owner: so.Mapped['User'] = so.relationship(back_populates='note_categories')

sa.UniqueConstraint(NoteCategory.name, NoteCategory.user_id)