# Team mapp - Pratham Rawat, Hong Wei Chen, Yifan Wang, Justin Shaw
# SoftDev1 pd1
# P#01 - ArRESTed Development
# 2019-11-17

from flask import Flask, render_template, session, flash, request, redirect
import sqlite3, os
import datetime
import util
import util.matchmaker
from util.user import User
from util.request import Request
import util.api_request as api
from login_tool import login_required, current_user
import json

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
    print(f"Ohmanda request: {get_request}")
    print(current_user().dob)
    print(current_user().get_starsign())
    return render_template("welcome.html", horoscope=json.loads(get_request))

@app.route("/hotsingles")
@login_required
def matchmaking():
    # return f"{current_user().unmatched()}"
    counter = 0;
    searchMatches = [[[None] for x in range(10)] for y in range(50)];
    print(current_user().unmatched())
    for person in current_user().unmatched():
        try:
            userDOB = current_user().dob.split("-")
            this = util.matchmaker.Person(userDOB[0], userDOB[1], userDOB[2])
            otherDOB = User.query_by_id(person, "dob").split("-")
            other = util.matchmaker.Person(otherDOB[0], otherDOB[1], otherDOB[2]) #Person object for other user
            searchMatches[counter][0] = User.query_by_id(person, "name")
            searchMatches[counter][1] = util.matchmaker.personalityCompatibility(this, other)
            searchMatches[counter][2] = util.matchmaker.sexualCompatibility(this, other)
            searchMatches[counter][3] = util.matchmaker.inLawsCompatibility(this, other)
            searchMatches[counter][4] = util.matchmaker.futureSuccess(this, other)
            searchMatches[counter][5] = User.query_by_id(person, "bio")
            searchMatches[counter][6] = person
            counter += 1
            if(counter > 45 or counter == len(searchMatches) - 1):
                break;
        except Exception as e:
            print(e)
    session["prev_url"] = "/hotsingles"
    return render_template("matchmaking.html", listings=searchMatches)

@app.route("/relation")
@login_required
def updateRelations():
    userID = request.args["id"]
    newRelation = request.args["type"]
    Request.new_request(current_user().id, userID, newRelation, "")
    url = session["prev_url"]
    session.pop("prev_url")
    return redirect(url)

@app.route("/logout")
@login_required
def logout():
    if("username" in session):
        session.pop("username")
        flash("Successfully Logged Out")
    return redirect("/login")

@app.route("/requests")
@login_required
def requests():
    return redirect("/requests/recieved")

@app.route("/requests/recieved")
@login_required
def recieved_requests():
    recieved = current_user().recieved_pending()
    counter = 0;
    searchMatches = [[[None] for x in range(10)] for y in range(50)];
    for person in recieved:
        try:
            userDOB = current_user().dob.split("-")
            this = util.matchmaker.Person(userDOB[0], userDOB[1], userDOB[2])
            otherDOB = User.query_by_id(person, "dob").split("-")
            other = util.matchmaker.Person(otherDOB[0], otherDOB[1], otherDOB[2]) #Person object for other user
            searchMatches[counter][0] = User.query_by_id(person, "name")
            searchMatches[counter][1] = util.matchmaker.personalityCompatibility(this, other)
            searchMatches[counter][2] = util.matchmaker.sexualCompatibility(this, other)
            searchMatches[counter][3] = util.matchmaker.inLawsCompatibility(this, other)
            searchMatches[counter][4] = util.matchmaker.futureSuccess(this, other)
            searchMatches[counter][5] = User.query_by_id(person, "bio")
            searchMatches[counter][6] = person
            counter += 1
            if(counter > 45 or counter == len(searchMatches) - 1):
                break;
        except Exception as e:
            print(e)
    session["prev_url"] = "/requests/recieved"
    return render_template("received_requests.html", listings=searchMatches)

@app.route("/requests/pending")
@login_required
def pending_requests():
    recieved = current_user().sent_pending()
    counter = 0;
    searchMatches = [[[None] for x in range(10)] for y in range(50)];
    for person in recieved:
        try:
            userDOB = current_user().dob.split("-")
            this = util.matchmaker.Person(userDOB[0], userDOB[1], userDOB[2])
            otherDOB = User.query_by_id(person, "dob").split("-")
            other = util.matchmaker.Person(otherDOB[0], otherDOB[1], otherDOB[2]) #Person object for other user
            searchMatches[counter][0] = User.query_by_id(person, "name")
            searchMatches[counter][1] = util.matchmaker.personalityCompatibility(this, other)
            searchMatches[counter][2] = util.matchmaker.sexualCompatibility(this, other)
            searchMatches[counter][3] = util.matchmaker.inLawsCompatibility(this, other)
            searchMatches[counter][4] = util.matchmaker.futureSuccess(this, other)
            searchMatches[counter][5] = User.query_by_id(person, "bio")
            searchMatches[counter][6] = person
            counter += 1
            if(counter > 45 or counter == len(searchMatches) - 1):
                break;
        except Exception as e:
            print(e)
    session["prev_url"] = "/requests/pending"
    return render_template("pending_requests.html", listings=searchMatches)
#
# @app.route("/requests/accepted")
# @login_required
# def accepted_requests():
#     #SQL to get list of people who have requested the current user from the database, as well as their DOBs
#     #for person in query:
#         this = util.matchmaker.Person(YEAR, MONTH, DAY) #Person object for current user (i just need the DOB)
#         other = util.matchmaker.Person(YEAR, MONTH, DAY) #Person object for other user
#         searchMatches[0] = #SQL for other person's name
#         searchMatches[1] = #SQL for the other person's email
#         searchMatches[2] = #SQL for the other person's phone number
#         searchMatches[3] = #SQL for the other person's bio
#         searchMatches[4] = #SQL for the other person's location
#     return render_template("accepted_requests.html", listings=searchMatches)

if __name__ == "__main__":
    util.db_setup()
    app.debug = True
    app.run()
