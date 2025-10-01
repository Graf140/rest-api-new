#та же бизнес логика, только PyJWT. В отдельный файл выносил
#для того, чтобы потом свапнуться на flask-JWT
#начал на PyJWT по аналогии с SQLAlchemy: чтобы в принцип вникнуть

import jwt
import datetime
from flask import current_app
from werkzeug.security import check_password_hash
from models.user import UserRepository
from exceptions import UserNotFoundError, InvalidPasswordError, ValidationError

def authenticate_user(username, password):
    if not username or not password:
        raise ValidationError("Логин и пароль обязательны для заполнения")

    user = UserRepository.get_user_by_name(username)
    if not user:
        raise UserNotFoundError("Пользователь не найден")

    if not check_password_hash(user['password_hash'], password):
        raise InvalidPasswordError("Неверный пароль")

    return user

def generate_jwt_token(user_id, username):

    # Генерирует JWT-токен для авторизованного пользователя
    # Токен действителен 24 часа(шпорняк)

    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    secret_key = current_app.config['SECRET_KEY']
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token