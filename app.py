from flask import *
import os #for generating a secret key
import urllib.request
import json

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
	if 'user' in session:
		print("Session username: " + session['user'])
		flash("You are logged in.")
		return render_template("clicker.html")

	return render_template("login.html", title = "Login")

@app.route('/login', methods=['POST'])
def login():
	username = request.form.get('user')
	password = request.form.get('pw')

@app.route("/register")
def register():
	username = request.form.get('user')
	password = request.form.get('pw')

if __name__ == "__main__":
	app.debug = True;
	app.run();
