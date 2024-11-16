from datetime import timedelta
import os
from flask_jwt_extended import create_access_token
from src.logic.adapter import Adapter
import bcrypt
from src.server.email import send_activation_email
import uuid

def generate_hash(password):
    password_bytes = password.encode("utf-8")
    password_salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_bytes, password_salt)
    return hash_bytes.decode("utf-8")

def check_password_hash(user_password, hash_password):
    return bcrypt.checkpw(user_password.encode("utf-8"), hash_password.encode("utf-8"))

def handle_login(data):
    error = None
    token = None
    password = data.get('password')
    email = data.get('email')
    if not password or not email:
        error = 'Пожалуйста, заполните все поля'
    else:
        db = Adapter()
        user = db.sel_userdata_by_email(email=email)
        del db
        if not user:
            error = 'Неверные учетные данные'
        elif check_password_hash(password, user['password']):
            token = create_access_token(identity=email)
        else:
            error = 'Неверные учетные данные'
    return token, error

def create_activation_token(email):
    return create_access_token(identity=email, expires_delta=timedelta(hours=24))

def handle_registration(data):
    error = None
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    forbidden_symbols = ["{", "}", "'", '"']

    if not name or not email or not password:
        error = 'Пожалуйста, заполните все поля'
    elif any(symbol in name for symbol in forbidden_symbols) or any(symbol in email for symbol in forbidden_symbols) or any(symbol in password for symbol in forbidden_symbols):
        error = 'Недопустимые символы в полях'
    else:
        db = Adapter()
        user = db.sel_userdata_by_email(email=email)
        if user:
            if not user['is_active']:
                db.delete_by_uuid('users', user['uuid'])
            else:
                error = "Пользователь с таким email уже существует"
        if not error:
            hashed_password = generate_hash(password)
            is_active = os.getenv('AUTO_APPROVE_ACCOUNTS', 'False').lower() in ['true', '1', 't', 'y', 'yes']
            activation_key = str(uuid.uuid4())
            db.insert_userdata_inDB(username=name, hashed_password=hashed_password, email=email, is_active=is_active, activation_key=activation_key)
            send_activation_email(email, activation_key)
        del db
    return error