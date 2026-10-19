"""Unit tests for validation logic and password hashing.

These tests exercise pure logic only - no MySQL connection is required,
so they run in any environment.
"""
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

import pytest
from werkzeug.security import check_password_hash, generate_password_hash

# The same rules implemented in routes/transactions.py and routes/auth.py,
# imported directly from the app package.
from app.routes.auth import EMAIL_RE, _valid_registration
from app.routes.transactions import _parse_common


# ---------------------------------------------------------------------------
# Registration validation (TC-02, TC-03)
# ---------------------------------------------------------------------------
class TestRegistrationValidation:
    def test_accepts_valid_registration(self):
        assert _valid_registration("Preethi", "preethi@example.com", "secret6") is None

    def test_rejects_missing_fields(self):
        assert _valid_registration("", "a@b.com", "secret6") is not None
        assert _valid_registration("Preethi", "", "secret6") is not None
        assert _valid_registration("Preethi", "a@b.com", "") is not None

    def test_rejects_invalid_email(self):
        for bad in ["foo@bar", "foo.bar@com", "plain", "@example.com", "user@.com"]:
            assert _valid_registration("P", bad, "secret6") is not None, bad

    def test_rejects_short_password(self):
        assert _valid_registration("P", "a@b.com", "abc12") is not None

    def test_accepts_minimum_password_length(self):
        assert _valid_registration("P", "a@b.com", "abc123") is None

    def test_email_regex_shape(self):
        assert EMAIL_RE.match("user.name+tag@sub.example.co")
        assert not EMAIL_RE.match("user@localhost")


# ---------------------------------------------------------------------------
# Transaction parsing (TC-09, TC-10, TC-13)
# ---------------------------------------------------------------------------
class TestTransactionParsing:
    def test_accepts_valid_amount_and_date(self):
        amount, date_str, error = _parse_common({"amount": "500.50", "date": "2026-09-15"})
        assert error is None
        assert amount == Decimal("500.50")
        assert date_str == "2026-09-15"

    def test_rejects_missing_fields(self):
        assert _parse_common({"amount": "", "date": "2026-09-15"})[2] is not None
        assert _parse_common({"amount": "10", "date": ""})[2] is not None

    def test_rejects_non_numeric_amount(self):
        assert _parse_common({"amount": "abc", "date": "2026-09-15"})[2] is not None

    def test_rejects_zero_amount(self):
        assert _parse_common({"amount": "0", "date": "2026-09-15"})[2] is not None

    def test_rejects_negative_amount(self):
        assert _parse_common({"amount": "-5", "date": "2026-09-15"})[2] is not None

    def test_rejects_non_finite_amount(self):
        assert _parse_common({"amount": "NaN", "date": "2026-09-15"})[2] is not None
        assert _parse_common({"amount": "Infinity", "date": "2026-09-15"})[2] is not None

    def test_rejects_more_than_two_decimal_places(self):
        assert _parse_common({"amount": "10.999", "date": "2026-09-15"})[2] is not None

    def test_rejects_amount_larger_than_database_precision(self):
        assert _parse_common({"amount": "100000000", "date": "2026-09-15"})[2] is not None

    def test_rejects_invalid_date(self):
        assert _parse_common({"amount": "10", "date": "31-02-2026"})[2] is not None
        assert _parse_common({"amount": "10", "date": "2026/09/15"})[2] is not None

    def test_accepts_iso_dates(self):
        _, date_str, error = _parse_common({"amount": "10", "date": "2026-02-28"})
        assert error is None
        datetime.strptime(date_str, "%Y-%m-%d")  # round-trip sanity


# ---------------------------------------------------------------------------
# Password hashing (NFR-01)
# ---------------------------------------------------------------------------
class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        hashed = generate_password_hash("secret6")
        assert hashed != "secret6"
        assert "secret6" not in hashed

    def test_correct_password_verifies(self):
        hashed = generate_password_hash("secret6")
        assert check_password_hash(hashed, "secret6") is True

    def test_wrong_password_fails(self):
        hashed = generate_password_hash("secret6")
        assert check_password_hash(hashed, "wrong") is False

    def test_salts_are_unique(self):
        assert generate_password_hash("x") != generate_password_hash("x")
