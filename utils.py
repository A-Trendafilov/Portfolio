import json
import smtplib
from datetime import datetime

from flask import current_app, render_template, g


def load_data(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"The data file was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"The data file contains invalid JSON.")


def initialize_data():
    try:
        site_data = load_data("./data/data.json")
        error_messages = load_data("./data/error.json")
        return site_data, error_messages, None
    except FileNotFoundError as err:
        return None, None, err


def handle_error(error_code, error_messages, exception=None):
    error_info = error_messages.get(str(error_code), error_messages["default"])
    error_message = error_info["error_message"]
    if exception:
        error_message += f"<br> Error details: {exception}"
    return (
        render_template(
            "error.html",
            error_code=error_code,
            error_description=error_info["error_description"],
            error_message=error_message,
        ),
        error_code,
    )


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


def send_email(name, email, subject, message):
    email_message = (
        f"Subject: {subject}\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Message: {message}"
    )
    try:
        with smtplib.SMTP(
            current_app.config["SMTP_SERVER"], current_app.config["SMTP_PORT"]
        ) as connection:
            connection.starttls()
            connection.login(
                current_app.config["EMAIL"], current_app.config["PASSWORD"]
            )
            connection.sendmail(
                from_addr=current_app.config["EMAIL"],
                to_addrs=current_app.config["EMAIL"],
                msg=email_message.encode("utf-8"),
            )
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Failed to send email: {e}")
