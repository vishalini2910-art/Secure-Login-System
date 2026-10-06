from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
import os
import re

app = Flask(__name__)

# In a real deployment, store this in an environment variable.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "change-this-development-secret-key"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


def valid_username(username):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,50}", username))


def valid_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
    )


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not valid_username(username):
            flash(
                "Username must be 3-50 characters and contain only "
                "letters, numbers, or underscore."
            )
            return render_template("register.html")

        if not valid_password(password):
            flash(
                "Password must be at least 8 characters and include "
                "uppercase, lowercase, and a number."
            )
            return render_template("register.html")

        # SQLAlchemy parameterizes database queries, helping prevent
        # SQL injection caused by directly concatenating user input.
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return render_template("register.html")

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, password_hash=password_hash)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session.get("username")
    )


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
