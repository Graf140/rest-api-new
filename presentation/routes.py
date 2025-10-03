#presentation layer, чисто маршруты

from flask import jsonify, request, current_app
from models.user import UserRepository
from services.forum_service import ForumService
from services.user_service import UserService
from services.auth_service import AuthService
from exceptions import *


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

        user = AuthService.authentificate_user(username, password)
        token = AuthService.generate_jwt_token(user_id=user['user_id'], username=user['name'])

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
        user_id = AuthService.authentificate_token(auth_token)
        try:
            profile = UserService.get_user_profile(user_id)
            return jsonify(profile)
        except UserNotFoundError:
            return jsonify({"error": "Пользователь не найден"}), 404

#-----------------------Rest API, но добавляю форум-------------------------
    @app.route("/api/forum/posts/", methods=['GET'])
    def get_forum_posts():
        data = ForumService.get_all_posts()
        return jsonify(data)

    @app.route("/api/forum/posts/", methods=['POST'])
    def put_forum_posts():
        if not request.is_json:
            return jsonify({"error": "Ожидался JSON"}), 400

        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Требуется токен авторизации"}), 401

        auth_token = auth_header[7:]
        user_id = AuthService.authentificate_token(auth_token)

        try:
            post = ForumService.create_post(user_id, title, content)
            return jsonify(post), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except UserNotFoundError as e:
            return jsonify({"error": str(e)}), 404


    @app.route("/api/forum/posts/<int:post_id>/", methods=['GET'])
    def get_forum_post(post_id):
        try:
            post = ForumService.get_post_by_id(post_id)
            return jsonify(post)
        except PostNotFoundError as e:
            return jsonify({"error": str(e)}), 404