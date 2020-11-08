import os
from flask import (
    Flask, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# Used to connect to mongodb
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# Used for session cookie
app.secret_key = os.environ.get("SECRET_KEY")
# creating mongodb using ["MONGO_URI"]
mongo = PyMongo(app)


@app.route("/")
def all_items():
    mongo.db.items.find()
    return render_template("/items")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
