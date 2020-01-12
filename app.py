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
		#print("Session username: " + session['username'])
		if 'prev_url' in session:
			return redirect(session.pop("prev_url"))

		return redirect(url_for('clicker'))

	return render_template("login.html")

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
	return render_template("register.html")

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
	flash("You have successfully created your account.")
	session['username'] = username
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
	username = session['username']
	persecond = db_ops.calc_persecond(username)

	return render_template("clicker.html", title = "Cookie Clicker", persecond = persecond)

@app.route('/profile')
@login_required
def profile():
	username = session['username']
	cookies = db_ops.get_clicks(username) # a tuple, index 0 is cookies, index 1 is total_cookies
	trials = db_ops.get_trial_data(username) #same here

	return render_template("profile.html",
		name = username, cookies = cookies[0], total_cookies = cookies[1],
		trial_15_sec = trials[0], trial_30_sec = trials[1])

@app.route('/leaderboards')
@login_required
def leaderboards():
	leaderboards = db_ops.get_leaderboards()
	leaderboard_15_sec = leaderboards[0]
	leaderboard_30_sec = leaderboards[1]
	return render_template("leaderboards.html", leaderboard_15_sec = leaderboard_15_sec,
							leaderboard_30_sec = leaderboard_30_sec, runs = api.get_leaderboards())

@app.route('/trial')
@login_required
def trial():
	return render_template("trial.html")

@app.route('/help')
def help():
	return render_template('help.html')

# JS related routes ============================================================
@app.route('/regclicks')
def reg_clicks():
	username = session['username']
	num_clicks = request.args.get('clicks')
	db_ops.reg_clicks(username, num_clicks)
	return "I just need something here to get rid of that internal server error in the console."

@app.route('/shop')
def shop():
	username = session['username']
	perk_id = request.args.get('id')
	print("Perk ID selected: " + perk_id)
	db_ops.buy_perk(username, perk_id)
	return "Same here."

@app.route("/api")
def pass_info():
	db = sqlite3.connect("database.db")
	c = db.cursor()

	username = session['username']
	pull_info = c.execute("SELECT * FROM accounts WHERE username = (?)", (username,)).fetchall()[0]
	info_dict = {"username": pull_info[0], "click": pull_info[2], "perk_0_lvl": pull_info[4], "perk_1_lvl": pull_info[5]}

	db.commit()
	db.close()
	#print(jsonify(info_dict))
	return jsonify(info_dict)

@app.route("/api/perks/<perk_id>")
def pass_task_info(perk_id):
	db = sqlite3.connect("database.db")
	c = db.cursor()

	pull_info = c.execute("SELECT * FROM perks WHERE id = (?)", (perk_id,)).fetchall()[0]
	info_dict = {"name": pull_info[1], "description": pull_info[2], "cost": pull_info[3]}

	db.commit()
	db.close()
	print(jsonify(info_dict))
	return jsonify(info_dict)


@app.route('/recordtrial')
def record_trial():
	username = session['username']
	trial_type = request.args.get('trial_type')
	num_clicks = request.args.get('clicks')

	if (trial_type == "15"):
		db_ops.record_trial(username, "trial_15_sec", num_clicks)
	if (trial_type == "30"):
		db_ops.record_trial(username, "trial_30_sec", num_clicks)

	return "Blah blah blah"

if __name__ == "__main__":
	app.debug = True;
	app.run();
