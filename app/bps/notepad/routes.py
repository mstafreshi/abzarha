from flask import render_template, flash, redirect, url_for, request, g, current_app
from . import bp
from app.models import NoteCategory, Note, File
from .forms import CategoryForm, NoteForm
from app.bps.main.forms import UploadForm
from app import db
import sqlalchemy as sa
from flask_login import current_user, login_required
from flask_babel import _
import os
from werkzeug.utils import secure_filename

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/categories', methods=['GET', 'POST'])
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        category = NoteCategory(name=form.name.data)
        category.owner = current_user
        db.session.add(category)
        db.session.commit()
        flash(_('Category added successfully'))
        return redirect(url_for('.categories'))

    rows = db.session.scalars(
        sa.select(NoteCategory).where(
            NoteCategory.owner == current_user
        ). order_by(NoteCategory.id.desc())
    )
    return render_template('categories.html', rows=rows, form=form)

@bp.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = db.first_or_404(
        sa.select(NoteCategory).where(
            sa.and_(
                NoteCategory.id == int(id),
                NoteCategory.owner == current_user
            )
        )
    )

    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash(_('Category editted successfully.'))
        return redirect(url_for('.edit_category', id=id))
    return render_template('edit_category.html', form=form)

@bp.route('/notes')
def notes():
    notes = db.paginate(
        sa.select(Note).where(Note.author == current_user).order_by(Note.id.desc()),
        page = g.page,
        per_page = g.per_page
    )

    return render_template('notes.html', paginated=notes)

@bp.route('/add_note', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note()
        note.title = form.title.data
        note.body = form.body.data
        note.author = current_user
        note.lang = form.lang.data
        note.category_id = form.category_id.data
        db.session.add(note)
        db.session.commit()
        flash(_('Note added successfully.'))
        return redirect(url_for('.add_note'))

    return render_template('add_note.html', form=form)

@bp.route('/edit_note/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = db.session.scalar(
        sa.select(Note).where(sa.and_(Note.id == id, Note.author == current_user))
    )

    if not note:
        abort(404)

    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        note.lang = form.lang.data
        note.category_id = form.category_id.data
        db.session.commit()
        flash(_('Note editted successfully'))
        return redirect(url_for('.edit_note', id=id))

    upload_form = UploadForm()
    return render_template('edit_note.html', note=note, form=form, upload_form=upload_form)