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
    '''Redirect to welcome if session is activate, otherwise redirect to login'''
    if("username" in session): #Check if username is stored in site cookies
        print("Username Stored in Cache")
        return redirect("/welcome") #Redirects to Logged In Welcome Page
    return redirect("/login") #Redirect to Login Page to Login

@app.route("/login")
def login():
    '''Assigns astronomy picture of the day to user login'''
    if(not "apod" in session):
        try:
            session["apod"] = api.json2dict(api.APOD("DEMO_KEY"))["hdurl"]
            # The DEMO_KEY is used here due to caching essentially making the limit almost impossible to reach as the file is never removed
            # Adding a key to the code would not be in the interests of a user, and so we have left it out
        except Exception as e:
            print(e)
            session["apod"] = "bg1.jpg"
    return render_template("login.html", bg=session["apod"])

@app.route("/create", methods=["GET", "POST"])
def create():
    return render_template("createAccounts.html");

@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    '''When you create an account, you have to submit a bunch of personal information'''
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
    '''Authentication function to log stored users in'''
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
        print(session)
        print(current_user().id)
    if ("prev_url" in session):
        return redirect(session.pop("prev_url"))
    return redirect("/welcome")


@app.route("/welcome")
@login_required
def welcomePage():
    '''The welcome page displays a bunch of links the user can click, as well as displaying a horoscope from our API'''
    get_request = api.ohmanda(current_user().get_starsign())
    print(f"Ohmanda request: {get_request}")
    print(current_user().dob)
    print(current_user().get_starsign())
    return render_template("welcome.html", horoscope=json.loads(get_request), name=current_user().name)

@app.route("/hotsingles")
@login_required
def matchmaking():
    '''The matchmaking function measures compatibility with other users in the database using available user data,
    and displays the data'''
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
    '''Refreshes page and updates database'''
    userID = request.args["id"]
    newRelation = request.args["type"]
    Request.new_request(current_user().id, userID, newRelation, "")
    url = session["prev_url"]
    session.pop("prev_url")
    return redirect(url)

@app.route("/logout")
@login_required
def logout():
    '''Logs the user out'''
    if("username" in session):
        session.pop("username")
        flash("Successfully Logged Out")
    return redirect("/login")

@app.route("/requests")
@login_required
def requests():
    '''Sends user to requests page'''
    return redirect("/requests/recieved")

@app.route("/requests/recieved")
@login_required
def recieved_requests():
    '''This function handles the requests that are sent to the user, stores and displays them on screen'''
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
    '''This function handles the requests that the user has sent to other users, stores and displays them'''
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
@app.route("/requests/accepted")
@login_required
def accepted_requests():
    '''This function handles requests from the user that have been accepted from another user, stores and displays them'''
    recieved = current_user().accepted()
    counter = 0;
    searchMatches = [[[None] for x in range(10)] for y in range(50)];
    for person in recieved:
        try:
            searchMatches[counter][0] = User.query_by_id(person, "name")
            searchMatches[counter][1] = User.query_by_id(person, "email")
            searchMatches[counter][2] = User.query_by_id(person, "phone_number")
            searchMatches[counter][3] = User.query_by_id(person, "bio")
            searchMatches[counter][4] = User.query_by_id(person, "location")
            searchMatches[counter][5] = person
            counter += 1
            if(counter > 45 or counter == len(searchMatches) - 1):
                break;
        except Exception as e:
            print(e)
    session["prev_url"] = "/requests/pending"
    return render_template("accepted_requests.html", listings=searchMatches)

if __name__ == "__main__":
    util.db_setup()
    app.debug = True
    app.run()
