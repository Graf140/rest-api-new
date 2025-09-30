# Business Logic Layer
#для меня(проверка паролей, хеширование и валидация(пупупууу... валидацию добавить позже))

from werkzeug.security import generate_password_hash
from models.user import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash #также пароли
from exceptions import *


class UserService:
    @staticmethod
    def register_user(username, password, confirm_password):
        if not username or not password or not confirm_password:
            raise ValidationError("Все поля обязательны для заполнения")

        if password != confirm_password:
            raise InvalidPasswordError("Пароли не совпадают")

        hashed_password = generate_password_hash(password)
        UserRepository.create_user(username, hashed_password)  # Может выбросить UserAlreadyExistsError
        #эту ошибку добавили в обработку
        return True


    @staticmethod
    def login_user(username, password):
        if not username or not password:
            raise ValidationError("Логин и пароль обязательны")

        user = UserRepository.get_user_by_name(username)
        if not user:
            raise UserNotFoundError("Пользователь не найден")

        if not check_password_hash(user['password_hash'], password):
            raise InvalidPasswordError("Неверный пароль")

        return True