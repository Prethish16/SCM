"""Authentication routes: register, login, logout."""
import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .. import db
from ..helpers import flash_db_error
from ..models import users

bp = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _valid_registration(name, email, password):
    """Return an error message for invalid registration input, else None."""
    if not name or not email or not password:
        return "All fields are required."
    if len(name) > 100 or len(email) > 255:
        return "Name or email is too long."
    if not EMAIL_RE.match(email):
        return "Please enter a valid email address."
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    return None


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        error = _valid_registration(name, email, password)
        if error:
            flash(error, "error")
            return render_template("register.html", name=name, email=email)

        try:
            if users.get_user_by_email(email):
                flash("An account with this email already exists.", "error")
                return render_template("register.html", name=name, email=email)
            users.create_user(name, email, password)
        except Exception:
            db.log_db_exception("DB failure during registration")
            flash_db_error()
            return render_template("register.html", name=name, email=email)

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html", email=email)

        try:
            user = users.verify_login(email, password)
        except Exception:
            db.log_db_exception("DB failure during login")
            flash_db_error()
            return render_template("login.html", email=email)

        if user is None:
            flash("Invalid email or password.", "error")
            return render_template("login.html", email=email)

        session.clear()
        session["user_id"] = user["UserID"]
        return redirect(url_for("dashboard.index"))

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
