from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from apps.extentions import db
from apps.users.models import User

class RegisteratinForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Pasword", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = db.session.execute(db.Select(User).where(User.email==email.data)).scalar()
        if user:
            raise ValidationError("This email already exists..!") 


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Pasword", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Register")


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    email = EmailField("Email", validators=[DataRequired()])

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.execute(db.Select(User).where(User.email==email.data)).scalar()
            if user:
                raise ValidationError("This email already exists..!") 
            

class FollowForm(FlaskForm):
    submit = SubmitField("submit")