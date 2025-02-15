from . import bp
from flask import render_template, flash, redirect, url_for, current_app
from flask_babel import _
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app import db
from app.email import send_reset_password_email
import sqlalchemy as sa

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(
                sa.or_(
                    User.username == form.username_or_email.data, User.email == form.username_or_email.data
                )
            )
        )
        print(form.password.data)
        if not user or not user.check_password(form.password.data):
            flash(_('Invalid username(email) or password'))
            return redirect(url_for('.login'))

        login_user(user, remember=form.remember_me.data)
        flash(_('login successful'), category='success')
        return redirect(url_for('main.home'))

    return render_template('login.html', title=_('login'), form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(_('User registered successfully'), category='success')
        return redirect(url_for('.login'))

    return render_template('register.html', title=_('Register'), form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_reset_password_email(user)

            flash(_('Email sent'))

        flash(_('Please check your email'))
        return redirect(url_for('.reset_password_request'))

    return render_template('reset_password_request.html', title=_('Reset password request'), form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.home'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Password reset successfully'))
        return redirect(url_for('.login'))

    return render_template('reset_password.html', title=_('Reset password'), form=form)