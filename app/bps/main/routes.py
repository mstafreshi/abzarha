from . import bp
from flask import render_template
from flask_babel import _
from flask_login import login_required

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/')
def home():
    return render_template('home.html', title=_('Home'))