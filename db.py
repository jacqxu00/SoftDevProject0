import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="storytime.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

c.execute("CREATE TABLE users (user TEXT PRIMARY KEY, pass TEXT)")
c.execute("CREATE TABLE edit (id INT PRIMARY KEY, user TEXT PRIMARY KEY, section INT, content TEXT)")
c.execute("CREATE TABLE users (id INT PRIMARY KEY, title TEXT, numsections INT)")

#==========================================================
db.commit() #save changes
db.close()  #close database

