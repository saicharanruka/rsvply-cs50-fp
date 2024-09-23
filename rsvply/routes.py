from rsvply import app
from flask import url_for, render_template


@app.route("/")
@app.route("/home")
def main():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html", title="Login")

@app.route("/register")
def register():
    return render_template("register.html", title="Register")