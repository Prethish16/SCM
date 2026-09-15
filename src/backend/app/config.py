"""Application configuration.

Credentials and secrets come from environment variables, optionally loaded
from a .env file at the project root (never committed - see .env.example).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent          # src/backend/app
BACKEND_DIR = APP_DIR.parent                       # src/backend
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"     # src/frontend
PROJECT_ROOT = BACKEND_DIR.parent.parent           # repository root

load_dotenv(PROJECT_ROOT / ".env")


class Config:
    """Flask + MySQL configuration values."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "expense_tracker")
