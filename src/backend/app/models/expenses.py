"""Expense record queries."""
from ..db import get_db


def add_expense(user_id, amount, category, description, date):
    """Insert an expense record; returns the new ExpenseID."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Expenses (UserID, Category, Amount, Description, Date) "
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, category, amount, description, date),
        )
        return cur.lastrowid


def expense_history(user_id):
    """All expense records for a user, newest first."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT ExpenseID, Category, Amount, Description, Date FROM Expenses "
            "WHERE UserID = %s ORDER BY Date DESC, ExpenseID DESC",
            (user_id,),
        )
        return cur.fetchall()


def totals(user_id):
    """Return {'total_expenses': ...} for the user's records."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(SUM(Amount), 0) AS t FROM Expenses WHERE UserID = %s", (user_id,))
        row = cur.fetchone()
        return {"total_expenses": row["t"]}


def recent(user_id, limit):
    """The user's most recent expense records."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT Category, Amount, Description, Date FROM Expenses "
            "WHERE UserID = %s ORDER BY Date DESC, ExpenseID DESC LIMIT %s",
            (user_id, limit),
        )
        return cur.fetchall()


def get_by_id(user_id, expense_id):
    """Return one expense record owned by the user, or None."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT ExpenseID, Category, Amount, Description, Date FROM Expenses "
            "WHERE ExpenseID = %s AND UserID = %s",
            (expense_id, user_id),
        )
        return cur.fetchone()


def update_expense(user_id, expense_id, amount, category, description, date):
    """Update one expense record owned by the user."""
    conn = get_db()
    with conn.cursor() as cur:
        return cur.execute(
            "UPDATE Expenses SET Amount = %s, Category = %s, Description = %s, Date = %s "
            "WHERE ExpenseID = %s AND UserID = %s",
            (amount, category, description, date, expense_id, user_id),
        )


def delete_expense(user_id, expense_id):
    """Delete one expense record owned by the user."""
    conn = get_db()
    with conn.cursor() as cur:
        return cur.execute(
            "DELETE FROM Expenses WHERE ExpenseID = %s AND UserID = %s",
            (expense_id, user_id),
        )
