# Business Logic Layer
#для меня(проверка паролей, хеширование и валидация(пупупууу... валидацию добавить позже))

from repositories.user import UserRepository
from werkzeug.security import generate_password_hash #также пароли
from exceptions import *


class UserService:
    @staticmethod
    def register_user(username, password):
        #!!!ДОБАВИЛ валидацию через marshmallow в presentation!!!(в next commit'е delete)

        # if not username or not password or not confirm_password:
        #     raise ValidationError("Все поля обязательны для заполнения")
        #
        # if password != confirm_password:
        #     raise InvalidPasswordError("Пароли не совпадают")

        hashed_password = generate_password_hash(password)
        UserRepository.create_user(username, hashed_password)  # Может выбросить UserAlreadyExistsError
        #эту ошибку добавили в обработку
        return True

    @staticmethod
    def get_user_profile(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("Пользователь не найден")
        return {
            "id": user['user_id'],
            "username": user['name']
        }