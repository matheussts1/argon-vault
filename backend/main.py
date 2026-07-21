import os
import traceback
import sys

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIRECTORY)

from flask import Flask
from extensions import data_base, login_manager, limiter

app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')))

from routes import main_bp 

try:
    data_base.init_app(app)

    with app.app_context():
        data_base.create_all()
except Exception as e:
    traceback.print_exc()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

login_manager.init_app(app)
limiter.init_app(app)
login_manager.login_view = 'main.auth_login'
app.register_blueprint(main_bp)

from routes import *

if __name__ == "__main__":
    app.run()