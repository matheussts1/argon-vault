import os
import traceback
import sys

MAIN_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(MAIN_FILE_DIR)

from flask import Flask
from extensions import data_base, login_manager, limiter
from data_base_config import database_path, connection_to_url, local_db_connection

app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')))

if database_path:
   app.config['SQLALCHEMY_DATABASE_URI'] = connection_to_url(database_path)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = local_db_connection()

from routes import main_bp 

try:
    data_base.init_app(app)
    with app.app_context():
        data_base.create_all()

except Exception as e:
    traceback.print_exc()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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