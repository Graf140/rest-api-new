from repositories.user import UserRepository
from exceptions import *
from repositories.forum_post import ForumPost


class ForumService:
    @staticmethod
    def create_post(dto):

        if not UserRepository.get_user_by_id(dto.user_id):
            raise UserNotFoundError("Пользователь не найден")

        return ForumPost.create_post(dto.user_id,
                                     dto.title,
                                     dto.content)

    @staticmethod
    def get_all_posts():
        return ForumPost.get_all_posts()

    @staticmethod
    def get_post_by_id(dto):
        post = ForumPost.get_post_by_id(dto.post_id)
        if not post:
            raise PostNotFoundError("Сообщение не найдено")
        return post
