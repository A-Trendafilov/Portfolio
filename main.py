import os

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(SECRET_KEY)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)