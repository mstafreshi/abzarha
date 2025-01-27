from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from typing import Optional

class File(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    path: so.Mapped[str] = so.mapped_column(sa.String(255))
    caption: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    post_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('post.id', ondelete='SET NULL'), index=True)
    note_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('note.id', ondelete='SET NULL'), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    owner: so.Mapped['User'] = so.relationship(back_populates='files')
    post: so.Mapped['Post'] = so.relationship(back_populates='files')
    note: so.Mapped['Note'] = so.relationship(back_populates='files')