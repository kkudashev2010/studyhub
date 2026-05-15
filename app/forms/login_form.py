from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Email


class LoginForm(FlaskForm):

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Войти')