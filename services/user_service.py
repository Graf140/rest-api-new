# Business Logic Layer
#для меня(проверка паролей, хеширование и валидация(пупупууу... валидацию добавить позже))

from repositories.user import UserRepository
from werkzeug.security import generate_password_hash #также пароли
from exceptions import *


class UserService:
    @staticmethod
    def register_user(dto):
        hashed_password = generate_password_hash(dto.password)
        UserRepository.create_user(dto.username, hashed_password)  # Может выбросить UserAlreadyExistsError
        #эту ошибку добавили в обработку
        return True

    @staticmethod
    def get_user_profile(dto):
        user = UserRepository.get_user_by_id(dto.user_id)
        if not user:
            raise UserNotFoundError("Пользователь не найден")
        return {
            "id": user['user_id'],
            "username": user['name']
        }