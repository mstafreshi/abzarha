from flask import current_app, render_template
from flask_mail import Message
from app import mail

def send(subject, sender, recipients, body, html):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = body
    message.html = html
    mail.send(message)

def send_reset_password_email(user):
    token=user.get_reset_password_token()

    sender = current_app.config['ADMINS'][0]
    recipients = [user.email]
    subject = current_app.config['APP_NAME'] + ': reset password'
    body = render_template('reset_password_email.txt', user=user, token=token)
    html = render_template('reset_password_email.html', user=user, token=token)

    send(subject, sender, recipients, body, html)
