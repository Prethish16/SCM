"""Transaction routes: add income, add expense, view history."""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

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
    except (InvalidOperation, ValueError):
        return None, None, "Amount must be a valid number."

    if not amount.is_finite() or amount <= 0:
        return None, None, "Amount must be greater than zero."
    if amount.as_tuple().exponent < -2:
        return None, None, "Amount can have at most two decimal places."
    if amount > Decimal("99999999.99"):
        return None, None, "Amount is too large."

    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
    except ValueError:
        return None, None, "Date must be in YYYY-MM-DD format."

    return amount, raw_date, None


@bp.route("/income/add", methods=["GET", "POST"])
@login_required
def add_income():
    user = get_current_user()
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        amount, date_str, error = _parse_common(request.form)
        source = request.form.get("source", "").strip()

        if error is None and not source:
            error = "Source is required."
        elif error is None and len(source) > 100:
            error = "Source must be 100 characters or fewer."

        if error:
            flash(error, "error")
            return render_template("income_add.html", form=request.form)

        try:
            income.add_income(user["UserID"], amount, source, date_str)
        except Exception:
            db.log_db_exception("DB failure adding income")
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
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        amount, date_str, error = _parse_common(request.form)
        category = request.form.get("category", "").strip() or DEFAULT_CATEGORY
        description = request.form.get("description", "").strip()

        if len(category) > 50:
            error = "Category must be 50 characters or fewer."
        elif len(description) > 255:
            error = "Description must be 255 characters or fewer."
        if error:
            flash(error, "error")
            return render_template("expense_add.html", form=request.form)

        try:
            expenses.add_expense(user["UserID"], amount, category, description, date_str)
        except Exception:
            db.log_db_exception("DB failure adding expense")
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
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))

    try:
        income_rows = income.income_history(user["UserID"])
        expense_rows = expenses.expense_history(user["UserID"])
    except Exception:
        db.log_db_exception("DB failure loading history")
        flash_db_error()
        income_rows, expense_rows = [], []

    transactions = (
        [{"type": "income", "id": r["IncomeID"], **r} for r in income_rows]
        + [{"type": "expense", "id": r["ExpenseID"], **r} for r in expense_rows]
    )
    transactions.sort(
        key=lambda r: (str(r["Date"]), r["id"]), reverse=True
    )

    search = request.args.get("search", "").strip()
    transaction_type = request.args.get("type", "").strip().lower()
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()

    if search:
        search_lower = search.lower()
        transactions = [
            transaction for transaction in transactions
            if search_lower in " ".join(
                str(transaction.get(field, "") or "")
                for field in ("Source", "Category", "Description")
            ).lower()
        ]
    if transaction_type in {"income", "expense"}:
        transactions = [
            transaction for transaction in transactions
            if transaction["type"] == transaction_type
        ]
    if date_from:
        transactions = [
            transaction for transaction in transactions
            if str(transaction["Date"]) >= date_from
        ]
    if date_to:
        transactions = [
            transaction for transaction in transactions
            if str(transaction["Date"]) <= date_to
        ]

    filters = {
        "search": search,
        "type": transaction_type,
        "date_from": date_from,
        "date_to": date_to,
    }
    return render_template(
        "history.html",
        transactions=transactions,
        filters=filters,
        has_filters=any(filters.values()),
    )


@bp.route("/income/<int:income_id>/edit", methods=["GET", "POST"])
@login_required
def edit_income(income_id):
    user = get_current_user()
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))
    try:
        record = income.get_by_id(user["UserID"], income_id)
        if record is None:
            flash("Income record not found.", "error")
            return redirect(url_for("transactions.history"))
        if request.method == "POST":
            amount, date_str, error = _parse_common(request.form)
            source = request.form.get("source", "").strip()
            if error is None and not source:
                error = "Source is required."
            elif error is None and len(source) > 100:
                error = "Source must be 100 characters or fewer."
            if error:
                flash(error, "error")
                return render_template("income_edit.html", form=request.form)
            income.update_income(user["UserID"], income_id, amount, source, date_str)
            flash("Income updated successfully.", "success")
            return redirect(url_for("transactions.history"))
    except Exception:
        db.log_db_exception("DB failure editing income")
        flash_db_error()
        return redirect(url_for("transactions.history"))

    return render_template("income_edit.html", form=record)


@bp.post("/income/<int:income_id>/delete")
@login_required
def delete_income(income_id):
    user = get_current_user()
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))
    try:
        if income.delete_income(user["UserID"], income_id):
            flash("Income deleted successfully.", "success")
        else:
            flash("Income record not found.", "error")
    except Exception:
        db.log_db_exception("DB failure deleting income")
        flash_db_error()
    return redirect(url_for("transactions.history"))


@bp.route("/expense/<int:expense_id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    user = get_current_user()
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))
    try:
        record = expenses.get_by_id(user["UserID"], expense_id)
        if record is None:
            flash("Expense record not found.", "error")
            return redirect(url_for("transactions.history"))
        if request.method == "POST":
            amount, date_str, error = _parse_common(request.form)
            category = request.form.get("category", "").strip() or DEFAULT_CATEGORY
            description = request.form.get("description", "").strip()
            if len(category) > 50:
                error = "Category must be 50 characters or fewer."
            elif len(description) > 255:
                error = "Description must be 255 characters or fewer."
            if error:
                flash(error, "error")
                return render_template("expense_edit.html", form=request.form)
            expenses.update_expense(
                user["UserID"], expense_id, amount, category, description, date_str
            )
            flash("Expense updated successfully.", "success")
            return redirect(url_for("transactions.history"))
    except Exception:
        db.log_db_exception("DB failure editing expense")
        flash_db_error()
        return redirect(url_for("transactions.history"))

    return render_template("expense_edit.html", form=record)


@bp.post("/expense/<int:expense_id>/delete")
@login_required
def delete_expense(expense_id):
    user = get_current_user()
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))
    try:
        if expenses.delete_expense(user["UserID"], expense_id):
            flash("Expense deleted successfully.", "success")
        else:
            flash("Expense record not found.", "error")
    except Exception:
        db.log_db_exception("DB failure deleting expense")
        flash_db_error()
    return redirect(url_for("transactions.history"))
