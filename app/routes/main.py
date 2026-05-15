from flask import Blueprint
from flask import render_template
from flask_login import current_user

from app.models.user import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/profile/<int:user_id>')
def profile(user_id):

    user = User.query.get_or_404(user_id)

    return render_template(
        'profile.html',
        user=user
    )