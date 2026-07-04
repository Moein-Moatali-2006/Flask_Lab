from flask import Blueprint, render_template, redirect, url_for, flash
from apps.posts.forms import CreatePostForm
from flask_login import login_required, current_user
from apps.posts.models import Post
from apps.extentions import db


blueprint = Blueprint("posts", __name__)

@blueprint.route("/post/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created..!", "success")
        return redirect(url_for("home.home"))
    return render_template("posts/create_post.html", form=form)