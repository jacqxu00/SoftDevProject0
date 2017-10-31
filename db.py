import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib

f="storytime.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

c.execute("CREATE TABLE users (user TEXT PRIMARY KEY, pass TEXT);")
c.execute("CREATE TABLE edit (id INT, user TEXT, section INT, content TEXT);")
c.execute("CREATE TABLE stories (id INT PRIMARY KEY, title TEXT, numsections INT);")

pw1 = hashlib.md5('crazy').hexdigest()
pw2 = hashlib.md5('pass').hexdigest()
pw3 = hashlib.md5('mashed').hexdigest()
c.execute("INSERT INTO users VALUES('bananas',\"%s\");"%(pw1))
c.execute("INSERT INTO users VALUES('jackie',\"%s\");"%(pw2))
c.execute("INSERT INTO users VALUES('potato',\"%s\");"%(pw3))
#==========================================================
db.commit() #save changes
db.close()  #close database

