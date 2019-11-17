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
def loggingIn():
    return render_template("start.html");

if __name__ == "__main__":
	app.debug = True
	app.run()
