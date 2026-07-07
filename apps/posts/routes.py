from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
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


@blueprint.route("/post/<int:post_id>")
def detail(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template("posts/detail.html", post=post)


@blueprint.route("/post/delete/<int:post_id>")
@login_required
def delete(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted..!", "success")
    return redirect(url_for("home.home"))


@blueprint.route("/post/update/<int:post_id>", methods=["GET", "POST"])
@login_required
def update(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    update_form = CreatePostForm()
    if update_form.validate_on_submit():
        post.title = update_form.title.data
        post.body = update_form.body.data
        db.session.commit()
        flash("post updated..!", "success")
        return redirect(url_for("posts.detail", post_id=post.id))
    elif request.method == "GET":
        update_form.title.data = post.title
        update_form.body.data = post.body
    return render_template("posts/update.html", form=update_form)