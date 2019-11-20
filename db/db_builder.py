import sqlite3

file = "horoscope_dating.db"

db_ex(cmd):
    db = sqlite3.connect(file) #open if file exists, otherwise create
    c = db.cursor()
    c.execute(cmd)
    db.commit()

db_setup():
    db_ex("DROP TABLE IF EXISTS \"users\"")
    db_ex("DROP TABLE IF EXISTS \"requests\"")
    db_ex("CREATE TABLE \"users\""
          "(id INTEGER PRIMARY KEY,"
          "username VARCHAR,"
          "password VARCHAR,"
          "name VARCHAR,"
          "dob VARCHAR,"
          "email VARCHAR,"
          "phone_number VARCHAR,"
          "bio VARCHAR)")

db_setup()
