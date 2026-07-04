from flask import Blueprint, render_template, redirect, url_for, flash
from apps.posts.forms import CreatePostForm
from flask_login import login_required, current_user
from apps.posts.models import Post
from apps.extentions import db


blueprint = Blueprint("posts", __name__)

@blueprint.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = CreatePostForm()
    return render_template()