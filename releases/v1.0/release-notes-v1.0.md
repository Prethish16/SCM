# Release Notes — Personal Expense Tracker v1.0.0

**Tag:** `v1.0.0` · **Date:** 2026-09-15 · **Type:** Initial release

## Overview
First baseline of the Personal Expense Tracker. Users can register, log in, record income and expenses, and see their balance and transaction history.

## New Features
- **User management (FR-01 … FR-03):** registration with unique email, login with hashed-password verification, logout.
- **Income recording (FR-04):** add income with amount, source, and date.
- **Expense recording (FR-05):** add expense with amount, category (defaults to *General*), optional description, and date.
- **Dashboard (FR-06, FR-07):** total income, total expenses, remaining balance, five most recent transactions.
- **History (FR-08):** complete combined transaction list, newest first.
- **Validation (FR-09):** positive numeric amounts, ISO dates, email shape, 6+ character passwords; form values preserved on error.
- **Resilience (FR-10):** friendly message instead of a stack trace when MySQL is unreachable.

## Known Limitations
- Transactions cannot be edited or deleted yet (planned v1.1).
- Expense categories are free text; the managed `Categories` table is linked in v2.0.
- Password reset arrives in v2.1.

## Compatibility
- Python 3.10+, Flask 3.x, MySQL 8.x
- Database schema: `src/database/schema.sql` (run before first use; `seed.sql` optional)

## Verification
- `pytest test/` — 20 automated checks pass (validation + hashing; TC-02/03/09/10/13 automated).
- Manual register TC-01 … TC-17 executed against MySQL 8.0.
