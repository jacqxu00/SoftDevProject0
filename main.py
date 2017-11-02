'''
Madonna's Pajamas
SoftDev Pd9
Project 0 Option 0
10.30.17
'''

from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3, hashlib
import os
#from utils import db


my_app = Flask (__name__)
my_app.secret_key = os.urandom(100)


f = "storytime.db"
db = sqlite3.connect(f, check_same_thread=False)  #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops


#c.execute("CREATE TABLE users (user TEXT PRIMARY KEY, pass TEXT)")
#c.execute("CREATE TABLE edit (id INT, user TEXT, section INT, content TEXT)")
#c.execute("CREATE TABLE stories (id INT PRIMARY KEY, title TEXT, numsections INT)")


username = ""
contrib = {} #dict, KEY: story id's the user in session has contributed to, VALUE: [title, numsections]
uncontrib = {} #dict, KEY: story id's the user in session has not contributed to, VALUE: [title, numsections]

#==========================================================

#creates two arrays, one for all the ids of the stories the user has contributed to, one for all the ids not contributed to

def printdict():
    print("CONTRIB:\n")
    for each in contrib:
        print("%d: %s, %d\n", contrib[each], contrib[each][0], contrib[each][1])
    print("UNCONTRIB:\n")
    for each in uncontrib:
        print("%d: %s, %d\n", uncontrib[each], uncontrib[each][0], uncontrib[each][1])

#populated contrib and uncontrib lists
def create(username):
    contributed_stories = []
    for id in  c.execute("SELECT id FROM edit WHERE user = \"%s\" ;" %(username)):
        contributed_stories.append(id[0])
    #pulls all story ids that user has contributed to
    print username
    print contributed_stories
    
    for story in contributed_stories:
        
        value = [] #creates a value array
        
        #finds the story title based on story id
        for story_title in c.execute("SELECT title FROM stories WHERE id = %d;" %(story)):
            value.append(story_title[0])
        
        #finds the number of sections in story using story id then finds the content of the section
        for recent_section in c.execute("SELECT content FROM edit WHERE id = %d AND section = 1;" %(story)):
            value.append(recent_section[0])

        value.append(story)
        
        #defines story id key as value
        contrib[story] = value

    uncontributed_stories = []    
    for id in c.execute("SELECT id FROM stories;"):
        uncontributed_stories.append(id[0])
    for id in contributed_stories:
        uncontributed_stories.remove(id)
    
    #pulls all story ids that user has not contributed to
    
    for story in uncontributed_stories:
        
        value = [] #creates a value array
        
        #finds the story title based on story id
        for story_title in c.execute("SELECT title FROM stories WHERE id = %d;" %(story)):
            value.append(story_title[0])
        
        #finds the number of sections in story using story id then finds the content of the section
        for recent_section in c.execute("SELECT content FROM edit WHERE id = %d AND section = 1;" %(story)):
            value.append(recent_section[0])

        value.append(story)
        
        #defines story id key as value
        uncontrib[story] = value

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
    inputPasshashed = hashlib.md5(inputPass).hexdigest()
    if password != inputPasshashed:
        return 1

    else:
        return 2

# function used for getting the ID when creating a story
def getID():
    current = 0
    for each in c.execute("SELECT * FROM stories;"):
        current += 1
    current += 1
    return current


# function that gets title of a story with its ID
def getTitle(id):
    c.execute("SELECT title FROM stories WHERE id = " + str(id))
    ans = c.fetchone()[0]
    return ans
 
#function that gets number of sections
def getLast(id):
    c.execute("SELECT numsections FROM stories WHERE id = " + str(id))
    ans = c.fetchone()[0]
    return ans
 
#function that gets most recent edit
def getPrev(id):
    c.execute("SELECT content FROM edit WHERE id = " + str(id) + " AND section = " + str(getLast(id)))
    ans = c.fetchone()[0]
    return ans
	
def getNext(id):
    ans = getLast(id) + 1
    return ans

#root: if user in session redirects to home route, else displays login.html
@my_app.route('/', methods=["POST", "GET"])
def root():
    if "user" in session:
        return redirect( url_for('home') )
    return render_template("login.html")

#if input username doesn't already exist, creates account and adds to database, then redirects back to login, else tells you to try a new username
@my_app.route('/register', methods=["POST", "GET"])
def register():
    user = request.form['username']
    password = request.form['password']
    for each in c.execute("SELECT user FROM users"):
        if each[0] == user:
            flash("Sorry, that username already exists. Try registering again.")
            return redirect( url_for("root") )
    pass_hashed = hashlib.md5(password).hexdigest()
    c.execute("INSERT INTO users VALUES (\"%s\", \"%s\");"%(user, pass_hashed))
    flash("Account creation successful. You may now log in.")
    return redirect( url_for("root") )


#home: if username and password authorized displays home.html, else redirects to root route
@my_app.route('/home', methods=["POST", "GET"])
def home():
    #print request.form
    if 'username' in request.form:
        #username = request.form['username']
        #print username + " here"
        #create()
        getUser = request.form['username']
        getPass = request.form['password']
        result = check(getUser, getPass)
        session["user"] = getUser
        username = request.form['username']
        create(username)
        if result == 0:
            flash("Sorry, your username does not exist. Try registering instead.")
            return redirect( url_for("root") )
        elif result == 1:
            flash("Sorry, your username and password do not match. Try again.")
            return redirect( url_for("root") )
        else:
            #print username + " here"
            return render_template("home.html", c = contrib) 
    elif 'title' in request.form:
        title = request.form['title']
        submit = request.form['section']
        c.execute("INSERT INTO edit VALUES (%d, \"%s\", %d, \"%s\");"%(getID(), session['user'], 1, submit))
        c.execute("INSERT INTO stories VALUES (%d, \"%s\", %d);"%(getID(), title, 1))
        return redirect(url_for("root"))
    elif 'next' in request.form:
        submit = request.form['next']
        id = int(request.form['id'])
        print getNext(id)
        print id
        c.execute("INSERT INTO edit VALUES (%d, \"%s\", %d, \"%s\");"%(id, session['user'], getNext(id), submit))
        c.execute("UPDATE stories SET numsections = %d WHERE id = %d;"%(getNext(id), id))
        return redirect(url_for("root"))
    else:
        return render_template("home.html", c = contrib)


#discover: goes to discover.html
@my_app.route('/discover', methods=["POST", "GET"])
def discover():
    create(username)
    #print uncontrib
    return render_template("discover.html", u = uncontrib)


#new: goes to new.html
@my_app.route('/new', methods=["POST", "GET"])
def new():
    return render_template("create.html")


#edit: goes to edit.html
@my_app.route('/edit', methods=["POST", "GET"])
def edit():
    id = request.form['id']
    id = int(id)
    c.execute("SELECT title FROM stories WHERE id = %d;"%(id))
    return render_template("edit.html", title = getTitle(id), previous = getPrev(id), key = id)

#story: goes to storypage.html of requested story
@my_app.route('/story', methods=["POST", "GET"])
def story():
    ppl_cont = [] #array of people who contributed to this story
    story_sec = [] #array of sections in the story
    story_id = int(request.form["story"])
    
    #pulls all story ids that user has contributed to
    contributors = c.execute("SELECT user FROM edit WHERE id = %d;" %(story_id))
    for each in contributors:
        #add each contributor to a list of contributors
        ppl_cont.append(each[0])
        
    #pulls all story ids that user has contributed to
    sections = c.execute("SELECT content FROM edit WHERE id = %d;" %(story_id))
    for each in sections:
        #add each section to a list of all sections
        story_sec.append(each[0])

    #receives story title for story id
    story_name = ""
    for each in c.execute("SELECT title FROM stories WHERE id = %d;" %(story_id)):
        story_name = each[0]
    
    if story_id in contrib:
        return render_template("storypage.html", title = story_name, contribs = ppl_cont, sections = story_sec)
    else:
        return redirect(url_for('edit')) #FIX make sure that this still gets the title?
    
    
#logout: removes session and redirects to root route
@my_app.route('/logout', methods=["POST", "GET"])
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
