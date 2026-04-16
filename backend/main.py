import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from argon2 import PasswordHasher
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
limiter = Limiter(
    get_remote_address,
    app=app,
)

csp = (
    "default-src 'self'; "
    "style-src 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
    "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
    "script-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'wasm-unsafe-eval'; " 
    "worker-src 'self'; "
    "img-src 'self' data:; "
)

bdbase = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(bdbase, 'instance', 'user.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth_login'

ph = PasswordHasher(
    hash_len=32,
    time_cost=3,
    memory_cost=65536,
    parallelism=4
    )

from .routes import *


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()