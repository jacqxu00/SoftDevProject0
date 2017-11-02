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

c.execute("INSERT INTO stories VALUES(0, 'Pizza Man', 1);")
c.execute("INSERT INTO edit VALUES(0, 'bananas', 1, 'There once was a pizza man who delivered pizzas');")
c.execute("INSERT INTO stories VALUES(1, 'The Dirty Wall', 1);")
c.execute("INSERT INTO edit VALUES(1, 'jackie', 1, 'The wall was dirty.');")
c.execute("INSERT INTO stories VALUES(2, 'Huge Scandal', 1);")
c.execute("INSERT INTO edit VALUES(2, 'potato', 1, 'Huge scaldal is huge scandal but with an l.');")
#==========================================================
db.commit() #save changes
db.close()  #close database

