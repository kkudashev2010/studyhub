from flask import Blueprint
from flask import jsonify

from app.models.post import Post

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/posts', methods=['GET'])
def get_posts():

    posts = Post.query.order_by(
        Post.created_at.desc()
    ).all()

    return jsonify([
        {
            'id': post.id,
            'title': post.title,
            'subject': post.subject,
            'description': post.description,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%d.%m.%Y %H:%M'),
            'file': post.file_path
        }
        for post in posts
    ])


@api_bp.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):

    post = Post.query.get_or_404(post_id)

    return jsonify({
        'id': post.id,
        'title': post.title,
        'subject': post.subject,
        'description': post.description,
        'author': post.author.username,
        'created_at': post.created_at.strftime('%d.%m.%Y %H:%M'),
        'file': post.file_path
    })