"""Shared helpers: DB error handling and request-scoped user lookups."""
from functools import wraps

from flask import flash, redirect, session, url_for

from .db import get_db

# Friendly, non-leaking message used whenever the database is unreachable
# or a query fails unexpectedly.
DB_ERROR_MSG = (
    "The database is unavailable right now. "
    "Please make sure MySQL is running and try again."
)


def flash_db_error():
    """Flash the friendly database-unavailable message."""
    flash(DB_ERROR_MSG, "error")


def login_required(view):
    """Redirect unauthenticated visitors to the login page."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def get_current_user():
    """Return the logged-in user's row as a dict, or None."""
    if "user_id" not in session:
        return None
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT UserID, Name, Email FROM Users WHERE UserID = %s",
            (session["user_id"],),
        )
        return cur.fetchone()


def _execute(statement, params):
    """Run a single statement and return the affected rowcount."""
    conn = get_db()
    with conn.cursor() as cur:
        return cur.execute(statement, params)
