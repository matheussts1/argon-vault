from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, InputRequired, EqualTo

class RegisterForm(FlaskForm):
    user = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[InputRequired(), EqualTo('confirm_password', message='As senhas nao coincidem!')])
    confirm_password = PasswordField('Confirme sua senha')
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[InputRequired()])
    submit = SubmitField('Entrar')

class PasswordsForm(FlaskForm):
    service = StringField('Serviço', validators=[DataRequired()])
    usuario_service = StringField('Usuario', validators=[DataRequired()])
    password_service = PasswordField('Senha', validators=[InputRequired()])
    submit = SubmitField('Adicionar')

class DeleteForm(FlaskForm):
    id_senha = HiddenField('ID')