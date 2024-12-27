from . import bp
from flask import render_template, flash, redirect, url_for, request
from flask_babel import _
from flask_login import login_required, current_user
from .forms import PostForm
from app import db
from app.models import Post

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
    paginated_posts = db.paginate(current_user.posts.select().order_by(Post.id.desc()), page=page, per_page=1)

    return render_template('home.html', title=_('Home'), form=form, paginated_posts=paginated_posts)