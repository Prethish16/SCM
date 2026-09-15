# Class Diagram — Personal Expense Tracker (CI-03)

Reflects the **v1.0** implementation (Flask + PyMySQL, function-oriented modules).

```mermaid
classDiagram
    direction LR

    class FlaskApp {
        +create_app() Flask
        +register blueprints
        +teardown close_db
    }

    class Config {
        +SECRET_KEY
        +MYSQL_HOST
        +MYSQL_PORT
        +MYSQL_USER
        +MYSQL_PASSWORD
        +MYSQL_DB
    }

    class Db {
        +get_db() Connection
        +close_db(exc)
    }

    class UsersModel {
        +get_user_by_email(email) dict?
        +create_user(name, email, password) int
        +verify_login(email, password) dict?
        +update_name(user_id, name) int
    }

    class IncomeModel {
        +add_income(user_id, amount, source, date) int
        +income_history(user_id) list
        +totals(user_id) dict
        +recent(user_id, limit) list
    }

    class ExpensesModel {
        +add_expense(user_id, amount, category, description, date) int
        +expense_history(user_id) list
        +totals(user_id) dict
        +recent(user_id, limit) list
    }

    class AuthRoutes {
        +register()
        +login()
        +logout()
    }

    class DashboardRoutes {
        +index()
    }

    class TransactionRoutes {
        +add_income()
        +add_expense()
        +history()
    }

    class Helpers {
        +login_required(view)
        +get_current_user() dict?
        +flash_db_error()
    }

    class User {
        +UserID : int
        +Name : str
        +Email : str
        +PasswordHash : str
    }

    class Income {
        +IncomeID : int
        +UserID : int
        +Amount : Decimal
        +Source : str
        +Date : date
    }

    class Expense {
        +ExpenseID : int
        +UserID : int
        +Category : str
        +Amount : Decimal
        +Description : str
        +Date : date
    }

    FlaskApp --> Config : reads
    FlaskApp --> Db : teardown
    FlaskApp --> AuthRoutes
    FlaskApp --> DashboardRoutes
    FlaskApp --> TransactionRoutes
    AuthRoutes --> UsersModel
    DashboardRoutes --> IncomeModel
    DashboardRoutes --> ExpensesModel
    TransactionRoutes --> IncomeModel
    TransactionRoutes --> ExpensesModel
    AuthRoutes --> Helpers
    DashboardRoutes --> Helpers
    TransactionRoutes --> Helpers
    UsersModel --> Db
    IncomeModel --> Db
    ExpensesModel --> Db
    UsersModel --> User : maps rows
    IncomeModel --> Income : maps rows
    ExpensesModel --> Expense : maps rows
```

## Notes
- Route modules are Flask blueprints; models are plain query modules over PyMySQL `DictCursor` rows.
- Session state holds only `user_id`; the user row is re-fetched per request (`get_current_user`).
- Future versions add classes (e.g. `Category`, `Budget`, `ReportExporter`) without changing this structure — extension points are the `models` and `routes` packages.
