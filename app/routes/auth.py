from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app import db
from app.models.user import User

from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_username = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_username:

            flash(
                'Пользователь с таким именем уже существует',
                'danger'
            )

            return redirect(url_for('auth.register'))

        existing_email = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_email:

            flash(
                'Пользователь с таким email уже существует',
                'danger'
            )

            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(
            form.password.data
        )

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешна!', 'success')

        return redirect(url_for('auth.login'))

    return render_template(
        'register.html',
        form=form
    )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
                user.password_hash,
                form.password.data
        ):

            login_user(user)

            flash('Вы вошли в аккаунт!', 'success')

            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)

            return redirect(url_for('main.index'))

        else:

            flash(
                'Неверный email или пароль',
                'danger'
            )

    return render_template(
        'login.html',
        form=form
    )


@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()

    flash('Вы вышли из аккаунта', 'info')

    return redirect(url_for('main.index'))