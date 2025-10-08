from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import SessionLocal
from app.models.user import User
from sqlalchemy.exc import IntegrityError

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        with SessionLocal() as db:
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.add(user)
            try:
                db.commit()
                flash("Registration successful, please log in")
                return redirect(url_for("users.login"))
            except IntegrityError:
                db.rollback()
                flash("User with this email or username already exists")
                return redirect(url_for("users.register"))

    return render_template("user/register.html")
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with SessionLocal() as db:
            user = db.query(User).filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for("posts.list_posts"))

            
            flash("Invalid username or password")
            return redirect(url_for("users.login"))

    return render_template("user/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))