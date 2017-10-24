'''
Madonna's Pajamas
SoftDev Pd9
Project 0 Option 0
10.04.17
'''

from flask import Flask, render_template, request, session, redirect, url_for, flash
import os


my_app = Flask (__name__)
my_app.secret_key = os.urandom(100)

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
    return render_template("home.html")


#discover: goes to discover.html
@my_app.route('/discover')
def discover():


#new: goes to new.html
@my_app.route('/new')
def new():
    
    
#edit: goes to edit.html
@my_app.route('/edit')
def edit():
    

#logout: removes session and redirects to root route
@my_app.route('/logout')
def logout():
    
    
if __name__ == '__main__':
    my_app.debug = True
    my_app.run()