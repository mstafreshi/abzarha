from . import bp
from flask import render_template, flash, redirect, url_for, request, current_app, g, send_from_directory
from flask_babel import _, get_locale
from flask_login import login_required, current_user
from .forms import PostForm, ProfileForm, UploadForm
from app import db
from app.models import Post, User, File, Note
from app.forms import EmptyForm
import sqlalchemy as sa
from datetime import datetime, timezone
from langdetect import detect
from werkzeug.utils import secure_filename
import os

@bp.app_context_processor
def inject_symbols_to_templates():
    return {'db': db}
    
@bp.before_app_request
def app_before_request():
    g.per_page = current_app.config.get('PER_PAGE', 10)

    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

        if int(current_user.per_page) > 0:
            g.per_page = current_user.per_page            

    g.page = int(request.args.get('page', 1))
    g.locale = str(get_locale())

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/', methods=['GET', 'POST'])
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text=form.text.data)
        post.lang_code = detect(post.text)
        post.author = current_user
        db.session.add(post)
        db.session.commit()
        flash(_('Post sent successfully'))
        return redirect(url_for('.home'))

    page = int(request.args.get('page', 1))
    paginated = db.paginate(sa.select(Post).order_by(Post.id.desc()), page=page, per_page=g.per_page)

    return render_template('home.html', title=_('Home'), form=form, paginated=paginated)

@bp.route('/profile/<username>')
def profile(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = int(request.args.get('page', 1))
    paginated = db.paginate(user.posts.select().order_by(Post.id.desc()), page=page, per_page=g.per_page)
    return render_template('profile.html', title=_('Profile'), user=user, paginated=paginated)

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.lang = form.lang.data
        current_user.per_page = int(form.per_page.data)
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Profile updated successfully.'))
        return redirect(url_for('.edit_profile'))
    return render_template('edit_profile.html', form=form)

@bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = db.first_or_404(sa.select(Post).where(sa.and_(Post.author == current_user, Post.id == id)))
    form = PostForm()
    if form.validate_on_submit():
        post.text = form.text.data
        post.lang_code = detect(post.text)
        db.session.commit()
        flash(_('Post editted successfully.'))
        return redirect(url_for('.edit_post', id=post.id))
    elif request.method == 'GET':
        form.text.data = post.text

    delete_form = EmptyForm()
    upload_form = UploadForm()

    return render_template('edit_post.html', title=_('Edit post'), post=post, form=form, delete_form=delete_form, upload_form=upload_form)

@bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    post = db.first_or_404(sa.select(Post).where(sa.and_(Post.author == current_user, Post.id == id)))
    db.session.delete(post)
    db.session.commit()
    flash(_('Post deleted successfully.'))
    return redirect(url_for('.home'))

@bp.route('/upload_file/<string:to>/<int:id>', methods=['POST'])
def upload_file(to, id):
    form = UploadForm()
    if not form.validate_on_submit():
        return render_template('_utilities/_form_errors.html', form=form)

    post = None
    note = None

    if to == 'post':
        post = db.first_or_404(
            sa.select(Post).where(
                sa.and_(
                    Post.id ==id,
                    Post.author == current_user
                )
            )
        )
        folder_id = post.id
        back_url = url_for('.edit_post', id=post.id)

    elif to == 'note':
        note = db.first_or_404(
            sa.select(Note).where(
                sa.and_(
                    Note.id == id,
                    Note.author == current_user
                )
            )
        )
        folder_id = note.id
        back_url = url_for('notepad.edit_note', id=note.id)

    else:
        return 'invalid target'

    file = request.files['file']
    if file.filename == '':
        return 'no file selected', 204

    path = os.path.join(
        current_app.config['POST_FILES_DIRECTORY'] if to == 'post' else current_app.config['NOTE_FILES_DIRECTORY'],
        str(current_user.id),
        str(folder_id)
    )

    if not os.path.exists(path):
       os.makedirs(path)

    filename = secure_filename(file.filename)
    full_path = os.path.join(path, filename)

    file.save(full_path)

    file = File()
    file.post = post if post else None
    file.note = note if note else None
    file.path = full_path[4:]
    file.caption = form.caption.data
    file.owner = current_user
    db.session.add(file)
    db.session.commit()

    flash(_('File uploaded successfully.'))
    return redirect(back_url)

@bp.route('/image/<int:id>')
def image(id):
    file = db.get_or_404(File, id)
    
    if file.owner != current_user:
        abort(404)

    return send_from_directory(os.path.dirname(file.path), os.path.basename(file.path))