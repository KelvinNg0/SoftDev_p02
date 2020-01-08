from flask import *
import os #for generating a secret key
import urllib.request
import json
from utl import db_ops

app = Flask(__name__)

#========================================
#Secret key handling
secret_key_file = 'secret_key.txt'
if (os.path.exists(secret_key_file)): #check if secret key file already exists on disk
	file = open(secret_key_file, 'r')
	app.secret_key = file.read()
else: #don't want this to ever get pushed to GitHub (in .gitignore), so generate one on the spot for ppl without the file
	file = open(secret_key_file, 'w+') #w+ creates the file if it doesn't exist
	file.write(str(os.urandom(32)))
	app.secret_key = file.read()

file.close()
#========================================

#If logged in: show clicker page, else login page
@app.route('/')
def home():
	if 'username' in session:
		print("Session username: " + session['username'])
		flash("You are logged in.")
		return render_template("clicker.html", title = "Cookie Clicker")

	return render_template("login.html", title = "Login")

@app.route('/login', methods=['POST'])
def login():
	username = request.form.get('user')
	password = request.form.get('pw')

	if (db_ops.authenticate(username, password)):
		session['username'] = username
		return redirect(url_for('home')) #should trigger if statement in home route

	flash("Failed to log in. The username/password combination provided did not match any accounts.")
	return redirect(url_for('home'))

#Need this route since the anchor element on the login page for creating an account links to this
@app.route('/signup')
def signup():
	return render_template("register.html", title = "Register")

@app.route("/register", methods=['POST'])
def register():
	username = request.form.get('user')
	password = request.form.get('pw')

	if (db_ops.accountExists(username)):
		flash("This username is already in use. Try another one.")
		return redirect(url_for('signup'))

	db_ops.addAccount(username, password)
	flash("You have successfully created your account. Please sign in now.")
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	if 'username' in session: #checks that a user is logged in, in the first place
		session.pop('username')
		flash("You have been logged out.")
		return redirect(url_for('home'))

	flash("You are already logged out.")
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.debug = True;
	app.run();
