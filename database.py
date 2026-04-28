import sqlite3
import os
import numpy as np
from datetime import date

DB_PATH = "attendance.db"
FACE_DATA_DIR = "face_data"

def init_db():
    os.makedirs(FACE_DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        department TEXT,
        designation TEXT,
        phone TEXT,
        email TEXT,
        face_encoding BLOB,
        registered_on TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT NOT NULL,
        date TEXT NOT NULL,
        check_in TEXT,
        status TEXT DEFAULT 'Present',
        UNIQUE(emp_id, date)
    )''')
    conn.commit()
    conn.close()

def add_employee(emp_id, name, department, designation, phone, email, face_encoding):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    encoding_bytes = face_encoding.tobytes() if face_encoding is not None else None
    try:
        c.execute('''INSERT INTO employees 
            (emp_id, name, department, designation, phone, email, face_encoding, registered_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (emp_id, name, department, designation, phone, email, 
             sqlite3.Binary(encoding_bytes) if encoding_bytes else None,
             date.today().isoformat()))
        conn.commit()
        return True, "Employee registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Employee ID already exists!"
    finally:
        conn.close()

def get_all_employees():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT emp_id, name, department, designation, phone, email, face_encoding FROM employees")
    rows = c.fetchall()
    conn.close()
    employees = []
    for row in rows:
        enc = None
        if row[6]:
            enc = np.frombuffer(row[6], dtype=np.float64)
        employees.append({
            "emp_id": row[0], "name": row[1], "department": row[2],
            "designation": row[3], "phone": row[4], "email": row[5],
            "face_encoding": enc
        })
    return employees

def mark_attendance(emp_id):
    from datetime import datetime
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")
    try:
        c.execute('''INSERT OR IGNORE INTO attendance (emp_id, date, check_in, status)
                     VALUES (?, ?, ?, 'Present')''', (emp_id, today, now))
        conn.commit()
        affected = conn.total_changes
        return affected > 0
    finally:
        conn.close()

def get_today_attendance():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute('''SELECT e.emp_id, e.name, e.department, a.check_in, a.status
                 FROM employees e
                 LEFT JOIN attendance a ON e.emp_id = a.emp_id AND a.date = ?''', (today,))
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "emp_id": row[0], "name": row[1], "department": row[2],
            "check_in": row[3] if row[3] else "—",
            "status": row[4] if row[4] else "Absent"
        })
    return result

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute("SELECT COUNT(*) FROM employees")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='Present'", (today,))
    present = c.fetchone()[0]
    absent = total - present
    conn.close()
    return total, present, absent


def delete_employee(emp_id):
    import sqlite3

    DB_PATH = "attendance.db"  

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute("DELETE FROM attendance WHERE emp_id = ?", (emp_id,))

        c.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))

        conn.commit()
        return True

    except Exception as e:
        print("Delete Error:", e)
        return False

    finally:
        conn.close()


def mark_as_absent(emp_id):
    import sqlite3
    from datetime import date
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    today = date.today().isoformat()
    try:
        c.execute("DELETE FROM attendance WHERE emp_id = ? AND date = ?", (emp_id, today))
        conn.commit()
        return True
    except Exception as e:
        print("Error marking absent:", e)
        return False
    finally:
        conn.close()    

def mark_attendance(emp_id):
    from datetime import datetime, date  # Critical: Import both 
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")

    # Check if attendance already exists for today
    c.execute("SELECT id FROM attendance WHERE emp_id = ? AND date = ?", (emp_id, today))
    if c.fetchone():
        conn.close()
        return "ALREADY_DONE"

    # If not found, insert new record
    try:
        c.execute('''INSERT INTO attendance (emp_id, date, check_in, status)
                     VALUES (?, ?, ?, 'Present')''', (emp_id, today, now))
        conn.commit()
        return "SUCCESS"
    except Exception as e:
        print(f"Database Error: {e}")
        return "ERROR"
    finally:
        conn.close()

def get_attendance_by_date(selected_date):
    import sqlite3
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    
    # LEFT JOIN ને બદલે INNER JOIN વાપરો
    # આનાથી ફક્ત એ જ રેકોર્ડ આવશે જે 'attendance' ટેબલમાં તે તારીખે ઉપલબ્ધ છે
    c.execute('''SELECT e.emp_id, e.name, e.department, a.check_in, a.status
                 FROM employees e
                 INNER JOIN attendance a ON e.emp_id = a.emp_id 
                 WHERE a.date = ?''', (selected_date,))
    
    rows = c.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "emp_id": row[0],
            "name": row[1],
            "department": row[2],
            "check_in": row[3], # check_in રેકોર્ડ હશે જ
            "status": row[4]    # status 'Present' હશે જ
        })
    return result