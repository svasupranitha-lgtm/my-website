# ⚡ StudyFlow — Complete Beginner Guide
### Your All-in-One Student Productivity Dashboard

---

## 1. 🎯 FINAL PRODUCT CONCEPT

### Product Name: **StudyFlow**
*Tagline: "Study smarter. Live better."*

### Main Idea
StudyFlow is a web-based student productivity dashboard that combines everything a student needs into one cohesive app: grade tracking, attendance management, to-do lists, daily planning, event reminders, and daily motivation — all in a beautiful, Gen Z-inspired interface.

### Problem Statement
Students juggle grades, attendance, assignments, deadlines, and personal goals across multiple apps, notebooks, and mental sticky notes. This leads to missed deadlines, forgotten assignments, poor attendance, and anxiety. StudyFlow solves this by being **the one app that has everything**.

### Why It Stands Out at Hackathons
- **Visually impressive** — glassmorphism dark UI, animated elements, gradient accents
- **Highly practical** — solves a real, universal student problem
- **Full-stack** — demonstrates frontend + backend + database skills
- **Cohesive UX** — feels like one product, not stitched-together mini-tools
- **Beginner-accessible code** — easy to explain to judges

---

## 2. 🎨 UI/UX DESIGN SYSTEM

### Color Palette
| Role | Color | Hex |
|------|-------|-----|
| Brand Primary | Electric Purple | `#7C3AED` |
| Brand Secondary | Amber Gold | `#F59E0B` |
| Success / Safe | Emerald | `#10B981` |
| Warning | Warm Amber | `#F59E0B` |
| Danger | Coral Red | `#EF4444` |
| Accent Pink | Hot Pink | `#EC4899` |
| Accent Blue | Sky Blue | `#3B82F6` |
| Background (dark) | Near Black | `#0A0A0F` |
| Surface (dark) | Dark Navy | `#13131A` |

### Typography
- **Display / Headings**: `Syne` — Bold, geometric, editorial feel
- **Body / UI Text**: `DM Sans` — Clean, modern, highly readable

### Design Elements
- **Glassmorphism**: Translucent cards with `backdrop-filter: blur()`
- **Gradient text**: CSS `background-clip: text` on key headings
- **Glowing borders**: Subtle purple glow on hover states
- **Progress circles**: SVG-based circular progress for CGPA
- **Streak animations**: Fire emoji animation using CSS keyframes
- **Staggered entry**: Cards fade in with offset animation delays
- **Dark mode default**: Toggle to light with localStorage persistence

---

## 3. 🗂️ COMPLETE FOLDER STRUCTURE

```
studyflow/
├── app.py                    # Flask server (main backend file)
├── requirements.txt          # Python packages needed
├── studyflow.db              # SQLite database (auto-created on first run)
│
├── templates/                # HTML files (Flask renders these)
│   ├── base.html             # Shared layout: sidebar, navbar, dark mode toggle
│   ├── dashboard.html        # Homepage / main dashboard
│   ├── cgpa.html             # CGPA tracker page
│   ├── attendance.html       # Attendance tracker page
│   ├── tasks.html            # To-do list page
│   ├── planner.html          # Daily planner page
│   └── reminders.html        # Reminders & events page
│
└── static/                   # Files served directly (CSS, JS, images)
    └── css/
        └── style.css         # All styles for the whole project
```

**Why this structure?**
- Flask looks for templates in the `templates/` folder automatically
- Flask serves files from `static/` with `/static/` URLs automatically
- All backend logic is in one file (`app.py`) — simple for beginners
- One CSS file means you control the whole look in one place

---

## 4. 🛠️ FULL FEATURE BREAKDOWN

### Feature 1: CGPA Tracker
- **Purpose**: Calculate weighted CGPA across all semesters
- **Frontend**: Circular SVG progress ring, semester cards with bar charts, add form
- **Backend**: Stores semester name, GPA, credits. Calculates weighted average
- **Formula**: `CGPA = Σ(GPA × Credits) / Σ(Credits)`

### Feature 2: Attendance Tracker
- **Purpose**: Track per-subject attendance with 75% threshold alerts
- **Frontend**: Per-subject cards with color-coded progress bars (green/yellow/red)
- **Backend**: Stores total_classes and attended per subject. Quick "Present"/"Absent" buttons
- **Smart alert**: Calculates exactly how many classes are needed to reach 75%

### Feature 3: To-Do List
- **Purpose**: Manage tasks with priorities and due dates
- **Frontend**: Inline add form, filterable list, checkbox completion, priority color coding
- **Backend**: CRUD operations on tasks table

### Feature 4: Daily Planner
- **Purpose**: Schedule activities for specific dates and times
- **Frontend**: Today's view + upcoming schedule grouped by date, category pills
- **Backend**: Planner items with date, time, category, and done status

### Feature 5: Reminders
- **Purpose**: Set event/exam/assignment reminders with countdown
- **Frontend**: Date blocks, category badges, automatic "X days left" countdown via JavaScript
- **Backend**: Stores event date/time/category, separates upcoming from past

### Feature 6: Motivation System
- **Purpose**: Daily dose of motivation and study tips
- **Frontend**: Quote card + study fact card, "New Quote" button fetches from API
- **Backend**: Stores quotes/facts in Python arrays (no DB needed — simple!)

### Feature 7: Streak Counter
- **Purpose**: Gamify daily usage and reward consistency
- **Frontend**: Fire emoji animation + streak number on dashboard
- **Backend**: Checks last_visit date, increments streak if visited yesterday, resets if missed a day

---

## 5. ⚙️ TECH STACK EXPLANATION

### Why Flask?
- Python-based → students usually know Python first
- Minimal setup → `pip install flask` and you're running
- Beginner-readable routing → `@app.route('/page')` is very intuitive
- Renders HTML templates → perfect for a multi-page app

### Why SQLite?
- No installation required → it's a single `.db` file
- Built into Python via `sqlite3` module → no extra packages
- SQL is readable even for beginners
- Perfect for hackathon/prototype scale

### Frontend/Backend Communication
- **Page loads**: Flask renders HTML with Jinja2 templates — data passed directly
- **Dynamic actions** (adding tasks, toggling done): JavaScript `fetch()` calls Flask API routes that return JSON
- This is a **hybrid approach** — simple pages + dynamic CRUD via API

### Why This Stack is Beginner-Friendly
- Only 2 languages: Python (backend) + HTML/CSS/JS (frontend)
- No package managers, build tools, or compilers needed
- Every line of code can be explained in plain English
- Runs with a single command: `python app.py`

---

## 6. 🚀 COMPLETE BEGINNER SETUP GUIDE

### Step 1: Install Python

1. Open your browser and go to: **https://www.python.org/downloads/**
2. Click the big yellow button: **"Download Python 3.x.x"**
3. Run the downloaded installer
4. **IMPORTANT**: On the first screen, check the box that says **"Add Python to PATH"**
5. Click **"Install Now"**
6. Wait for it to finish, then click **Close**

**Verify it worked**: Open a terminal (see Step 3) and type:
```
python --version
```
You should see something like `Python 3.11.x`

---

### Step 2: Install VS Code

1. Go to: **https://code.visualstudio.com/**
2. Click **"Download for Windows/Mac/Linux"**
3. Run the installer with all default settings
4. Open VS Code after installation

**Recommended Extensions** (install from the Extensions tab in VS Code):
- **Python** (by Microsoft) — Python language support
- **Prettier** — auto-formats your code
- **Auto Rename Tag** — helps with HTML tags
- **SQLite Viewer** — lets you peek inside your .db file

To install extensions: Click the 4-squares icon on the left sidebar → search the extension name → click Install

---

### Step 3: Open a Terminal

**In VS Code**: Go to menu → **Terminal → New Terminal** (or press Ctrl+backtick)

**Alternatively**:
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac**: Press `Cmd + Space`, type `terminal`, press Enter
- **Linux**: Right-click desktop → Open Terminal

---

### Step 4: Create Your Project Folder

In the terminal, type these commands one by one (press Enter after each):

```bash
# Go to your home/desktop directory
cd Desktop

# Create a new folder called studyflow
mkdir studyflow

# Go inside the folder
cd studyflow
```

---

### Step 5: Create the Folder Structure

```bash
# Create subfolders
mkdir templates
mkdir static
mkdir static/css
mkdir static/js
```

---

### Step 6: Install Flask

In your terminal (make sure you're in the studyflow folder):

```bash
pip install flask
```

Wait for it to download. You should see `Successfully installed flask-...`

**If pip doesn't work**, try:
```bash
pip3 install flask
```

---

### Step 7: Copy All the Code Files

Copy each file from this guide into the correct location:

| File | Location |
|------|----------|
| `app.py` | `studyflow/app.py` |
| `style.css` | `studyflow/static/css/style.css` |
| `base.html` | `studyflow/templates/base.html` |
| `dashboard.html` | `studyflow/templates/dashboard.html` |
| `cgpa.html` | `studyflow/templates/cgpa.html` |
| `attendance.html` | `studyflow/templates/attendance.html` |
| `tasks.html` | `studyflow/templates/tasks.html` |
| `planner.html` | `studyflow/templates/planner.html` |
| `reminders.html` | `studyflow/templates/reminders.html` |

---

### Step 8: Run the App

In your terminal, from the `studyflow/` folder:

```bash
python app.py
```

You should see:
```
✅ Database initialized!
🚀 StudyFlow is running!
📖 Open your browser and go to: http://localhost:5000
 * Running on http://127.0.0.1:5000
```

---

### Step 9: Open the Website

Open your browser and type in the address bar:
```
http://localhost:5000
```

Press Enter. StudyFlow should appear! 🎉

---

### Step 10: Stop the Server

Press `Ctrl + C` in the terminal to stop the server.

---

## 7. 🔌 API ENDPOINTS REFERENCE

| Method | URL | What it does |
|--------|-----|--------------|
| GET | `/` | Dashboard page |
| GET | `/cgpa` | CGPA tracker page |
| GET | `/attendance` | Attendance page |
| GET | `/tasks` | To-do list page |
| GET | `/planner` | Planner page |
| GET | `/reminders` | Reminders page |
| POST | `/api/cgpa` | Add semester |
| DELETE | `/api/cgpa/<id>` | Delete semester |
| POST | `/api/attendance` | Add subject |
| PUT | `/api/attendance/<id>` | Update attendance |
| DELETE | `/api/attendance/<id>` | Delete subject |
| POST | `/api/tasks` | Add task |
| PUT | `/api/tasks/<id>` | Toggle task done |
| DELETE | `/api/tasks/<id>` | Delete task |
| POST | `/api/planner` | Add planner item |
| PUT | `/api/planner/<id>` | Toggle done |
| DELETE | `/api/planner/<id>` | Delete item |
| POST | `/api/reminders` | Add reminder |
| DELETE | `/api/reminders/<id>` | Delete reminder |
| GET | `/api/quote` | Get random quote |
| GET | `/api/fact` | Get random fact |

---

## 8. 🐛 COMMON ERRORS & FIXES

### Error: `ModuleNotFoundError: No module named 'flask'`
**Fix**: Run `pip install flask` in your terminal

### Error: `Address already in use`
**Fix**: Another server is running on port 5000. Either stop it (Ctrl+C) or change the port in `app.py`: `app.run(port=5001)`

### Error: `TemplateNotFound`
**Fix**: Make sure your HTML files are inside a folder called exactly `templates/` (lowercase)

### Error: `sqlite3.OperationalError: no such table`
**Fix**: Delete `studyflow.db` and restart `python app.py` — `init_db()` will recreate it

### CSS not loading
**Fix**: Make sure `style.css` is in `static/css/style.css` and the path in `base.html` matches exactly

### JavaScript fetch not working
**Fix**: Make sure Flask is running (`python app.py`). Check browser DevTools (F12) → Console for error messages

### `python` command not found
**Fix**: Try `python3 app.py` instead. Or reinstall Python and check "Add to PATH"

---

## 9. 🌐 DEPLOYMENT GUIDE (Free Hosting)

### Option 1: Render.com (Recommended — Free)

1. Create a free account at **https://render.com**
2. Create a file called `Procfile` in your project root:
   ```
   web: python app.py
   ```
3. Update `app.py` last line to:
   ```python
   app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
   ```
4. Push your code to GitHub (create account at github.com)
5. In Render: **New → Web Service → Connect GitHub repo**
6. Set build command: `pip install -r requirements.txt`
7. Set start command: `python app.py`
8. Click Deploy!

### Option 2: Railway.app (Very Easy)

1. Go to **https://railway.app** → Sign up with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Select your StudyFlow repository
4. Railway auto-detects Python/Flask and deploys it!

### Option 3: PythonAnywhere (Beginner-Friendly)

1. Sign up free at **https://www.pythonanywhere.com**
2. Go to **Files** → upload all your project files
3. Go to **Web** → Add a new web app → Flask → Python 3.x
4. Set source code path to `/home/yourusername/studyflow`
5. Click **Reload** and your site is live!

---

## 10. 🏆 HACKATHON PRESENTATION STRATEGY

### What to Demo First (in this order):
1. **Dashboard** — instant visual wow factor, shows streaks and stats
2. **CGPA tracker** — the animated circle progress always impresses
3. **Attendance** — the "classes needed" calculation shows smart logic
4. **Tasks** — quick demo of adding + completing a task
5. **Quote/Fact** — the refresh button is satisfying and lightens mood

### How to Impress Judges:

**On Creativity**: "We designed a unified ecosystem instead of separate tools. Everything is connected — your task completion rate shows on the dashboard, your streak tracks daily engagement, your CGPA is always visible."

**On Technical Thinking**: "We used a hybrid rendering approach — Flask renders full pages with data using Jinja2 templates, while interactive actions like marking tasks done use JavaScript fetch() calls to our REST API, keeping the app fast and responsive."

**On Feasibility**: "The entire project runs with one command — `python app.py`. It uses only Python standard libraries plus Flask. No cloud services, no complex setup. Any student can download and run this in 5 minutes."

**On UI Choices**: "We used glassmorphism and gradient accents because students don't want to look at another boring white form. If your productivity app feels energizing to open, you're more likely to actually use it."

### Killer Demo Line:
*"Imagine every student had this instead of 6 different apps and a physical planner. That's exactly what StudyFlow replaces."*

---

## 11. 🔧 DATABASE SCHEMA REFERENCE

```sql
-- Stores GPA per semester for CGPA calculation
CREATE TABLE cgpa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester TEXT NOT NULL,
    gpa REAL NOT NULL,
    credits INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Per-subject attendance tracking
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    total_classes INTEGER DEFAULT 0,
    attended INTEGER DEFAULT 0,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- To-do tasks with priority and due dates
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'medium',
    is_done INTEGER DEFAULT 0,
    due_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Daily planner entries
CREATE TABLE planner (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    category TEXT DEFAULT 'study',
    is_done INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Event reminders with categories
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    event_date TEXT NOT NULL,
    event_time TEXT,
    category TEXT DEFAULT 'general',
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Streak tracking (one row, updated daily)
CREATE TABLE streak (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_visit TEXT,
    streak_count INTEGER DEFAULT 0
);
```

---

## 12. 🏗️ BEST BUILD ORDER FOR BEGINNERS

Follow this exact order:

1. **Set up Python + VS Code** (Step 1-2 above)
2. **Create folder structure** (Step 4-5)
3. **Copy `app.py`** — the backend brain
4. **Copy `style.css`** — all the visual styling
5. **Copy `base.html`** — the shared layout shell
6. **Copy `dashboard.html`** — run the app, see your first page!
7. **Test**: `python app.py` → open `http://localhost:5000`
8. **Copy `cgpa.html`** → test CGPA page
9. **Copy `attendance.html`** → test attendance
10. **Copy `tasks.html`** → test to-do list
11. **Copy `planner.html`** → test planner
12. **Copy `reminders.html`** → test reminders
13. **Test all features** with real data
14. **Polish UI** — adjust colors, spacing
15. **Deploy** using Render or Railway

---

*Built with ❤️ for students, by students.*
*Good luck at your hackathon! You've got this. 🚀*
