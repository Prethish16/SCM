# Software Requirements Specification — Personal Expense Tracker

| | |
|---|---|
| **Project** | Personal Expense Tracker |
| **Document** | SRS (CI-01) |
| **Version** | 1.0 |
| **Status** | Baseline for release v1.0 |
| **Scope** | Full product vision; requirements tagged per planned version |

---

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements of the **Personal Expense Tracker**, a web application that lets individuals record income and expenses, view their balance, and analyze spending habits. It is the primary configuration item (CI-01) baselined for release v1.0.

### 1.2 Scope
The application covers user management, income and expense recording, and a summary dashboard. Advanced analytics (charts, budgets, exports) and cloud features are planned for later releases (see §6 Versioned Requirements).

### 1.3 Definitions and Acronyms
| Term | Meaning |
|---|---|
| Transaction | An income or an expense record belonging to one user |
| Balance | Total income minus total expenses for a user |
| SCM | Software Configuration Management |
| CI | Configuration Item |

### 1.4 References
- Configuration Management Plan (`docs/SCM-Plan/ConfigurationManagementPlan.md`)
- Database design (CI-04, `docs/Design/ERDiagram.md`)
- Test cases (CI-07, `test/test-cases.md`)

---

## 2. Overall Description

### 2.1 Product Perspective
A standalone web application built with Flask (Python), MySQL, and server-rendered HTML/CSS. All data is per-user and private.

### 2.2 Target Users
- College students
- Working professionals
- Anyone who wants to manage personal finances

### 2.3 Product Features (summary)
- Account registration and login
- Income and expense recording with history
- Dashboard with totals and balance

### 2.4 Operating Environment
- Python 3.10+ with Flask 3.x
- MySQL 8.x server
- Any modern browser

### 2.5 Design Constraints
- Server-rendered pages (no client-side framework in v1.x)
- Passwords stored only as salted hashes (Werkzeug PBKDF2)
- Database credentials supplied via environment variables, never committed

---

## 3. Specific Requirements — v1.0 (Baseline)

### 3.1 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | The system shall allow a visitor to register with name, unique email, and password (min 6 chars). | Must |
| FR-02 | The system shall authenticate users by email and password and maintain a session. | Must |
| FR-03 | The system shall allow logged-in users to log out. | Must |
| FR-04 | The system shall allow users to add income records (amount, source, date). | Must |
| FR-05 | The system shall allow users to add expense records (amount, category, description, date). | Must |
| FR-06 | The system shall show the user's total income, total expenses, and remaining balance. | Must |
| FR-07 | The system shall show the user's five most recent transactions on the dashboard. | Should |
| FR-08 | The system shall show the user's complete transaction history, newest first. | Must |
| FR-09 | The system shall validate that amounts are positive numbers and dates are valid. | Must |
| FR-10 | The system shall show a friendly message when the database is unavailable. | Should |

### 3.2 Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | Passwords shall be stored hashed and never in plain text. |
| NFR-02 | All SQL access shall use parameterized queries (no string concatenation). |
| NFR-03 | Pages shall render correctly on screen widths from 360 px upward. |
| NFR-04 | A dashboard request shall complete in under 2 s with 10,000 transactions for a user. |
| NFR-05 | Flash messages shall clearly confirm success or explain user-input errors. |

### 3.3 Data Requirements
See CI-04 (ER diagram). Tables: `Users`, `Income`, `Expenses`, `Categories`.

---

## 4. External Interfaces
- **User interface:** HTML/CSS pages (login, register, dashboard, add income, add expense, history)
- **Software interface:** MySQL 8.x via PyMySQL
- **Communication:** HTTP over localhost (or LAN) with session cookies

---

## 5. Acceptance Criteria for v1.0
1. A new user can register and log in.
2. Income and expense records can be added and appear in history.
3. Dashboard totals and balance equal the sums of recorded transactions.
4. Invalid input (bad email, short password, zero/negative amount, bad date) is rejected with a clear message.
5. Test cases TC-01 … TC-15 in CI-07 pass.

---

## 6. Versioned Requirements (Planned)

### 6.1 v1.1 — Transaction Maintenance
| ID | Requirement |
|---|---|
| FR-11 | Edit an existing income or expense record. |
| FR-12 | Delete an existing income or expense record. |
| FR-13 | Improved validation and bug fixes from v1.0 feedback. |

### 6.2 v2.0 — Categories and Analysis
| ID | Requirement |
|---|---|
| FR-14 | Assign expenses to managed categories (FK to Categories table). |
| FR-15 | Search transactions by text. |
| FR-16 | Filter transactions by date range. |
| FR-17 | Monthly summary view. |

### 6.3 v2.1 — Profile and Recovery
| ID | Requirement |
|---|---|
| FR-18 | Password reset. |
| FR-19 | Profile management (edit name/email). |
| FR-20 | UI improvements. |

### 6.4 v3.0 — Budgets and Reports
| ID | Requirement |
|---|---|
| FR-21 | Budget planning per category. |
| FR-22 | Spending alerts when nearing/exceeding budget. |
| FR-23 | Charts and graphs. |
| FR-24 | Export reports (PDF/Excel). |

### 6.5 v4.0 — Cloud and Personalization
| ID | Requirement |
|---|---|
| FR-25 | Cloud backup. |
| FR-26 | Multi-device sync. |
| FR-27 | Dark mode. |
| FR-28 | Currency selection. |

---

## 7. Traceability
Functional requirements ↔ test cases mapping is maintained in `test/test-cases.md` (CI-07). Each FR listed in §3 and §6 has at least one corresponding test case for the version that implements it.
