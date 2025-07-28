from bson import ObjectId
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_bcrypt import Bcrypt
from flask_session import Session
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.jinja_env.globals.update(str=str)

# ✅ MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["book_catalog"]
books_collection = db["books"]
users_collection = db["users"]

# ✅ File upload config
UPLOAD_FOLDER = "static/covers"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

bcrypt = Bcrypt(app)

# ✅ HOME route
@app.route("/")
def home():
    if "username" in session:
        username = session["username"]
        books = list(books_collection.find({"username": username}))
        print("Books fetched:", books)
        return render_template("home.html", books=books)
    else:
        return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"Welcome, {session['username']}! <a href='/logout'>Logout</a>"
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form["password"]

        user = users_collection.find_one({"username": username})
        if user and bcrypt.check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form["password"]

        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            flash("Username already exists. Try logging in.", "error")
            return redirect(url_for("register"))

        hashed_pw = bcrypt.generate_password_hash("testpass").decode("utf-8")
        users_collection.insert_one({"username": "testuser", "password": hashed_pw})
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        genre = request.form["genre"]
        year = request.form["year"]
        description = request.form["description"]

        cover_file = request.files["cover"]
        cover_filename = None
        if cover_file and cover_file.filename:
            cover_filename = secure_filename(cover_file.filename)
            cover_path = os.path.join(app.config["UPLOAD_FOLDER"], cover_filename)
            cover_file.save(cover_path)

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "year": year,
            "description": description,
            "cover": cover_filename,
            "username": session["username"]
        }
        books_collection.insert_one(book)
        flash("Book added successfully!", "success")
        return redirect(url_for("home"))

    return render_template("add_book.html")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_book(id):
    if "username" not in session:
        return redirect(url_for("login"))

    book = books_collection.find_one({"_id": ObjectId(id)})

    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        genre = request.form["genre"]
        year = request.form["year"]
        description = request.form["description"]

        cover_file = request.files["cover"]
        cover_filename = book.get("cover")

        if cover_file and cover_file.filename:
            cover_filename = secure_filename(cover_file.filename)
            cover_path = os.path.join(app.config["UPLOAD_FOLDER"], cover_filename)
            cover_file.save(cover_path)

        books_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": title,
                "author": author,
                "genre": genre,
                "year": year,
                "description": description,
                "cover": cover_filename
            }}
        )
        flash("Book updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("edit_book.html", book=book)

@app.route("/delete/<id>", methods=["POST"])
def delete_book(id):
    if "username" not in session:
        return redirect(url_for("login"))

    book = books_collection.find_one({"_id": ObjectId(id)})

    if book and book.get("username") == session["username"]:
        books_collection.delete_one({"_id": ObjectId(id)})
        flash("Book deleted successfully!", "success")
    else:
        flash("You don't have permission to delete this book.", "error")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)