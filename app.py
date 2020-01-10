from flask import *
import os #for generating a secret key
import sqlite3
from functools import wraps

from utl import db_ops
from utl import api

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

#login_required wrapper
#========================================
def login_required(f):
    '''Login function'''
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            session['prev_url'] = url_for(f"{f.__name__}")
            return redirect(url_for('home'))
    return wrap

#If logged in: show clicker page, else login page
@app.route('/')
def home():
	if 'username' in session:
		print("Session username: " + session['username'])
		if 'prev_url' in session:
			return redirect(session.pop("prev_url"))

		return redirect(url_for('clicker'))

	return render_template("login.html", title = "Login")

@app.route('/login', methods=['GET','POST'])
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
	confirm_password = request.form.get('confirmpw')

	if (password != confirm_password):
		flash("The two passwords do not match.")
		return redirect(url_for('signup'))

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

@app.route('/clicker', methods = ['GET', 'POST'])
@login_required
def clicker():
	return render_template("clicker.html", title = "Cookie Clicker")

@app.route('/profile')
@login_required
def profile():
	##flash(session["username"])
	return render_template("profile.html",name=session["username"])

@app.route('/leaderboards')
@login_required
def leaderboards():
	return render_template("leaderboards.html", runs = api.get_leaderboards())

@app.route('/regclicks')
def reg_clicks():
	db = sqlite3.connect("database.db")
	c = db.cursor()

	username = session['username']
	num_clicks = request.args.get('clicks')
	print(username)
	print(num_clicks)
	c.execute("UPDATE accounts SET clicks = clicks + (?) WHERE username = (?)", (num_clicks, username,))
	c.execute("UPDATE accounts SET total_clicks = total_clicks + (?) WHERE username = (?)", (num_clicks, username,))

	db.commit()
	db.close()
	return "Nothing lol"

@app.route("/api", methods=["GET"])
def pass_info():
	db = sqlite3.connect("database.db")
	c = db.cursor()

	username = session['username']
	#command = f"SELECT * FROM accounts WHERE username = {username}"
	#pull_info = c.execute(command).fetchall()[0]
	pull_info = c.execute("SELECT * FROM accounts WHERE username = (?)", (username,)).fetchall()[0]
	info_dict = {"username": pull_info[0], "click": pull_info[2]}
	db.commit()
	db.close()
	print(jsonify(info_dict))
	return jsonify(info_dict)


if __name__ == "__main__":
	app.debug = True;
	app.run();
