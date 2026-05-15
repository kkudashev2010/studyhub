from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort
from flask import request

from flask_login import login_required
from flask_login import current_user

from app import db
from app.models.post import Post
from app.forms.post_form import PostForm


posts_bp = Blueprint('posts', __name__)


# =========================
# СПИСОК + ПОИСК
# =========================
@posts_bp.route('/posts')
def posts():

    search = request.args.get('search')

    query = Post.query.order_by(Post.created_at.desc())

    if search:

        query = query.filter(
            (Post.title.ilike(f"%{search}%")) |
            (Post.subject.ilike(f"%{search}%")) |
            (Post.description.ilike(f"%{search}%"))
        )

    posts = query.all()

    return render_template(
        'posts.html',
        posts=posts,
        search=search
    )


# =========================
# ДЕТАЛЬ ПОСТА
# =========================
@posts_bp.route('/post/<int:post_id>')
def post_detail(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template(
        'post_detail.html',
        post=post
    )


# =========================
# СОЗДАНИЕ ПОСТА
# =========================
@posts_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():

    form = PostForm()

    if form.validate_on_submit():

        file = form.file.data
        filename = None

        if file and file.filename:

            from werkzeug.utils import secure_filename
            import os
            from flask import current_app

            filename = secure_filename(file.filename)

            upload_folder = os.path.join(
                current_app.root_path,
                'static/uploads'
            )

            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

        post = Post(
            title=form.title.data,
            subject=form.subject.data,
            description=form.description.data,
            file_path=filename,
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        flash('Материал опубликован!', 'success')

        return redirect(url_for('posts.posts'))

    return render_template('create_post.html', form=form)


# =========================
# РЕДАКТИРОВАНИЕ
# =========================
@posts_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():

        post.title = form.title.data
        post.subject = form.subject.data
        post.description = form.description.data

        db.session.commit()

        flash('Материал обновлён!', 'success')

        return redirect(url_for('posts.post_detail', post_id=post.id))

    form.title.data = post.title
    form.subject.data = post.subject
    form.description.data = post.description

    return render_template(
        'edit_post.html',
        form=form
    )


# =========================
# УДАЛЕНИЕ
# =========================
@posts_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash('Материал удалён!', 'info')

    return redirect(url_for('posts.posts'))