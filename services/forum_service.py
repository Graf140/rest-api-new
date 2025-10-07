from repositories.user import UserRepository
from werkzeug.security import generate_password_hash #также пароли
from exceptions import *
from repositories.forum_post import ForumPost

class ForumService:
    @staticmethod
    def create_post(user_id: int, title: str, content: str):
        # if not title or not content:
        #     raise ValidationError("Заголовок и содержание обязательны")

        if not UserRepository.get_user_by_id(user_id):
            raise UserNotFoundError("Пользователь не найден")

        return ForumPost.create_post(user_id, title, content)

    @staticmethod
    def get_all_posts():
        return ForumPost.get_all_posts()

    @staticmethod
    def get_post_by_id(post_id: int):
        post = ForumPost.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError("Сообщение не найдено")
        return post