import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PASSWORD = os.getenv("FROM_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email, subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_task_reminder_email(to_email, name, pending_tasks, todays_tasks):
    subject = "📋 Study Scheduler Task Reminder"
    
    message = f"Hi {name},\n\n"

    if pending_tasks:
        message += "🔴 Pending Tasks:\n"
        for task in pending_tasks:
            message += f"- {task.title} (Scheduled on: {task.date})\n"
        message += "\n"

    if todays_tasks:
        message += "🟢 Today's Tasks:\n"
        for task in todays_tasks:
            message += f"- {task.title}\n"
        message += "\n"

    message += "Keep studying smart! 📚\n\n- Your Smart Study Scheduler"

    send_email(to_email, subject, message)