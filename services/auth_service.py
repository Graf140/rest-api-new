#та же бизнес логика, только PyJWT. В отдельный файл выносил
#для того, чтобы потом свапнуться на flask-JWT
#начал на PyJWT по аналогии с SQLAlchemy: чтобы в принцип вникнуть

import jwt
import datetime
from flask import current_app, jsonify
from werkzeug.security import check_password_hash
from repositories.user import UserRepository
from exceptions import *


class AuthService:
    def authenticate_user(dto):
        user = UserRepository.get_user_by_name(dto.username)
        if not user:
            raise UserNotFoundError("Пользователь не найден")

        if not check_password_hash(user['password_hash'], dto.password):
            raise InvalidPasswordError("Неверный пароль")
        return user

    def generate_jwt_token(dto):
        payload = {
            'user_id': dto.user_id,
            'username': dto.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        secret_key = current_app.config['SECRET_KEY']
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    def authentificate_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError("Токен просрочен")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Неверный токен")