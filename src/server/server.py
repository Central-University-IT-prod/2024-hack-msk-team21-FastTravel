from loguru import logger
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, make_response
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, get_jwt
import os
from dotenv import load_dotenv

from src.logic.adapter import Adapter
from src.server.auth import handle_login, handle_registration
from src.server.handler import handle_add_event

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


log_file = os.path.join(log_dir, "server_{time}.log")
logger.add(log_file, format="{time} {level} {message}", level="INFO", rotation="10 MB", compression="zip")

load_dotenv(dotenv_path='./.env', verbose=True)

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/ping', methods=['GET'])
def ping():
    logger.info('Ping request received')
    return jsonify(ping='pong')

@app.route('/account')
@jwt_required()
def account():
    username = get_jwt_identity()
    logger.info(f'Account page accessed by user: {username}')
    return render_template('user_data.html', username=username)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, error = handle_login(data)
    if email:
        access_token = create_access_token(identity=email)
        set_access_cookies(make_response(), access_token)
        logger.info(f'User {email} logged in successfully')
        return jsonify(access_token=access_token)
    logger.warning(f'Login failed: {error}')
    return jsonify(error=error), 401

@app.route('/registration', methods=['POST'])
def registration():
    data = request.get_json()
    error = handle_registration(data)
    if error:
        logger.warning(f'Registration failed: {error}')
        return jsonify(error=error), 400
    else:
        logger.info('User registered successfully')
        return '', 200

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    logger.info('Expired token detected, redirecting to login')
    return redirect(url_for('login'))


@app.route('/activate', methods=['GET'])
def activate_account():
    email = request.args.get('email')
    activation_key = request.args.get('key')
    print(email, activation_key)
    if not email or not activation_key:
        return jsonify(error='Почта или ключ активации не предоставлены'), 400

    db = Adapter()
    user = db.sel_userdata_by_activation_key(email, activation_key)
    if not user:
        return jsonify(error='Неверная почта или ключ активации'), 400

    if user['is_active']:
        return jsonify(error='Аккаунт уже активирован'), 400

    db.update('users', 'is_active = TRUE', user['uuid'])
    return jsonify(message='Аккаунт успешно активирован'), 200

@app.route('/add_event', methods=['POST'])
@jwt_required()
def add_event():
    data = request.get_json()
    user_name = get_jwt_identity()
    logger.info(f'User {user_name} adding event')
    return jsonify(handle_add_event(data))


if __name__ == "__main__":
    logger.info('Starting server')
    app.run(debug=True)