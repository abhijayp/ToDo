from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


DB = "tasks.db"

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# tabl create
def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        due TEXT,
        status TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# task create
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not data or 'task' not in data:
        return jsonify({"error": "Task is required"}), 400

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (task, due, status) VALUES (?, ?, ?)",
        (data["task"], data.get("due", ""), data.get("status", "To do"))
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "created"})

# task updt
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    if not data:
        return jsonify({"error": "Data is required"}), 400

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET task=?, due=?, status=? WHERE id=?",
        (data.get("task"), data.get("due"), data.get("status"), id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "updated"})

# task del
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)