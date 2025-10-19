from flask import Flask, render_template
from flask_login import LoginManager, current_user
from app.database import SessionLocal
from app.models.user import User
from app.controller import post, user
from app.config import settings

app = Flask(__name__)
app.secret_key = settings.secret_key

# Flask-Login
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as db:
        return db.get(User, int(user_id))

# Регистрируем блюпринты
app.register_blueprint(post.bp)
app.register_blueprint(user.bp)

@app.route("/")
def home():
    return render_template("base.html")

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.errorhandler(400)
def bad_request(error):
    return render_template("400.html"), 400


if __name__ == "__main__":
    app.run(debug=True)
