import sqlite3

DB_PATH = "todo.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task_db(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def update_task_db(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if new_task is not None:
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (int(completed), task_id))
    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
