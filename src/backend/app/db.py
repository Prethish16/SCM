"""MySQL connection management for Flask."""
import pymysql
from flask import current_app, g

from .config import Config


def get_db():
    """Return a per-request PyMySQL connection (cached on flask.g)."""
    if "db" not in g:
        g.db = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
    return g.db


def close_db(_exc=None):
    """Close the request's DB connection if one was opened."""
    db_conn = g.pop("db", None)
    if db_conn is not None:
        db_conn.close()


def log_db_exception(message):
    """Log a database failure through the active Flask application."""
    current_app.logger.exception(message)
