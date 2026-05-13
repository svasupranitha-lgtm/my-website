"""
StudyFlow - Student Productivity Dashboard
Flask Backend with SQLite Database
=======================================
This is the main server file. It handles all the routes (URLs)
and connects to the SQLite database.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime, date
import json

# =============================================
# APP SETUP
# =============================================
app = Flask(__name__)

# The database file will be created automatically
DATABASE = 'studyflow.db'


# =============================================
# DATABASE HELPER FUNCTIONS
# =============================================

def get_db():
    """
    Opens a connection to the SQLite database.
    Think of this like opening a filing cabinet.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name like a dictionary
    return conn


def init_db():
    """
    Creates all the database tables if they don't exist yet.
    Run this once when the app starts.
    """
    conn = get_db()
    cursor = conn.cursor()

    # ---- CGPA TABLE ----
    # Stores each semester's GPA info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cgpa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semester TEXT NOT NULL,
            gpa REAL NOT NULL,
            credits INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---- ATTENDANCE TABLE ----
    # Tracks attendance for each subject
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            total_classes INTEGER DEFAULT 0,
            attended INTEGER DEFAULT 0,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---- TASKS TABLE ----
    # Your to-do list items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            is_done INTEGER DEFAULT 0,
            due_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---- PLANNER TABLE ----
    # Daily schedule entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS planner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT,
            category TEXT DEFAULT 'study',
            is_done INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---- REMINDERS TABLE ----
    # Events, deadlines, activities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            event_date TEXT NOT NULL,
            event_time TEXT,
            category TEXT DEFAULT 'general',
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---- STREAK TABLE ----
    # Tracks daily login streaks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streak (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_visit TEXT,
            streak_count INTEGER DEFAULT 0
        )
    ''')

    # Insert default streak row if empty
    cursor.execute('SELECT COUNT(*) FROM streak')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO streak (last_visit, streak_count) VALUES (?, 1)',
                      (str(date.today()),))

    conn.commit()
    conn.close()
    print("✅ Database initialized!")


# =============================================
# MOTIVATION QUOTES (stored in code for simplicity)
# =============================================
QUOTES = [
    {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain"},
    {"quote": "It always seems impossible until it's done.", "author": "Nelson Mandela"},
    {"quote": "Push yourself, because no one else is going to do it for you.", "author": "Unknown"},
    {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson"},
    {"quote": "The expert in anything was once a beginner.", "author": "Helen Hayes"},
    {"quote": "Success is the sum of small efforts repeated day in and day out.", "author": "Robert Collier"},
    {"quote": "You don't have to be great to start, but you have to start to be great.", "author": "Zig Ziglar"},
    {"quote": "Study hard, for the well is deep and our brains are shallow.", "author": "Richard Baxter"},
    {"quote": "Education is the passport to the future.", "author": "Malcolm X"},
    {"quote": "The beautiful thing about learning is that no one can take it away from you.", "author": "B.B. King"},
]

FACTS = [
    "🧠 Your brain uses 20% of your body's total energy!",
    "💤 Sleep helps consolidate memories — studying before bed can help you remember more.",
    "🎵 Listening to Mozart can temporarily boost spatial reasoning skills.",
    "📚 The average person reads 200-250 words per minute.",
    "⏰ The Pomodoro Technique (25 min work + 5 min break) is proven to boost focus.",
    "🌊 Drinking water improves concentration by up to 30%.",
    "✍️ Handwriting notes helps retain information better than typing.",
    "🏃 Exercise for 20 minutes before studying can improve memory and focus.",
    "🌙 REM sleep is crucial for problem-solving and creative thinking.",
    "🎯 Breaking goals into smaller tasks activates the brain's reward system.",
]


# =============================================
# PAGE ROUTES (what users see in the browser)
# =============================================

@app.route('/')
def dashboard():
    """Main dashboard page"""
    conn = get_db()

    # Get streak info
    streak_data = conn.execute('SELECT * FROM streak WHERE id = 1').fetchone()
    streak_count = 0
    if streak_data:
        last_visit = streak_data['last_visit']
        today = str(date.today())
        streak_count = streak_data['streak_count']

        # Update streak: if last visit was yesterday, increment; if today, keep; else reset
        from datetime import timedelta
        yesterday = str(date.today() - timedelta(days=1))

        if last_visit == yesterday:
            streak_count += 1
            conn.execute('UPDATE streak SET last_visit = ?, streak_count = ? WHERE id = 1',
                        (today, streak_count))
            conn.commit()
        elif last_visit != today:
            streak_count = 1
            conn.execute('UPDATE streak SET last_visit = ?, streak_count = 1 WHERE id = 1',
                        (today,))
            conn.commit()

    # Get quick stats for dashboard
    total_tasks = conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    done_tasks = conn.execute('SELECT COUNT(*) FROM tasks WHERE is_done = 1').fetchone()[0]
    pending_tasks = total_tasks - done_tasks

    # Get today's planner items
    today_items = conn.execute(
        'SELECT COUNT(*) FROM planner WHERE date = ?', (str(date.today()),)
    ).fetchone()[0]

    # Get upcoming reminders (next 7 days)
    upcoming = conn.execute(
        "SELECT COUNT(*) FROM reminders WHERE event_date >= ? AND is_active = 1",
        (str(date.today()),)
    ).fetchone()[0]

    # Get CGPA data
    cgpa_records = conn.execute('SELECT * FROM cgpa ORDER BY id').fetchall()
    cgpa_value = 0.0
    if cgpa_records:
        total_weighted = sum(r['gpa'] * r['credits'] for r in cgpa_records)
        total_credits = sum(r['credits'] for r in cgpa_records)
        if total_credits > 0:
            cgpa_value = round(total_weighted / total_credits, 2)

    conn.close()

    # Get random quote and fact
    import random
    quote = random.choice(QUOTES)
    fact = random.choice(FACTS)

    return render_template('dashboard.html',
                           streak=streak_count,
                           total_tasks=total_tasks,
                           done_tasks=done_tasks,
                           pending_tasks=pending_tasks,
                           today_items=today_items,
                           upcoming=upcoming,
                           cgpa=cgpa_value,
                           quote=quote,
                           fact=fact)


@app.route('/cgpa')
def cgpa_page():
    """CGPA Tracker page"""
    conn = get_db()
    records = conn.execute('SELECT * FROM cgpa ORDER BY id').fetchall()

    # Calculate current CGPA
    cgpa_value = 0.0
    if records:
        total_weighted = sum(r['gpa'] * r['credits'] for r in records)
        total_credits = sum(r['credits'] for r in records)
        if total_credits > 0:
            cgpa_value = round(total_weighted / total_credits, 2)

    conn.close()
    return render_template('cgpa.html', records=records, cgpa=cgpa_value)


@app.route('/attendance')
def attendance_page():
    """Attendance Tracker page"""
    conn = get_db()
    subjects = conn.execute('SELECT * FROM attendance ORDER BY subject').fetchall()

    # Calculate percentage for each subject
    subjects_data = []
    for s in subjects:
        pct = 0
        if s['total_classes'] > 0:
            pct = round((s['attended'] / s['total_classes']) * 100, 1)
        subjects_data.append({
            'id': s['id'],
            'subject': s['subject'],
            'total_classes': s['total_classes'],
            'attended': s['attended'],
            'percentage': pct,
            'status': 'safe' if pct >= 75 else ('warning' if pct >= 60 else 'danger')
        })

    conn.close()
    return render_template('attendance.html', subjects=subjects_data)


@app.route('/tasks')
def tasks_page():
    """To-Do List page"""
    conn = get_db()
    all_tasks = conn.execute('SELECT * FROM tasks ORDER BY is_done ASC, created_at DESC').fetchall()
    conn.close()
    return render_template('tasks.html', tasks=all_tasks)


@app.route('/planner')
def planner_page():
    """Daily Planner page"""
    today = str(date.today())
    conn = get_db()
    # Get items for today and upcoming week
    items = conn.execute(
        'SELECT * FROM planner WHERE date >= ? ORDER BY date ASC, time ASC',
        (today,)
    ).fetchall()
    conn.close()
    return render_template('planner.html', items=items, today=today)


@app.route('/reminders')
def reminders_page():
    """Reminders & Events page"""
    today = str(date.today())
    conn = get_db()
    upcoming = conn.execute(
        'SELECT * FROM reminders WHERE event_date >= ? AND is_active = 1 ORDER BY event_date ASC',
        (today,)
    ).fetchall()
    past = conn.execute(
        'SELECT * FROM reminders WHERE event_date < ? ORDER BY event_date DESC LIMIT 10',
        (today,)
    ).fetchall()
    conn.close()
    return render_template('reminders.html', upcoming=upcoming, past=past, today=today)


# =============================================
# API ROUTES (used by JavaScript to save/load data)
# =============================================

# --- CGPA API ---
@app.route('/api/cgpa', methods=['POST'])
def add_cgpa():
    """Add a new semester GPA record"""
    data = request.json
    conn = get_db()
    conn.execute(
        'INSERT INTO cgpa (semester, gpa, credits) VALUES (?, ?, ?)',
        (data['semester'], float(data['gpa']), int(data['credits']))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Semester added!'})


@app.route('/api/cgpa/<int:record_id>', methods=['DELETE'])
def delete_cgpa(record_id):
    """Delete a semester record"""
    conn = get_db()
    conn.execute('DELETE FROM cgpa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# --- ATTENDANCE API ---
@app.route('/api/attendance', methods=['POST'])
def add_attendance():
    """Add a new subject"""
    data = request.json
    conn = get_db()

    # Check if subject already exists
    existing = conn.execute(
        'SELECT id FROM attendance WHERE subject = ?', (data['subject'],)
    ).fetchone()

    if existing:
        conn.close()
        return jsonify({'success': False, 'message': 'Subject already exists!'})

    conn.execute(
        'INSERT INTO attendance (subject, total_classes, attended) VALUES (?, ?, ?)',
        (data['subject'], int(data.get('total_classes', 0)), int(data.get('attended', 0)))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Subject added!'})


@app.route('/api/attendance/<int:subject_id>', methods=['PUT'])
def update_attendance(subject_id):
    """Update attendance numbers (mark present/absent)"""
    data = request.json
    conn = get_db()

    if data.get('action') == 'present':
        conn.execute(
            'UPDATE attendance SET total_classes = total_classes + 1, attended = attended + 1, updated_at = ? WHERE id = ?',
            (datetime.now().isoformat(), subject_id)
        )
    elif data.get('action') == 'absent':
        conn.execute(
            'UPDATE attendance SET total_classes = total_classes + 1, updated_at = ? WHERE id = ?',
            (datetime.now().isoformat(), subject_id)
        )
    else:
        # Direct update
        conn.execute(
            'UPDATE attendance SET total_classes = ?, attended = ?, updated_at = ? WHERE id = ?',
            (int(data['total_classes']), int(data['attended']), datetime.now().isoformat(), subject_id)
        )

    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/attendance/<int:subject_id>', methods=['DELETE'])
def delete_attendance(subject_id):
    """Delete a subject"""
    conn = get_db()
    conn.execute('DELETE FROM attendance WHERE id = ?', (subject_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# --- TASKS API ---
@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Add a new to-do task"""
    data = request.json
    conn = get_db()
    conn.execute(
        'INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)',
        (data['title'], data.get('description', ''), data.get('priority', 'medium'), data.get('due_date', ''))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Task added!'})


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Toggle task done/undone"""
    data = request.json
    conn = get_db()
    conn.execute('UPDATE tasks SET is_done = ? WHERE id = ?', (int(data['is_done']), task_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# --- PLANNER API ---
@app.route('/api/planner', methods=['POST'])
def add_planner():
    """Add a new planner entry"""
    data = request.json
    conn = get_db()
    conn.execute(
        'INSERT INTO planner (title, date, time, category) VALUES (?, ?, ?, ?)',
        (data['title'], data['date'], data.get('time', ''), data.get('category', 'study'))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Added to planner!'})


@app.route('/api/planner/<int:item_id>', methods=['PUT'])
def update_planner(item_id):
    """Mark planner item as done"""
    data = request.json
    conn = get_db()
    conn.execute('UPDATE planner SET is_done = ? WHERE id = ?', (int(data['is_done']), item_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/planner/<int:item_id>', methods=['DELETE'])
def delete_planner(item_id):
    """Delete planner item"""
    conn = get_db()
    conn.execute('DELETE FROM planner WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# --- REMINDERS API ---
@app.route('/api/reminders', methods=['POST'])
def add_reminder():
    """Add a new reminder/event"""
    data = request.json
    conn = get_db()
    conn.execute(
        'INSERT INTO reminders (title, description, event_date, event_time, category) VALUES (?, ?, ?, ?, ?)',
        (data['title'], data.get('description', ''), data['event_date'],
         data.get('event_time', ''), data.get('category', 'general'))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Reminder set!'})


@app.route('/api/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    """Delete a reminder"""
    conn = get_db()
    conn.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# --- MOTIVATION API ---
@app.route('/api/quote')
def get_quote():
    """Get a random motivational quote"""
    import random
    return jsonify(random.choice(QUOTES))


@app.route('/api/fact')
def get_fact():
    """Get a random study fact"""
    import random
    return jsonify({'fact': random.choice(FACTS)})


# =============================================
# RUN THE APP
# =============================================
if __name__ == '__main__':
    init_db()  # Set up the database tables
    print("🚀 StudyFlow is running!")
    print("📖 Open your browser and go to: http://localhost:5000")
   import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
