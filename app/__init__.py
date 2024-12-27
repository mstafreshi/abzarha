from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

babel = Babel()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    babel.init_app(app)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.bps.main import bp as main_bp
    from app.bps.auth import bp as auth_bp
    from app.bps.errors import bp as errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(errors_bp)

    return app

from app.models import User