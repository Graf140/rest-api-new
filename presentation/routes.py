#presentation layer, чисто маршруты

from flask import Flask, jsonify, request

from models.user import UserRepository
from services.user_service import UserService


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
        # if not request.is_json:
        #     return jsonify({"error": "Ожидался JSON"}), 400
        if not request.is_json:
            return jsonify({"error": "Ожидался JSON"}), 400

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        success = UserService.register_user(username, password, confirm_password)

    @app.route("/api/users/log/", methods=['POST'])
    def log_user():
        if not request.is_json:
            return jsonify({"error": "Ожидался JSON"}), 400

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Введите логин или пароль"})

        if UserService.login_user(username, password):
            return jsonify({"success": "Авторизация успешна"})
        else:
            return jsonify({"error": "Не существует пользователя с данным логином и паролем"})


    @app.route("/", defaults={"path": ""})  # перенаправление всего
    @app.route("/<path:path>")
    def avtobus(path):
        return jsonify("success")