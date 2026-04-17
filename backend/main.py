import os
import sys

print("DEBUG: Iniciando boot do servidor...", file=sys.stderr)
print(f"DEBUG: DATABASE_URL existe? {'Sim' if os.getenv('DATABASE_URL') else 'Não'}", file=sys.stderr)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from flask import Flask
from extensions import db, lm, limiter 
from routes import main_bp 

app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')))

database_url = os.getenv('DATABASE_URL')

if database_url:
    print("EXISTE O DATABASE")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

else:
    bdbase = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(bdbase, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'user.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    db.init_app(app)
    print("DEBUG: db.init_app executado", file=sys.stderr)
    
    with app.app_context():
        db.create_all()
        print("DEBUG: Tabelas criadas/verificadas", file=sys.stderr)
except Exception as e:
    print(f"ERRO FATAL NO BANCO: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()

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

if __name__ == "__main__":
    app.run()