import json
import sqlite3
from pathlib import Path
from datetime import date

DB_PATH = Path(__file__).with_name("careerpilot.db")

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                education TEXT NOT NULL,
                target_role TEXT NOT NULL,
                known_skills TEXT NOT NULL,
                level TEXT NOT NULL,
                hours_per_day REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                day_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                estimated_minutes INTEGER NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                skill TEXT NOT NULL,
                resources TEXT NOT NULL DEFAULT '[]',
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)
        # Backward-compatible migration for existing local careerpilot.db files.
        task_columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)").fetchall()}
        if "resources" not in task_columns:
            conn.execute("ALTER TABLE tasks ADD COLUMN resources TEXT NOT NULL DEFAULT '[]'")

def add_student(name, education, target_role, known_skills, level, hours_per_day):
    with connect() as conn:
        cursor = conn.execute(
            """INSERT INTO students
            (name, education, target_role, known_skills, level, hours_per_day, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name.strip() or "Student", education, target_role, json.dumps(known_skills), level,
             float(hours_per_day), date.today().isoformat())
        )
        return cursor.lastrowid

def get_student(student_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not row:
        return None
    result = dict(row)
    result["known_skills"] = json.loads(result["known_skills"])
    return result

def save_plan(student_id, roadmap, tasks):
    with connect() as conn:
        conn.execute("DELETE FROM tasks WHERE student_id = ?", (student_id,))
        for task in tasks:
            conn.execute("""
                INSERT INTO tasks
                (student_id, day_number, title, description, estimated_minutes, due_date, status, skill, resources)
                VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?, ?)
            """, (student_id, task["day_number"], task["title"], task["description"],
                  task["estimated_minutes"], task["due_date"], task["skill"],
                  json.dumps(task.get("resources", []), ensure_ascii=False)))

def get_tasks(student_id):
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE student_id = ? ORDER BY day_number, id", (student_id,)
        ).fetchall()
    tasks = [dict(row) for row in rows]
    for task in tasks:
        try:
            task["resources"] = json.loads(task.get("resources") or "[]")
        except (TypeError, json.JSONDecodeError):
            task["resources"] = []
    return tasks

def update_task(task_id, status):
    with connect() as conn:
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))

def get_summary(student_id):
    tasks = get_tasks(student_id)
    total = len(tasks)
    completed = sum(1 for task in tasks if task["status"] == "Completed")
    remaining = total - completed
    return {
        "total": total,
        "completed": completed,
        "remaining": remaining,
        "percent": round(completed * 100 / total) if total else 0
    }

def get_gaps(student_id):
    return []
