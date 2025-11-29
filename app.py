from flask import Flask
from models import db, Selection


app = Flask(__name__)


@app.route("/")

def home():
    return  "hell ya its routing url"


@app.route("/user/")


def home():
    return  "hell ya its routing url"

if __name__ == '__main__':
    app.run(debug=True)