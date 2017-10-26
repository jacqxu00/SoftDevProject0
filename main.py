'''
Madonna's Pajamas
SoftDev Pd9
Project 0 Option 0
10.30.17
'''

from flask import Flask, render_template, request, session, redirect, url_for, flash, sqlite3
import os


my_app = Flask (__name__)
my_app.secret_key = os.urandom(100)


f = "storytime.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

username = ""
contrib = []
uncontrib = []

#==========================================================

#creates two arrays, one for all the ids of the stories the user has contributed to, one for all the ids not contributed to
def create():
    contributed_stories = c.execute("SELECT id FROM edit WHERE user = username;") #pulls all story ids that user has contributed to
    for story in contributed_stories:
        #add each id to a list of ids
        contrib.append(story[0])
    uncontributed_stories = c.execute("SELECT id FROM edit WHERE user != username;") #pulls all story ids that user has not contributed to
    for story in uncontributed_stories:
        #add each id to a list of ids
        uncontrib.append(story[0])

#checks to see if username is valid, and password is correct
#returns: 0 if username is invalid, 1 if username valid password is incorrect, 2 if successful login
def check(inputUser, inputPass):
    userList = c.execute("SELECT user FROM users;")
    userExist = False
    for each in userList:
        if each[0] == inputUser:
            userExist = True
    if userExist == False:
        return 0

    password = ''
    for each in c.execute("SELECT pass FROM users WHERE user = \"%s\";"%inputUser):
        password = each[0]
    if password != inputPass:
        return 1

    else:
        return 2

def auth():
    getUser = request.form['username']
    getPass = request.form['password']
    result = check(getUser, getPass)
    if result == 0:
 	flash("Sorry, your username does not exist. Try registering instead.")
	return redirect( url_for("root") )
    elif result == 1:
	flash("Sorry, your username and password do not match. Try again.")
	return redirect( url_for("root") )
    else:
	session.add(getUser)
	return render_template("home.html", c = contrib) )
 
#root: if user in session redirects to home route, else displays login.html
@my_app.route('/')
def root():
    if "user" in session:
        return redirect( url_for('home') )
    return render_template("login.html")


#home: if user in sesson displays home.html, else redirects to root route
@my_app.route('/home')
def home():
    auth()


#discover: goes to discover.html
@my_app.route('/discover')
def discover():
    return render_template("home.html", u = uncontrib)

#new: goes to new.html
@my_app.route('/new')
def new():
    
    
#edit: goes to edit.html
@my_app.route('/edit')
def edit():
    

#logout: removes session and redirects to root route
@my_app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user")
    return redirect( url_for("root") )
    
if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
    
#==========================================================
db.commit() #save changes
db.close()  #close database
