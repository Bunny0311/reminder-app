from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ---------- IN-MEMORY STORAGE ----------
reminders = []  # Each reminder will be a dict with keys: id, title, date, time, day_of_week
next_id = 1

# ---------- AUTO DELETE EXPIRED ----------
def delete_expired_reminders():
    global reminders
    today = datetime.now().strftime("%Y-%m-%d")
    reminders = [r for r in reminders if r['date'] >= today]

# ---------- FETCH ALL REMINDERS ----------
def get_reminders():
    delete_expired_reminders()
    return reminders

@app.route('/')
def index():
    all_reminders = get_reminders()
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week_data = {day: [] for day in week_days}
    for r in all_reminders:
        week_data[r['day_of_week']].append(r)
    return render_template("index.html", week_data=week_data, title="Reminder")

@app.route('/add', methods=['POST'])
def add():
    global next_id
    title = request.form.get('title')
    date = request.form.get('date')
    time = request.form.get('time')

    if title and date and time:
        dt = datetime.strptime(date, "%Y-%m-%d")
        day_of_week = dt.strftime("%A")
        reminders.append({
            'id': next_id,
            'title': title,
            'date': date,
            'time': time,
            'day_of_week': day_of_week
        })
        next_id += 1

    return redirect(url_for('index'))

@app.route('/delete/<int:rem_id>')
def delete(rem_id):
    global reminders
    reminders = [r for r in reminders if r['id'] != rem_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
