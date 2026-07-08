from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from apps.users.forms import RegisteratinForm, LoginForm, UpdateProfileForm, FollowForm, PhoneRegisterationForm, CodeVerifyForm
from apps.users.models import User, Follow, Code
from apps.extentions import db, hashing, sms_api
from flask_login import login_user, current_user, logout_user, login_required
import random
import datetime
from config import Config
from werkzeug.utils import secure_filename
import os


blueprint = Blueprint("users", __name__)

@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisteratinForm()
    if form.validate_on_submit():
        hashed_password = hashing.hash_value(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You registerd successfully..!", "success")
        return redirect(url_for("home.home"))
    return render_template("users/register.html", form=form)

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user and hashing.check_value(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You logged in successfully..!", "success")
            next_page = request.args.get("next")
            return redirect(next_page if next_page else url_for("home.home"))
        else:
            flash("Email/Password is wrong", "danger")
    return render_template("users/login.html", form=form)

@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You loged out successfuly", "success")
    return redirect(url_for("home.home"))


@blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        file = request.files["profile_pic"]
        # if file.filename == "":
        #     flash("No selected file..!", "info")
        #     return redirect(url_for("users.profile"))
        if file and "." in file.filename and file.filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENTIONS:
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            current_user.profile_pic = "uploads/"+ filename
        db.session.commit()
        flash("Account updated", "info")
        return redirect(url_for("users.profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("users/profile.html", form=form)


@blueprint.route("/user/<int:user_id>")
def user_profile(user_id):
    user = db.get_or_404(User, user_id)
    form = FollowForm()
    following = False
    relation = db.session.execute(db.select(Follow).where(Follow.follower==current_user.id,
                                                          Follow.followed==user.id)).first()
    if relation:
        following = True
    return render_template("users/user_profile.html", user=user, form=form, following=following)


@blueprint.route("/follow/<int:user_id>", methods=["POST"])
@login_required
def follow(user_id):
    form = FollowForm()
    if form.validate_on_submit():
        user = db.get_or_404(User, user_id)
        if user == current_user:
            flash("You can not follow yourself..!", "info")
            return redirect(url_for("home.home"))
        relation = Follow(follower=current_user.id, followed=user.id)
        db.session.add(relation)
        db.session.commit()
        flash(f"You followed {user.email}..!", "success")
        return redirect(url_for("users.user_profile", user_id=user.id))
    return redirect(url_for("home.home"))


@blueprint.route("/unfollow/<int:user_id>", methods=["POST"])
@login_required
def unfollow(user_id):
    form = FollowForm()
    if form.validate_on_submit():
        user = db.get_or_404(User, user_id)
        if user == current_user:
            flash("You can not unfollow yourself..!")
            return redirect(url_for("home.home", "info"))
        relation = db.session.execute(db.select(Follow).where(Follow.follower==current_user.id,
                                                              Follow.followed==user.id)).scalar()
        db.session.delete(relation)
        db.session.commit()
        flash(f"You unfollowed {user.email}..!", "success")
        return redirect(url_for("users.user_profile", user_id=user.id))
    return redirect(url_for("home.home"))


@blueprint.route("/phone-register", methods=["GET", "POST"])
def phone_register():
    form = PhoneRegisterationForm()
    if form.validate_on_submit():
        rand_num = random.randint(1000, 9999)
        session["user_phone"] = form.phone.data
        params = {"sender": "", "receptor": form.phone.data, "message": rand_num}
        sms_api.sms_send(params)
        code = Code(number=rand_num, expire=datetime.datetime.now()+datetime.timedelta(minutes=10), phone=form.phone.data)
        db.session.add(code)
        db.session.commit()
        flash("We sent you a code..!", "info")
        return redirect(url_for("user.phone_verify"))
    return render_template("users/phone-register.html", form=form)


@blueprint.route("/phone-verify", methods=["GET", "POST"])
def phone_verify():
    form = CodeVerifyForm()
    user_phone = session.get("user_phone")
    code = db.session.execute(db.select(Code).where(phone=user_phone)).first()
    if form.validate_on_submit():
        if code.expire < datetime.datetime.now():
            flash("Expiration Error, Please try again..!", "danger")
            return redirect(url_for('users.phone_register'))
        if form.code.data != str(code.number):
            flash("Your code is wrong..!", "danger")
        else:
            user = User(phone=user_phone)
            db.session.add(user)
            db.session.commit()
            flash("You registerd successfully..!", "success")
            return redirect(url_for("home.home"))    
    return render_template("users/phone-verify.html", form=form)
