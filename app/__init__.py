from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from decouple import config

app = Flask(__name__)
db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()

#These imports are here to "solve" circular ImportError
from .models import User
from .views import page
from app.consts import LOGIN_REQUIRED_MESSAGE


def create_app(config):
    app.config.from_object(config)


    csrf.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = ".login"
    login_manager.login_message = LOGIN_REQUIRED_MESSAGE
    mail.init_app(app)

    app.register_blueprint(page)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app
