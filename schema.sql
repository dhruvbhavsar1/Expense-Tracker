PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    note TEXT
);

CREATE TABLE IF NOT EXISTS Expense_Audit(
    Audit_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Expense_Id INTEGER,
    Action TEXT,
    Action_time TEXT,
    old_amt REAL,
    New_amt REAL,
    old_category TEXT,
    new_category TEXT
);

CREATE VIEW IF NOT EXISTS V_Total_By_Category AS
SELECT category,
       SUM(amount) AS Total_Amount,
       COUNT(*) AS Count_Items
FROM Expenses
GROUP BY category;

CREATE VIEW IF NOT EXISTS V_Monthly_Total AS
SELECT substr(date,1,7) AS month,
       SUM(amount) AS Total_amount
FROM Expenses
GROUP BY month
ORDER BY month DESC;

CREATE TRIGGER IF NOT EXISTS Trg_Expense_Update 
AFTER UPDATE ON Expenses
BEGIN 
  INSERT INTO Expense_Audit(Expense_Id, Action, Action_time, old_amt, New_amt, old_category, new_category)
  VALUES(NEW.id, 'UPDATE', datetime('now'), OLD.amount, NEW.amount, OLD.category, NEW.category);
END;

CREATE TRIGGER IF NOT EXISTS Trg_Expense_Delete
AFTER DELETE ON Expenses
BEGIN 
  INSERT INTO Expense_Audit(Expense_Id, Action, Action_time, old_amt, new_category, old_category)
  VALUES(OLD.id, 'DELETE', datetime('now'), OLD.amount, NULL, OLD.category);
END;
