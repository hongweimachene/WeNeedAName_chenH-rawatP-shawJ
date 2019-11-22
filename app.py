# Team mapp - Pratham Rawat, Hong Wei Chen, Yifan Wang, Justin Shaw
# SoftDev1 pd1
# P#01 - ArRESTed Development
# 2019-11-17

from flask import Flask, render_template, session, flash, request, redirect
import sqlite3, os
import datetime
import util
from util.user import User
from login_tool import login_required, current_user


app = Flask(__name__)

# db = sqlite3.connect("horoscope_dating.db") #open if file exists, otherwise create
# c = db.cursor()

app.secret_key = os.urandom(32)
#b# ========================================================================
#b# Site Interaction
@app.context_processor
def inject_current_user():
    return dict(current_user = current_user())

@app.route("/")
def start():
    if("username" in session): #Check if username is stored in site cookies
        print("Username Stored in Cache")
        return redirect("/welcome") #Redirects to Logged In Welcome Page
    return redirect("/login") #Redirect to Login Page to Login

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    return render_template("createAccounts.html");

@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    if(request.form["password"] != request.form["password-confirm"]):
        return redirect("/create")
    for data in request.form:
        if(len(request.form[data]) == 0):
            print("bad")
            flash("Please submit each request")
            return redirect("/create")
    try:
        User.new_user(request.form["username"], request.form["password"], request.form["name"], request.form["dob"], request.form["email"], request.form["phone"], request.form["bio"], "yeet")
    except:
        flash("Username already exists")
        return redirect("/create")
    # TODO: integrate API for horoscope data
    session["username"] = request.form["username"]
    if ("prev_url" in session):
        return redirect(session.pop("prev_url"))
    return redirect("/welcome")

@app.route("/auth", methods=["POST"])
def authenticate():
    #Getting data inputting in login form
    username = request.form["username"]
    password = request.form["pass"]
    #Getting username from database
    user_auth = authenticate(username, password)
    if(user_auth == -1):
        #Checks if username is in database
        flash("No Username Found")
        return redirect("/login")
    elif (user_auth == 0):
        flash("Your Password in Incorrect")
        return redirect("/login")
    else:
    #Passed all checks, good to login
        session["username"] = username
    if ("prev_url" in session):
        return redirect(session.pop("prev_url"))
    return redirect("/welcome")

@app.route("/welcome")
def welcomePage():
    return render_template("welcome.html")

@app.route("/logout")
def logout():
    if("username" in session):
        session.pop("username")
        flash("Successfully Logged Out")
    return redirect("/login")

if __name__ == "__main__":
    util.db_setup()
    app.debug = True
    app.run()
