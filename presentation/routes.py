#presentation layer, чисто маршруты

from flask import Flask, jsonify, request, current_app
from models.user import UserRepository
from services.user_service import UserService
from services.auth_service import authenticate_user, generate_jwt_token
import jwt
from exceptions import UserNotFoundError


#-----------------------Rest API-------------------------
def register_routes(app):
    @app.route("/api/users/all/", methods=['GET'])
    def get_all_users():
        users = UserRepository.get_all_users()
        return jsonify(users)

    @app.route("/api/users/count/", methods=['GET'])
    def get_user_count():
        count = UserRepository.get_users_count()
        return jsonify({"count": str(count)})

    @app.route("/api/users/<username>/", methods=['GET'])
    def get_user_by_username(username):
        user = UserRepository.get_user_by_name(username)
        return jsonify(user)  # postman говорит, если пусто, то JSON ответ null

    @app.route("/api/users/<int:user_id>/", methods=['GET'])
    def get_user_by_id(user_id):
        user = UserRepository.get_user_by_id(user_id)
        return jsonify(user)  # также как и сверху

    @app.route("/api/users/exist_user/<username>/", methods=['GET'])
    def exist_user_by_username(username):
        result = UserRepository.user_exists(username)
        return jsonify(result)

    @app.route("/api/users/reg/", methods=['POST'])
    def add_user():
        if not request.is_json:
            return jsonify({"error": "Ожидался JSON"}), 400

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        UserService.register_user(username, password, confirm_password)

        return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201


    @app.route("/api/users/log/", methods=['POST'])
    def log_user():
        if not request.is_json:
            return jsonify({"error": "Ожидался JSON"}), 400
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = authenticate_user(username, password)
        token = generate_jwt_token(user_id=user['user_id'], username=user['name'])

        return jsonify({
            "message": "Авторизация успешна",
            "token": token,
            "user": {
                "id": user['user_id'],
                "username": user['name']
            }
        }), 200


#ШПОРА:
#пример запроса:    {Authorization: Bearer <jwt_токен>} - ну соответственно JSONчик с ключОм аавторизация, воот
#ща буду дергать через Postman
    @app.route("/api/profile", methods=['POST'])
    def get_profile():
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Требуется токен авторизации"})
        auth_token = auth_header[7:]
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Токен просрочен"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Неверный токен"}), 401

        try:
            profile = UserService.get_user_profile(user_id)
            return jsonify(profile)
        except UserNotFoundError:
            return jsonify({"error": "Пользователь не найден"}), 404