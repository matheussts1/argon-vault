from .main import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'User: "{self.user}"'
    
class Secrets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(100), nullable=False)
    user_log = db.Column(db.String(100), nullable=False)
    encrypted_content = db.Column(db.Text, nullable=False)
    iv_content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Service: '{self.service}', User: {self.user_log}, Password: {self.encrypted_content}, IV: {self.iv_content}"