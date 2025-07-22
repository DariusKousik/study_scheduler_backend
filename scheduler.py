from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import date, timedelta
from datetime import datetime, date, timedelta
from database import SessionLocal
import crud
from utils.email_utils import send_email
import pytz
from apscheduler.triggers.cron import CronTrigger
# from apscheduler.triggers.interval import IntervalTrigger


def check_and_send_reminders():
    db = SessionLocal()
    try:
        profile = crud.get_profile(db)
        if not profile or not profile.email:
            return

        tasks = crud.get_tasks(db)
        pending_tasks = [
                t for t in tasks 
                if not t.completed and 
                datetime.strptime(t.date, "%Y-%m-%d").date() < date.today() - timedelta(days=3)
        ]
        today_tasks = [t for t in tasks if t.date == date.today()]

        if not pending_tasks and not today_tasks:
            return  # Nothing to send

        body = ""
        if pending_tasks:
            body += "🔴 Pending Tasks for long time:\n" + "\n".join([t.title for t in pending_tasks]) + "\n\n"
        if today_tasks:
            body += "🟢 Today's Tasks:\n" + "\n".join([t.title for t in today_tasks])

        send_email(profile.email, "📧 Task Reminder", body)
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Kolkata"))  # ✅ Set your timezone
    scheduler.add_job(check_and_send_reminders, CronTrigger(hour=9, minute=0))
    # scheduler.add_job(check_and_send_reminders, IntervalTrigger(seconds=30))
    scheduler.start()
