# library imports
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# local imports
from games import initialFetch

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello World"


@app.before_first_request
def activate_job():
    client = MongoClient("mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/games?retryWrites=true&w=majority")

    if "games" not in client.list_database_names():
        print("Running inital fetch")
        initialFetch()
    else:
        print("Skipping initial fetch")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)