import sys
import os

from main import app

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIRECTORY)

database_url = os.getenv('DATABASE_URL')

if database_url:
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