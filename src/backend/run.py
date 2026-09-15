"""Personal Expense Tracker - development entry point.

Usage:
    python src/backend/run.py

Requires MySQL credentials in a .env file at the project root
(see .env.example) and the database created via src/database/schema.sql.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
