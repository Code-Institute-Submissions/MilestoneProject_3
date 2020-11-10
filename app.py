import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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


# Main Page
@app.route("/")
def all_items():
    # Find all items in item database
    items = mongo.db.items.find()
    return render_template("items.html", items=items)


# Registration modal
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Find a match in exsiting user database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # If a match is found and existing_user returns a username
        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("all_items"))
        # If no match is found
        else:
            # Store username/password into users database
            register = {"username": request.form.get("username").lower(),
                        "password": generate_password_hash(
                        request.form.get("password"))}
            mongo.db.users.insert_one(register)
            # Add username into session cookie
            session["user"] = request.form.get("username").lower()
            flash("You have been registered!")
            return redirect(url_for("all_items"))


# Login modal
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Locate any users with same username in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username2").lower()})
        if existing_user:
            # check if passwords are identical
            if check_password_hash(
                    existing_user["password"], request.form.get("password2")):
                # If match is obtained, save username to session cookie
                session["user"] = request.form.get("username2").lower()
                flash("Welcome, {}".format(request.form.get("username2")))
                return redirect(url_for("profile", username=session["user"]))
            # Password do not match
            else:
                flash("Incorrect Password/Password")
                return redirect(url_for("all_items"))
        else:
            # No username exists in user database
            flash("Incorrect Username/Password")
            return redirect(url_for("all_items"))


# Logout function
@app.route("/logout")
def logout():
    # Remove session cookie
    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for("all_items"))


# Profile page
@app.route("/profile/<username>")
def profile(username):
    # Find user and profile database for username
    user = mongo.db.users.find_one({"username": username})
    profile = mongo.db.profile.find_one({"username": username})

    return render_template('profile.html', username=user, profile=profile)


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        item_image = request.files["item_image"]
        mongo.save_file(item_image.filename, item_image)
        new_item = {"item_category": request.form.get("item_category"),
                    "item_image": item_image.filename,
                    "item_name": request.form.get("item_name"),
                    "item_description": request.form.get("item_description"),
                    "item_price": request.form.get("item_price"),
                    "username": session["user"],
                    "contact_number": request.form.get("contact_number"),
                    "email": request.form.get("email")}
        mongo.db.items.insert_one(new_item)
        flash("Item has been inserted")
        return redirect(url_for("all_items"))
    categories = list(mongo.db.categories.find())
    return render_template("add_item.html", categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
