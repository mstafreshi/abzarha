from . import bp
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_babel import _
from flask_login import login_required, current_user
from .forms import PostForm, ProfileForm
from app import db
from app.models import Post, User
from app.forms import EmptyForm
import sqlalchemy as sa
from datetime import datetime, timezone

@bp.before_app_request
def app_before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/', methods=['GET', 'POST'])
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text=form.text.data)
        post.author = current_user
        db.session.add(post)
        db.session.commit()
        flash(_('Post sent successfully'))
        return redirect(url_for('.home'))

    page = int(request.args.get('page', 1))    
    paginated_posts = db.paginate(sa.select(Post).order_by(Post.id.desc()), page=page, per_page=current_app.config['PER_PAGE'])

    return render_template('home.html', title=_('Home'), form=form, paginated_posts=paginated_posts)

@bp.route('/profile/<username>')
def profile(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = int(request.args.get('page', 1))
    paginated_posts = db.paginate(user.posts.select().order_by(Post.id.desc()), page=page, per_page=current_app.config['PER_PAGE'])

    return render_template('profile.html', title=_('Profile'), user=user, paginated_posts=paginated_posts)

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Profile updated successfully.'))
        return redirect(url_for('.edit_profile'))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', form=form)

@bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = db.first_or_404(sa.select(Post).where(sa.and_(Post.author == current_user, Post.id == id)))
    form = PostForm()
    if form.validate_on_submit():
        post.text = form.text.data
        db.session.commit()
        flash(_('Post editted successfully.'))
        return redirect(url_for('.edit_post', id=post.id))
    elif request.method == 'GET':
        form.text.data = post.text

    delete_form = EmptyForm()
    return render_template('edit_post.html', title=_('Edit post'), post=post, form=form, delete_form=delete_form)

@bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    post = db.first_or_404(sa.select(Post).where(sa.and_(Post.author == current_user, Post.id == id)))
    db.session.delete(post)
    db.session.commit()
    flash(_('Post deleted successfully.'))
    return redirect(url_for('.home'))
