#presentation layer, чисто маршруты

from flask import jsonify, request, g
from repositories.user import UserRepository
from services.forum_service import ForumService
from services.user_service import UserService
from services.auth_service import AuthService
from exceptions import *
from presentation.decorators import jwt_required, is_json_request
from schemas.schemas import *


#-----------------------Rest API-------------------------
# def register_routes(app):
#     @app.route("/api/users/all/", methods=['GET'])
#     def get_all_users():
#         users = UserRepository.get_all_users()
#         return jsonify(users)
#
#     @app.route("/api/users/count/", methods=['GET'])
#     def get_user_count():
#         count = UserRepository.get_users_count()
#         return jsonify({"count": str(count)})
#
#     @app.route("/api/users/<username>/", methods=['GET'])
#     def get_user_by_username(username):
#         user = UserRepository.get_user_by_name(username)
#         return jsonify(user)  # postman говорит, если пусто, то JSON ответ null
#
#     @app.route("/api/users/<int:user_id>/", methods=['GET'])
#     def get_user_by_id(user_id):
#         user = UserRepository.get_user_by_id(user_id)
#         return jsonify(user)  # также как и сверху
#
#     @app.route("/api/users/exist_user/<username>/", methods=['GET'])
#     def exist_user_by_username(username):
#         result = UserRepository.user_exists(username)
#         return jsonify(result)

#РАБОТА с валидацией через json
    # @app.route("/api/users/reg/", methods=['POST'])
    # @is_json_request(AddUserSchema)
    # def add_user(validated_data):
    #     username = validated_data['username']
    #     password = validated_data['password'] #т.к. пароли совпали, confirm_password удаляем
    #
    #     UserService.register_user(username, password)
    #
    #     return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201
    #
    #
    # @app.route("/api/users/log/", methods=['POST'])
    # @is_json_request(LogUserSchema)
    # def log_user(validated_data):
    #     username = validated_data['username']
    #     password = validated_data['password']
    #
    #     user = AuthService.authentificate_user(username, password)
    #     token = AuthService.generate_jwt_token(user_id=user['user_id'], username=user['name'])
    #
    #     return jsonify({
    #         "message": "Авторизация успешна",
    #         "token": token,
    #         "user": {
    #             "id": user['user_id'],
    #             "username": user['name']
    #         }
    #     }), 200


#ШПОРА:
#пример запроса:    {Authorization: Bearer <jwt_токен>} - ну соответственно JSONчик с ключОм аавторизация, воот
    # @app.route("/api/profile/", methods=['GET'])
    # @jwt_required
    # def get_profile():
    #     user_id = g.user_id
    #     profile = UserService.get_user_profile(user_id)
    #     return jsonify(profile)

#-----------------------Rest API, но добавляю форум-------------------------
# @app.route("/api/profile/", methods=['GET'])
# @jwt_required
# def get_profile():
#     user_id = g.user_id
#     profile = UserService.get_user_profile(user_id)
#     return jsonify(profile)

    # @app.route("/api/forum/posts/", methods=['GET'])
    # def get_forum_posts():
    #     data = ForumService.get_all_posts()
    #     return jsonify(data)
    #
    # @app.route("/api/forum/posts/", methods=['POST'])
    # @jwt_required
    # @is_json_request(PutForumPostsSchema)
    # def put_forum_posts(validated_data):
    #
    #     title = validated_data['title']
    #     content = validated_data['content']
    #     user_id = g.user_id
    #
    #     try:
    #         post = ForumService.create_post(user_id, title, content)
    #         return jsonify(post), 201
    #     except ValidationError as e:
    #         return jsonify({"error": str(e)}), 400
    #     except UserNotFoundError as e:
    #         return jsonify({"error": str(e)}), 404
    #
    #
    # @app.route("/api/forum/posts/<int:post_id>/", methods=['GET'])
    # def get_forum_post(post_id):
    #     try:
    #         post = ForumService.get_post_by_id(post_id)
    #         return jsonify(post)
    #     except PostNotFoundError as e:
    #         return jsonify({"error": str(e)}), 404