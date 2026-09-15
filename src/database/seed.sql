-- ============================================================
-- Personal Expense Tracker - Seed Data (v1.0)
-- Apply after schema.sql:
--   mysql -u root -p < src/database/seed.sql
-- ============================================================

USE expense_tracker;

INSERT INTO Categories (CategoryName) VALUES
  ('Food'),
  ('Transport'),
  ('Shopping'),
  ('Rent'),
  ('Entertainment'),
  ('Medical'),
  ('Education')
AS new_row
ON DUPLICATE KEY UPDATE CategoryName = new_row.CategoryName;
