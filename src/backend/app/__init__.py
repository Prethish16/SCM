"""Personal Expense Tracker - Flask application factory."""
from flask import Flask

from .config import Config, FRONTEND_DIR
from . import db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder=str(FRONTEND_DIR / "templates"),
        static_folder=str(FRONTEND_DIR / "static"),
    )
    app.config.from_object(Config)

    # Close the per-request MySQL connection when the request ends.
    app.teardown_appcontext(db.close_db)

    # Register blueprints.
    from .routes.auth import bp as auth_bp
    from .routes.dashboard import bp as main_bp
    from .routes.transactions import bp as txns_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(txns_bp)

    return app
