from extensions import data_base
from flask_login import UserMixin

class Users(data_base.Model, UserMixin):
    id = data_base.Column(data_base.Integer, primary_key=True)
    user = data_base.Column(data_base.String(50), nullable=False, unique=True)
    password = data_base.Column(data_base.String(255), nullable=False)
    salt = data_base.Column(data_base.String(255), nullable=False)

    def __repr__(self):
        return f'User: "{self.user}"'
    
class Secrets(data_base.Model):
    id = data_base.Column(data_base.Integer, primary_key=True)
    service = data_base.Column(data_base.String(100), nullable=False)
    user_log = data_base.Column(data_base.String(100), nullable=False)
    encrypted_content = data_base.Column(data_base.Text, nullable=False)
    iv_content = data_base.Column(data_base.Text, nullable=False)

    user_id = data_base.Column(data_base.Integer, data_base.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Service: '{self.service}', User: {self.user_log}, Password: {self.encrypted_content}, IV: {self.iv_content}"