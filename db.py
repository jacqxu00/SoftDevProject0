import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="storytime.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

c.execute("CREATE TABLE users (user TEXT PRIMARY KEY, pass TEXT)")
c.execute("CREATE TABLE edit (id INT, user TEXT, section INT, content TEXT)")
c.execute("CREATE TABLE stories (id INT PRIMARY KEY, title TEXT, numsections INT)")

c.execute("INSERT INTO users VALUES('potato', 'mashed');")
c.execute("INSERT INTO stories VALUES (0, 'bananas', 1);")
c.execute("INSERT INTO edit VALUES (0, 'jackie', 1,'A girl liked bananas.');")

c.execute("INSERT INTO stories VALUES (1, 'cookies', 1);")
c.execute("INSERT INTO edit VALUES (0, 'potato', 1,'He stole a cookie.');")

#==========================================================
db.commit() #save changes
db.close()  #close database

