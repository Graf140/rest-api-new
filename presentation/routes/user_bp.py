from flask import jsonify, request, g, Blueprint
from repositories.user import UserRepository
from services.forum_service import ForumService
from services.user_service import UserService
from services.auth_service import AuthService
from exceptions import *
from presentation.decorators import jwt_required, is_json_request
from schemas.schemas import *


user_bp = Blueprint('users', __name__, url_prefix='/api/users')

#-----------------no validation(так делю)--------------


@user_bp.route("/all/", methods=['GET'])
def get_all_users():
    users = UserRepository.get_all_users()
    return jsonify(users)


@user_bp.route("/count/", methods=['GET'])
def get_user_count():
    count = UserRepository.get_users_count()
    return jsonify({"count": str(count)})


@user_bp.route("/<username>/", methods=['GET'])
def get_user_by_username(username):
    user = UserRepository.get_user_by_name(username)
    return jsonify(user)  # postman говорит, если пусто, то JSON ответ null


@user_bp.route("/<int:user_id>/", methods=['GET'])
def get_user_by_id(user_id):
    user = UserRepository.get_user_by_id(user_id)
    return jsonify(user)  # также как и сверху


@user_bp.route("/exist_user/<username>/", methods=['GET']) #true или false
def exist_user_by_username(username):
    result = UserRepository.user_exists(username)
    return jsonify(result)


#-------------with validtation-------


@user_bp.route("/api/users/reg/", methods=['POST'])
@is_json_request(AddUserSchema)
def add_user(validated_data):
    username = validated_data['username']
    password = validated_data['password'] #т.к. пароли совпали, confirm_password удаляем

    UserService.register_user(username, password)

    return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201


@user_bp.route("/api/users/log/", methods=['POST'])
@is_json_request(LogUserSchema)
def log_user(validated_data):
    username = validated_data['username']
    password = validated_data['password']

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


#-----------------с проверкой JWT--------------------


@user_bp.route("/profile/", methods=['GET'])
@jwt_required
def get_profile():
    user_id = g.user_id
    profile = UserService.get_user_profile(user_id)
    return jsonify(profile)