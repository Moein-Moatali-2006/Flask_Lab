from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreatePostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(min=4, max=250)])
    body = TextAreaField("body", validators=[DataRequired()])
    