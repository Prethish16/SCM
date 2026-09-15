# User Manual — Personal Expense Tracker (v1.0)

Welcome to the Personal Expense Tracker. This manual explains how to install, run, and use version 1.0 of the application.

---

## 1. Requirements
- Python 3.10 or newer
- MySQL 8.x running locally (or any reachable MySQL server)
- A modern web browser

## 2. Installation

```bash
# 1. Create a virtual environment (from the project root)
python -m venv venv

# 2. Activate it
# Windows (PowerShell):
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 3. Database Setup

1. Create your environment file: copy `.env.example` to `.env` and fill in your MySQL password:
   ```
   MYSQL_USER=root
   MYSQL_PASSWORD=your-mysql-password-here
   ```
2. Create the schema and seed data (from the project root):
   ```bash
   mysql -u root -p < src/database/schema.sql
   mysql -u root -p < src/database/seed.sql
   ```
   The script creates the `expense_tracker` database with tables `Users`, `Income`, `Expenses`, `Categories`.

## 4. Running the Application

```bash
python src/backend/run.py
```

Then open **http://127.0.0.1:5000** in your browser. *(Screenshot placeholder: login page.)*

## 5. Using the App

### 5.1 Create an Account
1. Click **Register** on the login page.
2. Enter your name, a valid email, and a password of at least 6 characters.
3. You will be returned to the login page to sign in. *(Screenshot placeholder: registration form.)*

### 5.2 Log In / Log Out
- Enter your email and password and click **Log in**.
- Click **Logout** in the top navigation to end your session.

### 5.3 Add Income
1. Click **Add Income** in the navigation.
2. Enter the amount, a source (e.g. *Salary*, *Freelance*), and the date.
3. Click **Add income** — the record is saved and confirmed with a green message.

### 5.4 Add Expense
1. Click **Add Expense** in the navigation.
2. Enter the amount, an optional category (defaults to *General*), an optional description, and the date.
3. Click **Add expense**.

### 5.5 Dashboard
The home page shows **Total Income**, **Total Expenses**, **Remaining Balance**, and your **five most recent transactions**. *(Screenshot placeholder: dashboard.)*

### 5.6 Transaction History
Click **History** to see every income and expense record, newest first.

## 6. Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| "The database is unavailable right now." | MySQL is not running, or `.env` credentials are wrong. Check MySQL service and `.env` values. |
| "Access denied" when loading schema | Wrong MySQL password; re-run with the correct `-u` / `-p`. |
| Port 5000 already in use | Stop the other program or run on another port (`flask --app src.backend.run run --port 5001`). |
| Forgot a password | Password reset arrives in v2.1; for now, contact the administrator (delete/recreate the user in MySQL). |

## 7. Feature Roadmap
| Version | Theme |
|---|---|
| v1.1 | Edit and delete transactions |
| v2.0 | Categories, search, date filters, monthly summary |
| v2.1 | Password reset, profile management |
| v3.0 | Budgets, alerts, charts, PDF/Excel exports |
| v4.0 | Cloud backup, sync, dark mode, currency selection |
