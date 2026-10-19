"""Dashboard route: totals, balance, recent transactions."""
from flask import Blueprint, render_template

from .. import db
from ..helpers import flash_db_error, get_current_user, login_required
from ..models import expenses, income

bp = Blueprint("dashboard", __name__)

RECENT_LIMIT = 5


@bp.route("/")
@login_required
def index():
    try:
        user = get_current_user()
        if user is None:
            return render_template("dashboard.html", user={}, total_income=0,
                                   total_expenses=0, balance=0,
                                   recent_transactions=[])
        inc_totals = income.totals(user["UserID"])
        exp_totals = expenses.totals(user["UserID"])
        recent_income = income.recent(user["UserID"], RECENT_LIMIT)
        recent_expenses = expenses.recent(user["UserID"], RECENT_LIMIT)
    except Exception:
        db.log_db_exception("DB failure loading dashboard")
        flash_db_error()
        user = {"Name": "there"}
        inc_totals = {"total_income": 0}
        exp_totals = {"total_expenses": 0}
        recent_income = []
        recent_expenses = []

    total_income = inc_totals["total_income"]
    total_expenses = exp_totals["total_expenses"]
    balance = total_income - total_expenses

    # Merge the two recent lists, newest date first.
    combined = (
        [{"type": "income", **row} for row in recent_income]
        + [{"type": "expense", **row} for row in recent_expenses]
    )
    combined.sort(key=lambda r: str(r["Date"]), reverse=True)
    recent_transactions = combined[:RECENT_LIMIT]

    return render_template(
        "dashboard.html",
        user=user,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        recent_transactions=recent_transactions,
    )
