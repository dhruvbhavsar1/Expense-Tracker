# DB_manage.py
import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple

DB = "expenses.db"

def get_conn():
    return sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES)

def init_db(sql_file="schema.sql"):
    if Path(DB).exists():
        print(f"Using existing DB: {DB}")
    conn = get_conn()
    cur = conn.cursor()
    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()
    cur.executescript(sql)
    conn.commit()
    conn.close()

# Add a new expense record
def add_expense(category: str, amount: float, note: str = "") -> int:
    sql = "INSERT INTO Expenses(date, category, amount, note) VALUES (datetime('now'), ?, ?, ?)"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (category, amount, note))
    conn.commit()
    inserted_id = cur.lastrowid
    conn.close()
    return inserted_id

# list_expenses
def list_expenses(limit: int = 10) -> List[Tuple]:
    sql = "SELECT id, date, category, amount, note FROM Expenses ORDER BY date DESC LIMIT ?"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

# search_expenses
def search_expenses(keyword: str) -> List[Tuple]:
    like = f"%{keyword}%"
    sql = '''
       SELECT id, date, category, amount, note FROM Expenses
       WHERE category LIKE ? OR note LIKE ? OR date LIKE ?
       ORDER BY date DESC
    '''
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (like, like, like))
    rows = cur.fetchall()
    conn.close()
    return rows

# update_expense
def update_expense(eid: int, category: str, amount: float, note: str) -> None:
    sql = "UPDATE Expenses SET category = ?, amount = ?, note = ? WHERE id = ?"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (category, amount, note, eid))
    conn.commit()
    conn.close()

# Delete expense
def delete_expense(eid: int) -> None:
    sql = "DELETE FROM Expenses WHERE id = ?"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()
    conn.close()

# Read view for totals by category
def total_by_cat() -> List[Tuple]:
    sql = "SELECT category, Total_Amount, Count_Items FROM V_Total_By_Category ORDER BY Total_Amount DESC"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows
#check if ID exists
def eid_exist(eid):
    sql="SELECT 1 FROM Expenses WHERE id=?"
    conn=get_conn()
    cur=conn.cursor()
    cur.execute(sql,(eid,))
    rows=cur.fetchall()
    conn.close()
    return rows is not None