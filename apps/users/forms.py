from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from apps.extentions import db
from apps.users.models import User, Code

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
    profile_pic = FileField("Profile picture")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.execute(db.Select(User).where(User.email==email.data)).scalar()
            if user:
                raise ValidationError("This email already exists..!") 
            

class FollowForm(FlaskForm):
    submit = SubmitField("submit")


class PhoneRegisterationForm(FlaskForm):
    phone = StringField("Phone")

    def validate_phone(self, phone):
        code = db.session.execute(db.select(Code).where(Code.phone.data)).scalar()
        if code:
            db.session.delete(code)
            db.session.commit()

        user = db.session.execute(db.select(User).where(User.phone==phone.data)).first()
        if user:
            raise ValidationError("This user already exists..!")


class CodeVerifyForm(FlaskForm):
    code = StringField("Code")