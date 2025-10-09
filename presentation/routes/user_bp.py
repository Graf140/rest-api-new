from flask import jsonify, g, Blueprint
from repositories.user import UserRepository
from services.user_service import UserService
from services.auth_service import AuthService
from presentation.decorators import jwt_required, is_json_request
from schemas.schemas import *
from dto.user_dto import *


user_bp = Blueprint('users', __name__, url_prefix='/api/users')

#-----------------no validation(так делю)--------------
#вопросииик: по логике между слоями

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


#-------------with validtation-------


@user_bp.route("/reg/", methods=['POST'])
@is_json_request(AddUserSchema)
def add_user(validated_data):
    dto = AddUserDTO(username=validated_data['username'], password=validated_data['password'])
    UserService.register_user(dto)

    return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201


@user_bp.route("/log/", methods=['POST'])
@is_json_request(LogUserSchema)
def log_user(validated_data):
    dto = LogUserDTO(username=validated_data['username'], password=validated_data['password'])

    user = AuthService.authenticate_user(dto)
    dto_jwt = GenJWTDTO(user_id=user['user_id'], username=user['name'])
    token = AuthService.generate_jwt_token(dto_jwt)

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
    dto = GetUserProfileDTO(user_id=g.user_id)
    profile = UserService.get_user_profile(dto)
    return jsonify(profile)