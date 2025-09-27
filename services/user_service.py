# Business Logic Layer
#для меня(проверка паролей, хеширование и валидация(пупупууу... валидацию добавить позже))

from werkzeug.security import generate_password_hash
from models.user import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash #также пароли


class UserService:
    @staticmethod
    def register_user(username, password, confirm_password):

        if not username or not password:
            raise ValueError("Имя пользователя и пароль обязательны")

        if password != confirm_password:
            raise ValueError("Пароли не совпадают")

        if UserRepository.user_exists(username):
            raise ValueError("Пользователь с таким именем уже существует")

        hashed_password = generate_password_hash(password)
        UserRepository.create_user(username, hashed_password)
        return True


    @staticmethod
    def authenticate_user(username, password):
        user = UserRepository.find_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            return True
        return False