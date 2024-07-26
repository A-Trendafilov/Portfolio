import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request
from utils import send_email, calculate_age, initialize_data, handle_error

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["EMAIL"] = os.getenv("EMAIL")
app.config["PASSWORD"] = os.getenv("PASSWORD")
app.config["SMTP_SERVER"] = os.getenv("SMTP_SERVER")
app.config["SMTP_PORT"] = int(os.getenv("SMTP_PORT"))
birthday_str = os.getenv("BIRTHDAY")

site_data, error_messages, data_error = initialize_data()


@app.route("/")
def home():
    try:
        if site_data is None:
            raise FileNotFoundError(data_error)
        birthday_date = datetime.strptime(birthday_str, "%Y-%m-%d")
        age = calculate_age(birthday_date)
        return render_template("index.html", current_age=age, data=site_data)
    except FileNotFoundError as e:
        return handle_error(404, error_messages, e)
    except ValueError as e:
        return handle_error(500, error_messages, e)
    except Exception as e:
        return handle_error(500, error_messages, e)


@app.route("/portfolio/<int:id>")
def portfolio(id):
    try:
        if site_data is None:
            raise FileNotFoundError(data_error)
        project = next(
            (item for item in site_data["portfolio"]["projects"] if item["id"] == id),
            None,
        )
        if project:
            return render_template("portfolio_details.html", project=project)
        else:
            return handle_error(404, error_messages)
    except Exception as e:
        return handle_error(500, error_messages, e)


@app.route("/contact", methods=["POST"])
def contact():
    try:
        if request.method == "POST":
            form_data = request.form
            send_email(
                form_data["name"],
                form_data["email"],
                form_data["subject"],
                form_data["message"],
            )
            return "OK"
    except ValueError as e:
        return handle_error(400, error_messages, e)
    except Exception as e:
        return handle_error(500, error_messages, e)


if __name__ == "__main__":
    app.run(debug=True)
