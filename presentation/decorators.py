from functools import wraps
from flask import request, jsonify, g
from services.auth_service import AuthService
from exceptions import ExpiredTokenError, InvalidTokenError
from marshmallow import ValidationError as MarshmallowValidationError
import marshmallow


def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Требуется токен авторизации"})
        auth_token = auth_header[7:]
        try:
            user_id = AuthService.authentificate_token(auth_token)
            g.user_id = user_id
        except ExpiredTokenError:
            return jsonify({"error": "Токен просрочен"}), 401
        except InvalidTokenError:
            return jsonify({"error": "Неверный токен"}), 401
        return func(*args, **kwargs)
    return wrapper


def is_json_request(schema=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Ожидался JSON"}), 400

            if schema is not None:
                data = request.get_json()
                try:
                    validated_data = schema().load(data)
                except MarshmallowValidationError as e:
                    return jsonify({"error": e.messages}), 400
                return func(validated_data, *args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
