# import the flask class  from the flask template
from  flask import Flask, render_template, redirect, \
		url_for, request, session, flash
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy 

from functools import wraps # Authontications
import sqlite3 # importing sqlite3

# create the application  object
app = Flask(__name__) 

#app.secret_key = "my precious"
#app.database = "sample.db" #select database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object('config.BaseConfig')
#import os
#app.config.from_object(os.environ['APP_SETTINGS'])

#create the  sqlalchemy object
db = SQLAlchemy(app)
from models import *


#login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap


# use decorators  to link the function to  a url
@app.route('/')
@login_required
def index():
	posts = db.session.query(BlogPost).all()
	return render_template("index.html", posts=posts)



@app.route('/profile')
@login_required
def profile():
	return render_template("profile.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('You were just logged in')
			return redirect(url_for('profile'))
	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out')
	return redirect(url_for('index'))


# function which connets database to the application
def connect_db():
	return sqlite3.connect('posts.db')

#start the server with the  'run()' method

if __name__ == '__main__':
	app.run()