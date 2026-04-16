from main import app, db
from models import Secrets

with app.app_context():
    db.session.query(Secrets).delete()
    db.session.commit()
        