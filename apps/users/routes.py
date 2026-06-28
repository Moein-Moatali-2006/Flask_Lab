from flask import Blueprint, render_template, redirect, url_for, flash
from apps.users.forms import RegisteratinForm, LoginForm
from apps.users.models import User
from apps.extentions import db, hashing


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

@blueprint.route("/login")
def login():
    form = LoginForm()
    return render_template("users/login.html", form=form)