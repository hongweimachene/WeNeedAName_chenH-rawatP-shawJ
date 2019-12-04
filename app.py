# Team WeNeedAName - Pratham Rawat, Hong Wei Chen, Yifan Wang, Justin Shaw
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
import randomUsers
import json



app = Flask(__name__)

# db = sqlite3.connect("horoscope_dating.db") #open if file exists, otherwise create
# c = db.cursor()

app.secret_key = os.urandom(32)
#b# ========================================================================
#b# Site Interaction

starsign_compatibilites = {
    "aries": {"aries": 60, "taurus": 65, "gemini": 65, "cancer": 65, "leo": 90,
              "virgo": 45, "libra": 70, "scorpio": 80, "sagittarius": 90,
              "capricorn": 50, "aquarius": 55, "pisces": 65},
    "taurus": {"aries": 60, "taurus": 70, "gemini": 70, "cancer": 80, "leo": 70,
              "virgo": 90, "libra": 75, "scorpio": 85, "sagittarius": 50,
              "capricorn": 95, "aquarius": 80, "pisces": 85},
    "gemini": {"aries": 70, "taurus": 70, "gemini": 75, "cancer": 60, "leo": 80,
              "virgo": 75, "libra": 90, "scorpio": 60, "sagittarius": 75,
              "capricorn": 50, "aquarius": 90, "pisces": 50},
    "cancer": {"aries": 65, "taurus": 80, "gemini": 60, "cancer": 75, "leo": 70,
              "virgo": 75, "libra": 60, "scorpio": 95, "sagittarius": 55,
              "capricorn": 45, "aquarius": 70, "pisces": 90},
    "leo": {"aries": 90, "taurus": 70, "gemini": 80, "cancer": 70, "leo": 85,
              "virgo": 75, "libra": 65, "scorpio": 75, "sagittarius": 95,
              "capricorn": 45, "aquarius": 70, "pisces": 75},
    "virgo": {"aries": 45, "taurus": 90, "gemini": 75, "cancer": 75, "leo": 75,
              "virgo": 70, "libra": 80, "scorpio": 85, "sagittarius": 70,
              "capricorn": 95, "aquarius": 50, "pisces": 70},
    "libra": {"aries": 70, "taurus": 75, "gemini": 90, "cancer": 60, "leo": 65,
              "virgo": 80, "libra": 80, "scorpio": 85, "sagittarius": 80,
              "capricorn": 85, "aquarius": 95, "pisces": 50},
    "scorpio": {"aries": 80, "taurus": 85, "gemini": 60, "cancer": 95, "leo": 70,
              "virgo": 85, "libra": 85, "scorpio": 90, "sagittarius": 80,
              "capricorn": 65, "aquarius": 60, "pisces": 95},
    "sagittarius": {"aries": 90, "taurus": 50, "gemini": 75, "cancer": 55, "leo": 95,
              "virgo": 70, "libra": 80, "scorpio": 85, "sagittarius": 85,
              "capricorn": 55, "aquarius": 60, "pisces": 75},
    "capricorn": {"aries": 50, "taurus": 95, "gemini": 50, "cancer": 45, "leo": 45,
              "virgo": 95, "libra": 85, "scorpio": 65, "sagittarius": 55,
              "capricorn": 85, "aquarius": 70, "pisces": 85},
    "aquarius": {"aries": 55, "taurus": 80, "gemini": 90, "cancer": 70, "leo": 70,
              "virgo": 50, "libra": 95, "scorpio": 60, "sagittarius": 60,
              "capricorn": 70, "aquarius": 80, "pisces": 55},
    "pisces": {"aries": 65, "taurus": 85, "gemini": 50, "cancer": 90, "leo": 75,
              "virgo": 70, "libra": 50, "scorpio": 95, "sagittarius": 75,
              "capricorn": 85, "aquarius": 55, "pisces": 80}
}
#makes current_user a global template variable
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
    loc_info = api.json2dict(api.ip_location(api.user_ip())) #current ip location
    if not User.new_user(request.form["username"], request.form["password"], request.form["name"], request.form["gender"], request.form["preference"], request.form["dob"], request.form["email"], request.form["phone"], request.form["bio"], f"{loc_info['lat']},{loc_info['lon']}"):
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
        current_user().update_location()
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
    counter = 0
    searchMatches = []
    print(current_user().unmatched())
    for person in current_user().unmatched():
        if(counter > 45):
            break
        # try:
        info = []
        userDOB = current_user().dob.split("-")
        this = util.matchmaker.Person(userDOB[0], userDOB[1], userDOB[2])
        otherDOB = User.query_by_id(person, "dob").split("-")
        other = util.matchmaker.Person(otherDOB[0], otherDOB[1], otherDOB[2]) #Person object for other user
        other_user = User(person)
        info.append(other_user.name)
        info.append(round((util.matchmaker.personalityCompatibility(this, other))*100))
        info.append(round((util.matchmaker.sexualCompatibility(this, other))*100))
        info.append(round((util.matchmaker.inLawsCompatibility(this, other))*100))
        info.append(round((util.matchmaker.futureSuccess(this, other))*100))
        info.append(other_user.bio)
        info.append(person)
        info.append(round(current_user().user_dist(person)))
        info.append(other_user.get_starsign().capitalize())
        info.append(starsign_compatibilites[current_user().get_starsign()][other_user.get_starsign()])
        counter += 1
        searchMatches.append(info)
        # except Exception as e:
        #     print(e)
    searchMatches.sort(key = lambda x : x[7])
    session["prev_url"] = "/hotsingles"
    return render_template("matchmaking.html", listings=searchMatches)

@app.route("/relation") #change relations
@login_required
def updateRelations():
    '''Refreshes page and updates the database'''
    userID = request.args["id"]
    newRelation = request.args["type"]
    Request.new_request(current_user().id, userID, newRelation, "")
    return redirect(session.pop("prev_url"))

@app.route("/logout")
@login_required
def logout():
    '''Logs the user out'''
    if("username" in session):
        session.clear()
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
    counter = 0
    searchMatches = []
    try:
        for person in recieved:
            if(counter > 45):
                break
            info = []
            userDOB = current_user().dob.split("-")
            this = util.matchmaker.Person(userDOB[0], userDOB[1], userDOB[2])
            otherDOB = User.query_by_id(person, "dob").split("-")
            other = util.matchmaker.Person(otherDOB[0], otherDOB[1], otherDOB[2]) #Person object for other user
            other_user = User(person)
            info.append(other_user.name)
            info.append(round((util.matchmaker.personalityCompatibility(this, other))*100))
            info.append(round((util.matchmaker.sexualCompatibility(this, other))*100))
            info.append(round((util.matchmaker.inLawsCompatibility(this, other))*100))
            info.append(round((util.matchmaker.futureSuccess(this, other))*100))
            info.append(other_user.bio)
            info.append(person)
            info.append(round(current_user().user_dist(person)))
            info.append(other_user.get_starsign().capitalize())
            info.append(starsign_compatibilites[current_user().get_starsign()][other_user.get_starsign()])
            counter += 1
            searchMatches.append(info)
    except Exception as e:
        print(e)
    session["prev_url"]= "/requests/recieved"
    return render_template("received_requests.html", listings=searchMatches)

@app.route("/requests/pending")
@login_required
def pending_requests():
    '''This function handles the requests that the user has sent to other users, stores and displays them'''
    recieved = current_user().sent_pending()
    counter = 0
    searchMatches = []
    try:
        for person in recieved:
            if(counter > 45):
                break
            info = []
            userDOB = current_user().dob.split("-")
            this = util.matchmaker.Person(userDOB[0], userDOB[1], userDOB[2])
            otherDOB = User.query_by_id(person, "dob").split("-")
            other = util.matchmaker.Person(otherDOB[0], otherDOB[1], otherDOB[2]) #Person object for other user
            other_user = User(person)
            info.append(other_user.name)
            info.append(round((util.matchmaker.personalityCompatibility(this, other))*100))
            info.append(round((util.matchmaker.sexualCompatibility(this, other))*100))
            info.append(round((util.matchmaker.inLawsCompatibility(this, other))*100))
            info.append(round((util.matchmaker.futureSuccess(this, other))*100))
            info.append(other_user.bio)
            info.append(person)
            info.append(round(current_user().user_dist(person)))
            info.append(other_user.get_starsign().capitalize())
            info.append(starsign_compatibilites[current_user().get_starsign()][other_user.get_starsign()])
            counter += 1
            searchMatches.append(info)
    except Exception as e:
        print(e)
    session["prev_url"]= "/requests/pending"
    return render_template("pending_requests.html", listings=searchMatches)
#
@app.route("/requests/accepted")
@login_required
def accepted_requests():
    '''This function handles requests from the user that have been accepted from another user, stores and displays them'''
    recieved = current_user().accepted()
    counter = 0
    searchMatches = []
    try:
        for person in recieved:
            if(counter > 45):
                break
            info = []
            match = User(person)
            info.append(match.name)
            info.append(match.email)
            info.append(match.phone_number)
            info.append(match.bio)
            info.append(match.location)
            info.append(person)
            info.append(round(current_user().user_dist(person)))
            counter += 1
            searchMatches.append(info)
    except Exception as e:
        print(e)
    session["prev_url"]= "/requests/accepted"
    return render_template("accepted_requests.html", listings=searchMatches)

if __name__ == "__main__":
    util.db_setup()
    randomUsers.populate()
    app.debug = True
    app.run()
