import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone
from typing import Optional
from markdown import markdown
from markdown.extensions.toc import TocExtension

class Note(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    body: so.Mapped[str] = so.mapped_column(sa.Text())
    body_html: so.Mapped[str] = so.mapped_column(sa.Text)
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('note_category.id'))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    lang: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[Optional[datetime]]

    category: so.Mapped['NoteCategory'] = so.relationship(back_populates='notes')
    author: so.Mapped['User'] = so.relationship(back_populates='notes')
    files: so.WriteOnlyMapped['File'] = so.relationship(back_populates='note')
    
    @staticmethod
    def body_changed(target, value, oldvalue, initiator):
        md = markdown(value, output_format='html', 
            extensions=[
                'pymdownx.emoji',
                'pymdownx.mark',
                'pymdownx.keys',
                'pymdownx.tilde',
                'pymdownx.caret',
                'extra', 
                'codehilite', 
                'admonition',
                ##TocExtension(permalink="&#128279;"),
            ]
        )
        
        # if initiator.key == 'body':
        target.body_html = md 

db.event.listen(Note.body, 'set', Note.body_changed)
