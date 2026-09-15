"""Transaction routes: add income, add expense, view history."""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .. import db
from ..helpers import flash_db_error, get_current_user, login_required
from ..models import expenses, income

bp = Blueprint("transactions", __name__)

DEFAULT_CATEGORY = "General"


def _parse_common(form):
    """Validate shared fields; returns (amount, date_str, error)."""
    raw_amount = form.get("amount", "").strip()
    raw_date = form.get("date", "").strip()

    if not raw_amount or not raw_date:
        return None, None, "Amount and date are required."

    try:
        amount = Decimal(raw_amount)
    except InvalidOperation:
        return None, None, "Amount must be a valid number."

    if amount <= 0:
        return None, None, "Amount must be greater than zero."

    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
    except ValueError:
        return None, None, "Date must be in YYYY-MM-DD format."

    return amount, raw_date, None


@bp.route("/income/add", methods=["GET", "POST"])
@login_required
def add_income():
    user = get_current_user()

    if request.method == "POST":
        amount, date_str, error = _parse_common(request.form)
        source = request.form.get("source", "").strip()

        if error is None and not source:
            error = "Source is required."

        if error:
            flash(error, "error")
            return render_template("income_add.html", form=request.form)

        try:
            income.add_income(user["UserID"], amount, source, date_str)
        except Exception:
            db.get_app().logger.exception("DB failure adding income")
            flash_db_error()
            return render_template("income_add.html", form=request.form)

        flash("Income added successfully.", "success")
        return redirect(url_for("transactions.add_income"))

    form = {"amount": "", "source": "", "date": date.today().isoformat()}
    return render_template("income_add.html", form=form)


@bp.route("/expense/add", methods=["GET", "POST"])
@login_required
def add_expense():
    user = get_current_user()

    if request.method == "POST":
        amount, date_str, error = _parse_common(request.form)
        category = request.form.get("category", "").strip() or DEFAULT_CATEGORY
        description = request.form.get("description", "").strip()

        if error:
            flash(error, "error")
            return render_template("expense_add.html", form=request.form)

        try:
            expenses.add_expense(user["UserID"], amount, category, description, date_str)
        except Exception:
            db.get_app().logger.exception("DB failure adding expense")
            flash_db_error()
            return render_template("expense_add.html", form=request.form)

        flash("Expense added successfully.", "success")
        return redirect(url_for("transactions.add_expense"))

    form = {
        "amount": "",
        "category": "",
        "description": "",
        "date": date.today().isoformat(),
    }
    return render_template("expense_add.html", form=form)


@bp.route("/history")
@login_required
def history():
    user = get_current_user()

    try:
        income_rows = income.income_history(user["UserID"])
        expense_rows = expenses.expense_history(user["UserID"])
    except Exception:
        db.get_app().logger.exception("DB failure loading history")
        flash_db_error()
        income_rows, expense_rows = [], []

    transactions = (
        [{"type": "income", "id": r["IncomeID"], **r} for r in income_rows]
        + [{"type": "expense", "id": r["ExpenseID"], **r} for r in expense_rows]
    )
    transactions.sort(
        key=lambda r: (str(r["Date"]), r["id"]), reverse=True
    )

    return render_template("history.html", transactions=transactions)
