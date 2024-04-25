import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(SECRET_KEY)


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


birthday = datetime(1987, 6, 22)


@app.route("/")
def home():
    age = calculate_age(birthday)
    return render_template("index.html", current_age=age)


if __name__ == "__main__":
    app.run(debug=True)
