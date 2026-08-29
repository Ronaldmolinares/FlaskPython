from flask import Blueprint, redirect, request, session, url_for
from models import User, db  # type: ignore[import-not-found]

users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        plain_password = request.form.get("password")

        if not username or not email or not plain_password:
            return "Faltan datos requeridos.", 400

        new_user = User(username=username, email=email, password=plain_password)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["username"] = new_user.username

        return redirect(url_for("notes.home"))

    return redirect(url_for("index"))


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password_attempt = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password_attempt):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("notes.home"))

        return "Usuario o contraseña incorrectos.", 401

    return redirect(url_for("index"))


@users_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
