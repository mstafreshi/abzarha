from . import bp
from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from flask_babel import _
from app import db

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/')
def settings_home():
    return render_template('settings_home.html')