#presentation layer, чисто маршруты

from flask import Flask, jsonify, request

from models.user import UserRepository
from services.user_service import UserService
from services.auth_service import authenticate_user, generate_jwt_token



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


    #нейронка порекомендовала удолить ловец. ПОЧЕМУ?(спросить)
    # @app.route("/", defaults={"path": ""})  # перенаправление всего
    # @app.route("/<path:path>")
    # def avtobus(path):
    #     return jsonify("success")