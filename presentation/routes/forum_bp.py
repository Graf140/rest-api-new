from flask import jsonify, request, g, Blueprint
from repositories.user import UserRepository
from services.forum_service import ForumService
from services.user_service import UserService
from services.auth_service import AuthService
from exceptions import *
from presentation.decorators import jwt_required, is_json_request
from schemas.schemas import *
from dto.forum_dto import CreatePostDTO, GetForumPostDTO

forum_bp = Blueprint('posts', __name__, url_prefix='/api/forum/posts')


@forum_bp.route("/", methods=['GET'])
def get_forum_posts():
    data = ForumService.get_all_posts()
    return jsonify(data)


@forum_bp.route("/", methods=['POST'])
@jwt_required
@is_json_request(PutForumPostsSchema)
def put_forum_posts(validated_data):
    dto = CreatePostDTO(title=validated_data['title'], content=validated_data['content'], user_id=g.user_id)
    try:
        post = ForumService.create_post(dto)
        return jsonify(post), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@forum_bp.route("/<int:post_id>/", methods=['GET'])
def get_forum_post(post_id):
    try:
        dto = GetForumPostDTO(post_id=post_id)
        post = ForumService.get_post_by_id(dto)
        return jsonify(post)
    except PostNotFoundError as e:
        return jsonify({"error": str(e)}), 404
