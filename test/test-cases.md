# Test Cases — Personal Expense Tracker (CI-07)

Traceability: each test case maps to a functional requirement (FR) in `docs/SRS/SRS.md`.
Automated cases are marked ✅ in the "Automated" column and implemented in `test/test_validation.py`.

| TC ID | Verifies | Description | Steps | Expected result | Automated |
|---|---|---|---|---|---|
| TC-01 | FR-01 | Successful registration | Register with name, valid email, 6+ char password | Account created; success flash; redirected to login | — |
| TC-02 | FR-01, FR-09 | Registration rejects short password | Register with 5-char password | Error "at least 6 characters"; account not created | ✅ (unit: validator) |
| TC-03 | FR-01, FR-09 | Registration rejects invalid email | Register with `foo@bar` (no TLD) | Error "valid email address"; account not created | ✅ (unit: validator) |
| TC-04 | FR-01 | Registration rejects duplicate email | Register twice with same email | Error "already exists"; second account not created | — |
| TC-05 | FR-02 | Successful login | Login with registered email + correct password | Redirect to dashboard; nav shows app links | — |
| TC-06 | FR-02 | Login rejects wrong password | Login with wrong password | Error "Invalid email or password." | ✅ (unit: verify_login logic requires DB — covered indirectly) |
| TC-07 | FR-03 | Logout | Click Logout while logged in | Session cleared; redirected to login | — |
| TC-08 | FR-04 | Add valid income | Add amount 500.50, source "Salary", today | Success flash; record visible in history | — |
| TC-09 | FR-09 | Reject zero/negative income | Submit amount 0 / -5 | Error "greater than zero"; record not saved | ✅ (unit: parser) |
| TC-10 | FR-09 | Reject non-numeric amount | Submit amount "abc" | Error "valid number"; record not saved | ✅ (unit: parser) |
| TC-11 | FR-05 | Add valid expense | Add amount 120, category Food, description, today | Success flash; record visible in history | — |
| TC-12 | FR-05 | Expense category defaults to General | Add expense leaving category blank | Record stored with category "General" | — |
| TC-13 | FR-09 | Reject invalid date | Submit date "31-02-2026" | Error "YYYY-MM-DD format"; record not saved | ✅ (unit: parser) |
| TC-14 | FR-06, FR-07 | Dashboard totals and balance | Add income 1000 + 500, expenses 300 + 200 | Income 1500.00, Expenses 500.00, Balance 1000.00; ≤5 recent rows | — |
| TC-15 | FR-08 | History ordering | Add records across several dates | Newest records first; income and expense rows interleaved by date | — |
| TC-16 | FR-10 | Database unavailable message | Stop MySQL, then attempt login | Friendly DB-unavailable flash; no stack trace shown | — |
| TC-17 | FR-02 | Unauthenticated access blocked | Open `/` while logged out | Redirected to login page | — |

## Notes
- Automated units cover input-validation logic without a database (TC-02/03/09/10/13); the remaining cases are exercised manually per this register during release testing, since they require a live MySQL instance.
- New FRs introduced in later versions (FR-11 …) must add test cases here in the same release.
