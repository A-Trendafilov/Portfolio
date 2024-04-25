import os
from datetime import datetime
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(SECRET_KEY)


@app.route("/")
def home():
    current_year = int(datetime.now().strftime("%Y"))
    return render_template("index.html", current_year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
