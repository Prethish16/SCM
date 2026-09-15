"""User account queries (register / login / profile)."""
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db


def get_user_by_email(email):
    """Return the user row for an email, or None."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Users WHERE Email = %s", (email,))
        return cur.fetchone()


def create_user(name, email, password):
    """Insert a new user with a hashed password; returns the new UserID."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Users (Name, Email, PasswordHash) VALUES (%s, %s, %s)",
            (name, email, generate_password_hash(password)),
        )
        return cur.lastrowid


def verify_login(email, password):
    """Return the user row if the email exists and password matches."""
    user = get_user_by_email(email)
    if user is None:
        return None
    if not check_password_hash(user["PasswordHash"], password):
        return None
    return user


def update_name(user_id, name):
    """Update a user's display name. Returns affected rowcount."""
    conn = get_db()
    with conn.cursor() as cur:
        return cur.execute(
            "UPDATE Users SET Name = %s WHERE UserID = %s", (name, user_id)
        )
