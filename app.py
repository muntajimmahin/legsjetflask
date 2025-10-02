from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_apscheduler import APScheduler
import threading
import json
from datetime import datetime, date
import re

# Import your scraper modules
import globeair
import aircharter
import flyvictor
import jettly
import privatelegs
import inboxscraper




from flask import Flask, render_template, Response, request, redirect, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
import queue
import time
import threading
import builtins






app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SCHEDULER_API_ENABLED'] = True

db = SQLAlchemy(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------- Models --------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # SQLAlchemy 2.0 syntax

# -------------------- Globals (Flights Scrapers) --------------------
scraper_enabled = True
scraper_stop_event = threading.Event()
scraper_thread = None
SCHEDULE_ID = "daily_scraper"
STATS_FILE = "stats.json"

# -------------------- Globals (Inbox Scraper) --------------------
inbox_scraper_enabled = True
inbox_scraper_stop_event = threading.Event()
inbox_scraper_thread = None
INBOX_SCHEDULE_ID = "inbox_scraper"
INBOX_STATS_FILE = "inbox_stats.json"

# -------------------- Flights Scraper Logic --------------------
def run_scraper():
    global scraper_thread
    if scraper_thread and scraper_thread.is_alive():
        return
    scraper_stop_event.clear()

    def task():
        for scraper in [privatelegs, aircharter, flyvictor,  globeair, jettly]:
            scraper.run(stop_event=scraper_stop_event)
            if not scraper_stop_event.is_set():
                update_stats()

    scraper_thread = threading.Thread(target=task)
    scraper_thread.start()

def update_stats():
    today = str(date.today())
    try:
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stats = {"last_run": "", "today_count": 0, "last_date": today}

    if stats["last_date"] != today:
        stats["today_count"] = 0
        stats["last_date"] = today

    stats["today_count"] += 1
    stats["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def schedule_scraper(hour=7, minute=0):
    try:
        scheduler.remove_job(SCHEDULE_ID)
    except Exception:
        pass

    scheduler.add_job(
        id=SCHEDULE_ID,
        func=run_scraper,
        trigger='cron',
        hour=hour,
        minute=minute
    )

schedule_scraper()

# -------------------- Inbox Scraper Logic --------------------
def run_inbox_scraper():
    global inbox_scraper_thread
    if inbox_scraper_thread and inbox_scraper_thread.is_alive():
        return
    inbox_scraper_stop_event.clear()

    def task():
        inboxscraper.run(stop_event=inbox_scraper_stop_event)
        if not inbox_scraper_stop_event.is_set():
            update_inbox_stats()

    inbox_scraper_thread = threading.Thread(target=task)
    inbox_scraper_thread.start()

def update_inbox_stats():
    today = str(date.today())
    try:
        with open(INBOX_STATS_FILE, "r") as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stats = {"last_run": "", "today_count": 0, "last_date": today}

    if stats["last_date"] != today:
        stats["today_count"] = 0
        stats["last_date"] = today

    stats["today_count"] += 1
    stats["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(INBOX_STATS_FILE, "w") as f:
        json.dump(stats, f)

def schedule_inbox_scraper(hour=9, minute=0):
    try:
        scheduler.remove_job(INBOX_SCHEDULE_ID)
    except Exception:
        pass

    scheduler.add_job(
        id=INBOX_SCHEDULE_ID,
        func=run_inbox_scraper,
        trigger='cron',
        hour=hour,
        minute=minute
    )

schedule_inbox_scraper()

# -------------------- Routes --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# -------- Flights Dashboard --------
@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    global scraper_enabled
    stats = {"last_run": "N/A", "today_count": 0}
    try:
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
    except Exception:
        pass

    job = scheduler.get_job(SCHEDULE_ID)
    scraper_time = "Not scheduled"

    if job:
        trigger_str = str(job.trigger)
        match = re.search(r"hour='([^']*)'.*minute='([^']*)'", trigger_str)
        if match:
            hour_str, minute_str = match.groups()
            time_obj = datetime.strptime(f"{hour_str}:{minute_str}", "%H:%M")
            scraper_time = time_obj.strftime("%I:%M %p")
        else:
            scraper_time = "Invalid"

    scraper_status = "Live" if not scraper_stop_event.is_set() else "Killed"

    if request.method == 'POST':
        if 'set_time' in request.form:
            try:
                hour, minute = map(int, request.form['run_time'].split(':'))
                schedule_scraper(hour, minute)
            except ValueError:
                flash("Invalid time format", "danger")
        elif 'toggle_scraper' in request.form:
            scraper_enabled = not scraper_enabled
            if scraper_enabled:
                schedule_scraper()
            else:
                try:
                    scheduler.remove_job(SCHEDULE_ID)
                except Exception:
                    pass
        elif 'kill_scraper' in request.form:
            scraper_stop_event.set()
        return redirect(url_for('dashboard'))

    return render_template(
        'dashboard.html',
        now=datetime.now(),
        stats=stats,
        enabled=scraper_enabled,
        scraper_time=scraper_time,
        scraper_status=scraper_status
    )






from flask import Flask, jsonify
from collections import deque
import builtins
from datetime import datetime


# Rolling buffer: log as tuple (timestamp, level, message)
log_buffer = deque(maxlen=10000)

# Override print
original_print = print
def print_and_log(*args, **kwargs):
    message = " ".join(str(a) for a in args)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = "INFO"
    log_buffer.append((timestamp, level, message))
    original_print(*args, **{**kwargs, "flush": True})

builtins.print = print_and_log

@app.route("/get-logs")
def get_logs():
    return jsonify(list(log_buffer))










@app.route('/run-now')
@login_required
def run_now():
    run_scraper()
    return redirect(url_for('dashboard'))

# -------- Inbox Dashboard --------
@app.route('/inbox-dashboard', methods=['GET', 'POST'])
@login_required
def inbox_dashboard():
    global inbox_scraper_enabled
    stats = {"last_run": "N/A", "today_count": 0}
    try:
        with open(INBOX_STATS_FILE, "r") as f:
            stats = json.load(f)
    except Exception:
        pass

    job = scheduler.get_job(INBOX_SCHEDULE_ID)
    scraper_time = "Not scheduled"

    if job:
        trigger_str = str(job.trigger)
        match = re.search(r"hour='([^']*)'.*minute='([^']*)'", trigger_str)
        if match:
            hour_str, minute_str = match.groups()
            time_obj = datetime.strptime(f"{hour_str}:{minute_str}", "%H:%M")
            scraper_time = time_obj.strftime("%I:%M %p")
        else:
            scraper_time = "Invalid"

    scraper_status = "Live" if not inbox_scraper_stop_event.is_set() else "Killed"

    if request.method == 'POST':
        if 'set_time' in request.form:
            try:
                hour, minute = map(int, request.form['run_time'].split(':'))
                schedule_inbox_scraper(hour, minute)
            except ValueError:
                flash("Invalid time format", "danger")
        elif 'toggle_scraper' in request.form:
            inbox_scraper_enabled = not inbox_scraper_enabled
            if inbox_scraper_enabled:
                schedule_inbox_scraper()
            else:
                try:
                    scheduler.remove_job(INBOX_SCHEDULE_ID)
                except Exception:
                    pass
        elif 'kill_scraper' in request.form:
            inbox_scraper_stop_event.set()
        return redirect(url_for('inbox_dashboard'))

    return render_template(
        'inbox_dashboard.html',
        now=datetime.now(),
        stats=stats,
        enabled=inbox_scraper_enabled,
        scraper_time=scraper_time,
        scraper_status=scraper_status
    )

@app.route('/inbox-run-now')
@login_required
def inbox_run_now():
    run_inbox_scraper()
    return redirect(url_for('inbox_dashboard'))

# -------- Users Management --------
@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.is_admin:
        return "Access denied", 403

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        hashed = generate_password_hash(password)
        db.session.add(User(username=username, password=hashed, is_admin=is_admin))
        db.session.commit()
        flash('User added.', 'success')
        return redirect(url_for('users'))

    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return "Access denied", 403

    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')

    return redirect(url_for('users'))




# -------------------- Main --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
