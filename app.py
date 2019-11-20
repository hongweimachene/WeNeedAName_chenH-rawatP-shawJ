# Team mapp - Pratham Rawat, Hong Wei Chen, Yifan Wang, Justin Shaw
# SoftDev1 pd1
# P#01 - ArRESTed Development
# 2019-11-17

from flask import Flask, render_template, session, flash, request, redirect
import sqlite3, os
import datetime

app = Flask(__name__)

db = sqlite3.connect("horoscope_dating.db") #open if file exists, otherwise create
c = db.cursor()

app.secret_key = os.urandom(32)
#b# ========================================================================
#b# Site Interaction

@app.route("/")
def start():
    if("username" in session): #Check if username is stored in site cookies
        print("Username Stored in Cache")
        return redirect("/welcome") #Redirects to Logged In Welcome Page
    return redirect("/login") #Redirect to Login Page to Login

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/create")
def create():
    return render_template("createAccount.html");

@app.route("/createAccount", methods=["POST"]):
def createAccount():
    return ""

@app.route("/auth", methods=["POST"])
def authenticate():
    #Getting data inputting in login form
    username = request.form["username"]
    password = request.form["password"]
    #Getting username from database
    c.execute("""SELECT users.username FROM users WHERE username = '{}';""".format(username))
    data = c.fetchall()
    if(len(data) == 0):
        #Checks if username is in database
        flash("No Username Found")
        return redirect("/login")
    else:
        #Getting passwords from database
        c.execute("""SELECT users.password FROM users WHERE username = '{}';""".format(username))
        data = c.fetchall()
        if(data[0] != password):
            #Checks if password is correct if the username exists
            flash("Your Password in Incorrect")
            return redirect("/login")
    #Passed all checks, good to login
    session["username"] = username
    return redirect("/welcome");

@app.route("/welcome")
def welcomePage():
    return render_template("welcome.html")

@app.route("/logout")
def logout()

if __name__ == "__main__":
    c.execute("""CREATE TABLE IF NOT EXISTS 'users' (userID INT PRIMARY KEY,
                                                     username STRING,
                                                     password STRING,
                                                     name STRING,
                                                     dob TIMESTAMP,
                                                     email STRING,
                                                     phone_number STRING,
                                                     bio STRING)""")
	app.debug = True
	app.run()
