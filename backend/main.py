import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from flask import Flask
from extensions import db, lm, limiter 

print("DEBUG 1: Iniciando script", file=sys.stderr)
app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')))

database_url = os.getenv('DATABASE_URL')
print(f"Database URL: {database_url}")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("DEBUG 3: Configurado para POSTGRES", file=sys.stderr)
else:
    bdbase = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(bdbase, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'user.db')
    print("DEBUG 3: Configurado para SQLITE", file=sys.stderr)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from routes import main_bp 

try:
    db.init_app(app)
    print("DEBUG 4: db.init_app concluído", file=sys.stderr)
    
    with app.app_context():
        print(f"DEBUG 5: URI dentro do contexto: {app.config['SQLALCHEMY_DATABASE_URI'][:15]}...", file=sys.stderr)
        db.create_all()
        print("DEBUG 6: db.create_all finalizado", file=sys.stderr)
except Exception as e:
    import traceback
    print("DEBUG ERRO: Falha ao inicializar o banco de dados: ", {e})
    traceback.print_exc()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

lm.init_app(app)
limiter.init_app(app)
lm.init_app(app)
lm.login_view = 'main.auth_login'
app.register_blueprint(main_bp)

from .routes import *

if __name__ == "__main__":
    app.run()