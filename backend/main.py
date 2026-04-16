import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from flask import Flask
from extensions import db, lm, limiter 
from routes import main_bp 

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')


bdbase = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(bdbase, 'instance', 'user.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

db.init_app(app)
lm.init_app(app)
limiter.init_app(app)
lm.init_app(app)
lm.login_view = 'main.auth_login'
app.register_blueprint(main_bp)

from .routes import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()