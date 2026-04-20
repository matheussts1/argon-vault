import base64
import models

from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from extensions import db, ph, limiter, csp, lm
from flask_login import current_user, login_user, logout_user, login_required
from form_validation import RegisterForm, LoginForm, PasswordsForm, DeleteForm
from sqlalchemy.exc import IntegrityError
from argon2.exceptions import VerifyMismatchError

main_bp = Blueprint('main', __name__)

@main_bp.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = csp
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@lm.user_loader
def load_user(user_id):
    return models.Users.query.get(int(user_id))

@main_bp.route("/", methods=["GET"])
def home_page():
    return render_template("home/homepage.html")

@main_bp.route("/argonvault", methods=["GET", "POST"])
def web_site():
    form_login = LoginForm()
    form_passwords = PasswordsForm()
    form_delete = DeleteForm()

    senhas_usuario = []

    if current_user.is_authenticated:
        senhas_usuario = models.Secrets.query.filter_by(user_id=current_user.id).all()
    
    return render_template("main/app.html",
                           login_form=form_login,
                           add_form=form_passwords,
                           delete_form=form_delete,
                           content=senhas_usuario)

@main_bp.route("/register", methods=["GET", "POST"])
#@limiter.limit("20 per hour")
def create_login():
    form = RegisterForm()

    if request.method == "POST":
        dados = request.get_json()
        form = RegisterForm(data=dados)

        user = dados.get('user')

        hash_recebido = dados.get('password')
        hash_bytes = bytes.fromhex(hash_recebido)

        salt = dados.get('salt')
        salt_bytes = base64.b64decode(salt)

        if not dados:
            return jsonify("message: Nenhum dado recebido"), 400

        if form.validate_on_submit():
            try:
                double_hash = ph.hash(hash_bytes, salt=salt_bytes)
                new_user = models.Users(
                    user=user, password=double_hash, salt=salt)
                db.session.add(new_user)
                db.session.commit()
        
                return jsonify(message="Sucesso"), 201
        
            except IntegrityError:
                db.session.rollback()
                return jsonify(message="Usuário ja existe"), 400
        else:
            return jsonify(errors=form.errors), 400
            
    return render_template("main/register.html", form=form)

@main_bp.route('/get-salt-login', methods=['GET'])
def get_salt():
    username = request.args.get('username')
    user = models.Users.query.filter_by(user=username).first()
    
    if user:
        return jsonify({"salt": user.salt}), 200
    else:
        return jsonify({"salt": "88a025044d4135a8c12603a447d832e4"}), 400
    
@main_bp.route('/get-salt-crypto', methods=['GET'])
def get_salt_crypto():
    usuario = request.args.get('usuario')
    user = models.Users.query.filter_by(user=usuario).first()
    
    if user:
        return jsonify({"salt": user.salt}), 200
    else:
        return jsonify({"salt": "df2ae307fff614da5649ff5ced16642f"}), 400

@main_bp.route("/login", methods=["GET", "POST"])
#@limiter.limit("20 per hour")
def auth_login():
    form = LoginForm()
    user = None

    if request.method == 'POST':
        dados = request.get_json()
        form = LoginForm(data=dados)

        user = models.Users.query.filter_by(user=form.usuario.data).first()

        if not user:
            return jsonify("Usuario não existe"), 404

        senha_banco = user.password

        hash = dados.get('hash').strip()
        hash_bytes = bytes.fromhex(hash)

    if form.validate_on_submit():
        try:
            if user and ph.verify(senha_banco, hash_bytes):
                login_user(user)
                return jsonify("Usuario logado!"), 200

        except VerifyMismatchError:
            return jsonify("Usuario ou senha incorretos!"), 401 
    else:
        return jsonify(errors=form.errors), 400
    
    return jsonify("Não entrou em nenhum if")

@main_bp.route("/passwords", methods=["GET", "POST"])
@login_required
def passwords():
    form = PasswordsForm()

    if request.method == "POST":

        dados = request.get_json()
        form = PasswordsForm(data=dados)

        service = dados.get('service')
        usuario = dados.get('usuario_service')
        senha = dados.get('password_service')
        iv = dados.get('iv')

        if not dados:
            return jsonify({"error": "Nenhum dado recebido"}), 400
            
        if form.validate_on_submit():
            try:
                new_service = models.Secrets(service=service, user_log=usuario,
                                            encrypted_content=senha, iv_content=iv, user_id=current_user.id)
                db.session.add(new_service)
                db.session.commit()
                
                id_senha = new_service.id

                return jsonify({
                    "message": "Senha salva com sucesso",
                    "ID": id_senha
                }), 200

            except Exception as e:
                return jsonify(e)
        else:
            return jsonify(errors=form.errors), 400
    
    return jsonify("Não entrou em nada")

@main_bp.route("/delete", methods=["POST"])
@login_required
def deletar():
    form = DeleteForm()

    if request.method == "POST": 

        dados = request.get_json()
        form = DeleteForm(data=dados)

        id = dados.get("id_senha")

        if not dados:
            return jsonify("Nenhum dado recebido"), 400
        
        if form.validate_on_submit():
            try:
                id_apagar = db.session.get(models.Secrets, id)
                db.session.delete(id_apagar)
                db.session.commit()
                return jsonify("Id deletado com sucesso!"), 200

            except Exception as e:
                return jsonify(f"message: {e}")
        else: 
            return jsonify(errors=form.errors), 400

    return jsonify("Não entrou em nenhum if")

@main_bp.route("/logout")
@login_required
def logout():
    logout_user(current_user)
    return (redirect(url_for("web_site")))