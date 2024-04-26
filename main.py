import os
import smtplib
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from celery import Celery

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(SECRET_KEY)
app.config["CELERY_BROKER_URL"] = "redis://red-colo7ki0si5c73f5pim0:6379"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])

birthday = datetime(1987, 6, 22)


def calculate_age(birthday_date):
    current_date = datetime.now()
    age = (
        current_date.year
        - birthday_date.year
        - (
            (current_date.month, current_date.day)
            < (birthday_date.month, birthday_date.day)
        )
    )
    return age


@celery.task
def send_email(name, email, subject, message):
    email_message = (
        f"Subject:{subject}\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    )
    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=email_message.encode("utf-8"),
            )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
    return False


@app.route("/")
def home():
    age = calculate_age(birthday)
    return render_template("index.html", current_age=age)


@app.route("/contact", methods=["POST"])
def contact():
    if request.method == "POST":
        form_data = request.form
        send_email.delay(
            form_data["name"],
            form_data["email"],
            form_data["subject"],
            form_data["message"],
        )
        return "OK"


if __name__ == "__main__":
    app.run(debug=True)
