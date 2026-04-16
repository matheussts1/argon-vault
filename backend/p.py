from extensions import db
from main import app
from models import Users, Secrets

with app.app_context():
    user_delete = db.session.get(Users, 2)
    senha_delete = db.session.get(Secrets, 1)

    db.session.delete(user_delete)
    db.session.delete(senha_delete)
    db.session.commit()