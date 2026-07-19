import base64
import models

from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from extensions import data_base, password_hasher, limiter, content_security_policy, login_manager
from flask_login import current_user, login_user, logout_user, login_required
from form_validation import RegisterForm, LoginForm, PasswordsForm, DeleteForm
from sqlalchemy.exc import IntegrityError
from argon2.exceptions import VerifyMismatchError

main_bp = Blueprint('main', __name__)

@main_bp.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = content_security_policy
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@login_manager.user_loader
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

    user_passwords = []

    if current_user.is_authenticated:
        user_passwords = models.Secrets.query.filter_by(user_id=current_user.id).all()
    
    return render_template("main/app.html",
                           login_form=form_login,
                           add_form=form_passwords,
                           delete_form=form_delete,
                           content=user_passwords)

@main_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("20 per hour")
def create_login():
    form = RegisterForm()

    if request.method == "POST":
        data = request.get_json()
        form = RegisterForm(data=data)

        user = data.get('user')

        hash_from_front = data.get('password')
        hash_bytes = bytes.fromhex(hash_from_front)

        salt = data.get('salt')
        salt_bytes = base64.b64decode(salt)

        if not data:
            return jsonify("message: No data received"), 400

        if form.validate_on_submit():
            try:
                double_hash = password_hasher.hash(hash_bytes, salt=salt_bytes)
                new_user = models.Users(
                    user=user, password=double_hash, salt=salt)
                data_base.session.add(new_user)
                data_base.session.commit()
        
                return jsonify(message="Success"), 201
        
            except IntegrityError:
                data_base.session.rollback()
                return jsonify(message="User already exists"), 400
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
    user = request.args.get('usuario')
    user_from_db = models.Users.query.filter_by(user=user).first()
    
    if user_from_db:
        return jsonify({"salt": user_from_db.salt}), 200
    else:
        return jsonify({"salt": "df2ae307fff614da5649ff5ced16642f"}), 400

@main_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("20 per hour")
def auth_login():
    form = LoginForm()
    user = None

    if request.method == 'POST':
        data = request.get_json()
        form = LoginForm(data=data)

        user = models.Users.query.filter_by(user=form.usuario.data).first()

        if not user:
            return jsonify("User dont exist"), 404

        password_from_db = user.password

        hash = data.get('hash').strip()
        hash_bytes = bytes.fromhex(hash)

    if form.validate_on_submit():
        try:
            if user and password_hasher.verify(password_from_db, hash_bytes):
                login_user(user)
                return jsonify("User logged!"), 200

        except VerifyMismatchError:
            return jsonify("User or password incorrect!"), 401 
    else:
        return jsonify(errors=form.errors), 400
    
    return jsonify("It did not enter any if statement.")

@main_bp.route("/passwords", methods=["GET", "POST"])
@login_required
def passwords():
    form = PasswordsForm()

    if request.method == "POST":

        data = request.get_json()
        form = PasswordsForm(data=data)

        service = data.get('service')
        usuario = data.get('usuario_service')
        senha = data.get('password_service')
        iv = data.get('iv')

        if not data:
            return jsonify({"error": "No data received"}), 400
            
        if form.validate_on_submit():
            try:
                new_service = models.Secrets(service=service, user_log=usuario,
                                            encrypted_content=senha, iv_content=iv, user_id=current_user.id)
                data_base.session.add(new_service)
                data_base.session.commit()
                
                password_id = new_service.id

                return jsonify({
                    "message": "Password saved successfully.",
                    "ID": password_id
                }), 200

            except Exception as e:
                return jsonify(e)
        else:
            return jsonify(errors=form.errors), 400
    
    return jsonify("It didn't get involved in anything.")

@main_bp.route("/delete", methods=["POST"])
@login_required
def delete():
    form = DeleteForm()

    if request.method == "POST": 

        data = request.get_json()
        form = DeleteForm(data=data)

        id = data.get("id_senha")

        if not data:
            return jsonify("No data received"), 400
        
        if form.validate_on_submit():
            try:
                id_for_delete = data_base.session.get(models.Secrets, id)
                data_base.session.delete(id_for_delete)
                data_base.session.commit()
                return jsonify("ID successfully deleted!"), 200

            except Exception as e:
                return jsonify(f"message: {e}")
        else: 
            return jsonify(errors=form.errors), 400

    return jsonify("It did not enter any if statement")

@main_bp.route("/logout")
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        return jsonify(f"message: {e}"), 400
    
    return (redirect(url_for("main.web_site")))