from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from app.database import SessionLocal
from app.models.post import Post
from flask_login import login_required, current_user
from app.models.rating import Rating

bp = Blueprint("posts", __name__, url_prefix="/posts")

@bp.route("/")
def list_posts():
    with SessionLocal() as db:
        posts = db.query(Post).all()
    return render_template("blog/index.html", posts=posts)

@bp.route("/<int:post_id>")
def view_post(post_id):
    with SessionLocal() as db:
        post = db.get(Post, post_id)
        if not post:
            abort(404)
        return render_template("blog/view_post.html", post=post)

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author_id = 1 
        
        with SessionLocal() as db:
            post = Post(title=title, content=content, author_id=current_user.id)
            db.add(post)
            db.commit()
        return redirect(url_for("posts.list_posts"))
    
    return render_template("blog/add_post.html")

@bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    with SessionLocal() as db:
        post = db.get(Post, post_id)
        if not post:
            abort(404)

        if post.author_id != current_user.id:
            flash("You are not allowed to edit this post")
            return redirect(url_for("posts.view_post", post_id=post.id))

        if request.method == "POST":
            post.title = request.form["title"]
            post.content = request.form["content"]
            db.commit()
            flash("Post updated successfully")
            return redirect(url_for("posts.view_post", post_id=post.id))

        return render_template("post/edit.html", post=post)
    
@bp.route("/<int:post_id>/rate", methods=["POST"])
def rate_post(post_id):
    rating = int(request.form["rating"])
    if rating < 1 or rating > 10:
        flash("Rating must be between 1 and 10")
        return redirect(url_for("posts.view_post", post_id=post_id))

    with SessionLocal() as db:
        post = db.get(Post, post_id)
        if not post:
            abort(404)

        if current_user.is_authenticated and post.author_id == current_user.id:
            flash("You cannot rate your own post")
            return redirect(url_for("posts.view_post", post_id=post.id))

        new_rating = Rating(post_id=post.id, value=rating)
        db.add(new_rating)
        db.commit()
        flash("Thanks for rating!")
        return redirect(url_for("posts.view_post", post_id=post.id))