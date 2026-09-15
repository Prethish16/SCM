"""Income record queries."""
from ..db import get_db


def add_income(user_id, amount, source, date):
    """Insert an income record; returns the new IncomeID."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Income (UserID, Amount, Source, Date) VALUES (%s, %s, %s, %s)",
            (user_id, amount, source, date),
        )
        return cur.lastrowid


def income_history(user_id):
    """All income records for a user, newest first."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT IncomeID, Amount, Source, Date FROM Income "
            "WHERE UserID = %s ORDER BY Date DESC, IncomeID DESC",
            (user_id,),
        )
        return cur.fetchall()


def totals(user_id):
    """Return {'total_income': ...} for the user's records."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(SUM(Amount), 0) AS t FROM Income WHERE UserID = %s", (user_id,))
        row = cur.fetchone()
        return {"total_income": row["t"]}


def recent(user_id, limit):
    """The user's most recent income records."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT Amount, Source, Date FROM Income "
            "WHERE UserID = %s ORDER BY Date DESC, IncomeID DESC LIMIT %s",
            (user_id, limit),
        )
        return cur.fetchall()
