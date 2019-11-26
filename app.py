# Team mapp - Pratham Rawat, Hong Wei Chen, Yifan Wang, Justin Shaw
# SoftDev1 pd1
# P#01 - ArRESTed Development
# 2019-11-17

from flask import Flask, render_template, session, flash, request, redirect
import sqlite3, os
import datetime
import util
from util.user import User
from util.request import Request
import util.api_request as api
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
            flash("Please enter a value in every field")
            return redirect("/create")
# new_user(username, password, name, gender, preference, dob, email, phone_number, bio, horoscope_info):
    # TODO: integrate API for horoscope data"""
    if not User.new_user(request.form["username"], request.form["password"], request.form["name"], request.form["gender"], request.form["preference"], request.form["dob"], request.form["email"], request.form["phone"], request.form["bio"], request.form["location"]):
        return redirect("/create")
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
    user_auth = User.authenticate_user(username, password)
    if not user_auth:
        return redirect("/login")
    else:
    #Passed all checks, good to login
        session["username"] = username
    if ("prev_url" in session):
        return redirect(session.pop("prev_url"))
    return redirect("/welcome")


@app.route("/welcome")
@login_required
def welcomePage():
    get_request = api.ohmanda(current_user().get_starsign())
    return render_template("welcome.html", horoscope=get_request)

@app.route("/hotsingles")
@login_required
def matchmaking():
    return f"{current_user().unmatched()}"
    """for person in query:
        this = util.matchmaker.Person(YEAR, MONTH, DAY) #Person object for current user (i just need the DOB)
        other = util.matchmaker.Person(YEAR, MONTH, DAY) #Person object for other user
        searchMatches[0] = #SQL for other person's name
        searchMatches[1] = matchmaker.personalityCompatibility(this, other)
        searchMatches[2] = matchmaker.sexualCompatibility(this, other)
        searchMatches[3] = matchmaker.inLawsCompatibility(this, other)
        searchMatches[4] = matchmaker.futureSuccess(this, other)
    return render_template("matchmaking.html", listings=searchMatches)"""

@app.route("/relation")
def updateRelations():
    userID = request.args["id"]
    newRelation = request.args["type"]
    # TODO: Add SQL Implementation to update the relationship
    redirect = session["prev_url"]
    session.pop("prev_url")
    return redirect(redirect)

@app.route("/logout")
def logout():
    if("username" in session):
        session.pop("username")
        flash("Successfully Logged Out")
    return redirect("/login")

@app.route("/requests")
def requests():
    return redirect("requests/recieved")

@app.route("/requests/recieved")
def recieved_requests():
    return render_template("recieved_requests.html")

@app.route("/requests/pending")
def pending_requests():
    return render_template("pending_requests.html")

@app.route("/requests/accepted")
def accepted_requests():
    return render_template("accepted_requests.html")

if __name__ == "__main__":
    util.db_setup()
    app.debug = True
    app.run()
