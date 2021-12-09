from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        found_user = users.query.filter_by(username=username, password=password).first()

        if found_user:
            return render_template("user.html")
        else:
            usr = users(username, password)
            db.session.add(usr)
            db.session.commit()
            return "<h1>Account created!</h1>"
    else:
        return render_template("login.html")

db.create_all()
app.run()
