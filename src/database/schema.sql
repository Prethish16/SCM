-- ============================================================
-- Personal Expense Tracker - Database Schema (v1.0)
-- CI-06: SQL Scripts
--
-- Apply with:
--   mysql -u root -p < src/database/schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS expense_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE expense_tracker;

-- ------------------------------------------------------------
-- Users
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Users (
  UserID       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  Name         VARCHAR(100)  NOT NULL,
  Email        VARCHAR(255)  NOT NULL,
  PasswordHash VARCHAR(255)  NOT NULL,
  CreatedAt    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_users_email UNIQUE (Email)
) ENGINE = InnoDB;

-- ------------------------------------------------------------
-- Income
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Income (
  IncomeID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  UserID   INT UNSIGNED  NOT NULL,
  Amount   DECIMAL(10,2) NOT NULL,
  Source   VARCHAR(100)  NOT NULL,
  Date     DATE          NOT NULL,
  CONSTRAINT fk_income_user FOREIGN KEY (UserID)
    REFERENCES Users (UserID) ON DELETE CASCADE,
  CONSTRAINT chk_income_amount CHECK (Amount > 0),
  INDEX idx_income_user_date (UserID, Date)
) ENGINE = InnoDB;

-- ------------------------------------------------------------
-- Expenses (Category is plain text in v1.0; the FK to the
-- Categories table is planned for v2.0 as a schema evolution.)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Expenses (
  ExpenseID   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  UserID      INT UNSIGNED  NOT NULL,
  Category    VARCHAR(50)   NOT NULL DEFAULT 'General',
  Amount      DECIMAL(10,2) NOT NULL,
  Description VARCHAR(255)  NULL,
  Date        DATE          NOT NULL,
  CONSTRAINT fk_expense_user FOREIGN KEY (UserID)
    REFERENCES Users (UserID) ON DELETE CASCADE,
  CONSTRAINT chk_expense_amount CHECK (Amount > 0),
  INDEX idx_expense_user_date (UserID, Date)
) ENGINE = InnoDB;

-- ------------------------------------------------------------
-- Categories (created and seeded in v1.0 for forward-preparedness;
-- linked from Expenses in v2.0)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Categories (
  CategoryID   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  CategoryName VARCHAR(50) NOT NULL,
  CONSTRAINT uq_categories_name UNIQUE (CategoryName)
) ENGINE = InnoDB;
