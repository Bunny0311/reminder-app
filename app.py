from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "reminders.db"

# ---------- INITIALIZE DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            day_of_week TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- AUTO DELETE EXPIRED ----------
def delete_expired_reminders():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE date < ?", (today,))
    conn.commit()
    conn.close()

# ---------- FETCH ALL REMINDERS ----------
def get_reminders():
    delete_expired_reminders()  # Automatically clean up old ones
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    reminders = get_reminders()
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week_data = {day: [] for day in week_days}
    for r in reminders:
        week_data[r[4]].append({'id': r[0], 'title': r[1], 'date': r[2], 'time': r[3]})
    return render_template("index.html", week_data=week_data, title="Reminder")

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    date = request.form.get('date')
    time = request.form.get('time')
    if title and date and time:
        dt = datetime.strptime(date, "%Y-%m-%d")
        day_of_week = dt.strftime("%A")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (title, date, time, day_of_week) VALUES (?, ?, ?, ?)",
            (title, date, time, day_of_week)
        )
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:rem_id>')
def delete(rem_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id=?", (rem_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


