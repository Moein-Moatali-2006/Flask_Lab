from flask import Blueprint, render_template
from apps.users.forms import RegisteratinForm, LoginForm


blueprint = Blueprint("users", __name__)

@blueprint.route("/register")
def register():
    form = RegisteratinForm()
    return render_template("users/register.html", form=form)

@blueprint.route("/login")
def login():
    form = LoginForm()
    return render_template("users/login.html", form=form)