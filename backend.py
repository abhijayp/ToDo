import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
task TEXT,
due TEXT,
status TEXT
)
""")
conn.commit()

def Create_Task(task, task_due_date, task_status):
    cursor.execute(
        "INSERT INTO tasks (task, due, status) VALUES (?, ?, ?)",
        (task, task_due_date, task_status)
    )
    conn.commit()

def Status_Update(task_choice_status, status_choice):
    cursor.execute(
        "UPDATE tasks SET status = ? WHERE task = ?",
        (status_choice, task_choice_status)
    )
    conn.commit()

def Task_Edit(task_edit_choice, edit_choice):
    cursor.execute(
        "UPDATE tasks SET task = ? WHERE task = ?",
        (task_edit_choice, edit_choice)
    )
    conn.commit()

def Task_Due_Date(task_id, due_date_edit):
    cursor.execute(
        "UPDATE tasks SET due = ? WHERE id = ?",
        (due_date_edit, task_id)
    )
    conn.commit()

def Delete_Task(task_id):
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?", 
        (task_id,)
    )
    conn.commit()

def Tasks_Show():
    cursor.execute("SELECT id, task, due, status FROM tasks")
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "task": row[1],
            "due": row[2],
            "status": row[3]
        })
    return tasks

def close_conn():
    conn.close()