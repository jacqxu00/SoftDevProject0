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
contrib = [] #array of story id's the user in session has contributed to
uncontrib = [] #array of story id's the user in session has not contributed to

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
def auth():


#root: if user in session redirects to home route, else displays login.html
@my_app.route('/')
def root():
    #if username is invalid: suggests pressing register account instead
    #if username is valid and password is incorrect: flash error


#home: if user in sesson displays home.html, else redirects to root route
@my_app.route('/home')
def home():
    return render_template("home.html", c = contrib)


#discover: goes to discover.html
@my_app.route('/discover')
def discover():
    return render_template("discover.html", u = uncontrib)

#new: goes to new.html
@my_app.route('/new')
def new():
    
    
#edit: goes to edit.html
@my_app.route('/edit')
def edit():
    

#story: goes to storypage.html of requested story
@my_app.route('/story')
def story():
    story_name = "something" #FIX request.form['story']
    ppl_cont = [] #array of people who contributed to this story
    story_sec = [] #array of sections in the story
    story_id = 0 #FIX story_id to equal the story id of story
    contributors = c.execute("SELECT user FROM edit WHERE id = story_id;") #pulls all story ids that user has contributed to
    for each in contributors:
        #add each contributor to a list of contributors
        ppl_cont.append(each[0])
    sections = c.execute("SELECT content FROM edit WHERE id = story_id;") #pulls all story ids that user has contributed to
    for each in sections:
        #add each section to a list of all sections
        story_sec.append(each[0])
    if story_id in contrib:
        return render_template("storypage.html", title = story_name, contribs = ppl_cont, sections = story_sec)
    else:
        return redirect(url_for('edit')) #FIX make sure that this still gets the title?
    
    
#logout: removes session and redirects to root route
@my_app.route('/logout')
def logout():
    
    
if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
    
#==========================================================
db.commit() #save changes
db.close()  #close database