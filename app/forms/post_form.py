from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Length

from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed


class PostForm(FlaskForm):

    title = StringField(
        'Название',
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    subject = StringField(
        'Предмет',
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    description = TextAreaField(
        'Описание',
        validators=[
            DataRequired()
        ]
    )

    file = FileField(
        'Файл (PDF, DOCX, TXT)',
        validators=[
            FileAllowed(
                ['pdf', 'docx', 'txt'],
                'Разрешены только PDF, DOCX, TXT'
            )
        ]
    )

    submit = SubmitField('Опубликовать')