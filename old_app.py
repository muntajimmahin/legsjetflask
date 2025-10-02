from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
import threading
import json
from datetime import datetime, date
import globeair  # Your scraper module
import aircharter
import flyvictor
import jettly
import privatelegs
import inboxscraper
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

# -------------------- Globals --------------------
scraper_enabled = True
scraper_stop_event = threading.Event()
scraper_thread = None
SCHEDULE_ID = "daily_scraper"
STATS_FILE = "stats.json"

# -------------------- Scraper Logic --------------------
def run_scraper():
    global scraper_thread
    if scraper_thread and scraper_thread.is_alive():
        return
    scraper_stop_event.clear()

    def task():
        globeair.run(stop_event=scraper_stop_event)
        if not scraper_stop_event.is_set():
            update_stats()

        aircharter.run(stop_event=scraper_stop_event)
        if not scraper_stop_event.is_set():
            update_stats()

        flyvictor.run(stop_event=scraper_stop_event)
        if not scraper_stop_event.is_set():
            update_stats()

        jettly.run(stop_event=scraper_stop_event)
        if not scraper_stop_event.is_set():
            update_stats()

        privatelegs.run(stop_event=scraper_stop_event)
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

    # Get current scheduled time
    from apscheduler.triggers.cron import CronTrigger

    import re
    from datetime import datetime

    job = scheduler.get_job(SCHEDULE_ID)
    scraper_time = "Not scheduled"

    if job:
        trigger_str = str(job.trigger)
        match = re.search(r"hour='([^']*)'.*minute='([^']*)'", trigger_str)
        if match:
            hour_str, minute_str = match.groups()
            hour_int = int(hour_str)
            minute_int = int(minute_str)
            time_obj = datetime.strptime(f"{hour_int}:{minute_int}", "%H:%M")
            scraper_time = time_obj.strftime("%I:%M %p")  # 12-ঘণ্টা AM/PM ফরম্যাট
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

@app.route('/run-now')
@login_required
def run_now():
    run_scraper()
    return redirect(url_for('dashboard'))

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
