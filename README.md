# Personal Expense Tracker

A web application that helps students and professionals record income and expenses, categorize transactions, view their balance, and understand their spending habits — built as a **Software Configuration Management (SCM) semester project** with a documented release ladder from v1.0 to v4.0.

**Current release: v1.0** (baseline)

## Features (v1.0)
- User registration and login (salted password hashes)
- Add income (amount, source, date)
- Add expense (amount, category, description, date)
- Dashboard: total income, total expenses, remaining balance, 5 recent transactions
- Full transaction history, newest first
- Graceful "database unavailable" handling

## Technology Stack
| Layer | Technology |
|---|---|
| Backend | Python 3, Flask 3 |
| Database | MySQL 8 (PyMySQL driver) |
| Frontend | Jinja2 templates, HTML, CSS |
| Testing | pytest |
| SCM | Git & GitHub (tagged releases) |

## Project Structure
```
ExpenseTracker/
├── docs/                  # Configuration items (CI-01…CI-04, CI-08, CI-10)
│   ├── SRS/               # Software Requirements Specification
│   ├── Design/            # Use case, class, and ER diagrams
│   ├── SCM-Plan/          # Configuration Management Plan
│   └── User-Manual/       # End-user documentation
├── src/
│   ├── backend/           # Flask application (CI-05)
│   ├── frontend/          # Templates + static CSS
│   └── database/          # schema.sql, seed.sql (CI-06)
├── test/                  # Test cases + pytest suite (CI-07)
├── releases/              # Release notes per version (CI-09)
└── README.md
```

## Quick Start
```bash
# 1. Virtual environment
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux

# 2. Dependencies
pip install -r requirements.txt

# 3. Configure: copy .env.example to .env and set MYSQL_PASSWORD
# 4. Database
mysql -u root -p < src/database/schema.sql
mysql -u root -p < src/database/seed.sql

# 5. Run
python src/backend/run.py        # http://127.0.0.1:5000
```

## Tests
```bash
pytest test/
```
The automated suite covers input validation and password hashing without a database; the manual test register lives in `test/test-cases.md`.

## Documentation Index
| CI | Document |
|---|---|
| CI-01 | [SRS](docs/SRS/SRS.md) |
| CI-02 | [Use Case Diagram](docs/Design/UseCaseDiagram.md) |
| CI-03 | [Class Diagram](docs/Design/ClassDiagram.md) |
| CI-04 | [Database Design / ER](docs/Design/ERDiagram.md) |
| CI-06 | [SQL Scripts](src/database/schema.sql) |
| CI-07 | [Test Cases](test/test-cases.md) |
| CI-08 | [User Manual](docs/User-Manual/UserManual.md) |
| CI-09 | [Release Notes v1.0](releases/v1.0/release-notes-v1.0.md) |
| CI-10 | [Configuration Management Plan](docs/SCM-Plan/ConfigurationManagementPlan.md) |

## Release Roadmap
| Version | Theme |
|---|---|
| **v1.0** ✅ | Login, add income/expenses, balance, history |
| v1.1 | Edit/delete transactions, validation hardening |
| v2.0 | Categories, search, date filters, monthly summary |
| v2.1 | Password reset, profile management |
| v3.0 | Budgets, spending alerts, charts, PDF/Excel export |
| v4.0 | Cloud backup, multi-device sync, dark mode, currency |
