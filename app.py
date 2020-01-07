from flask import *
import os #for generating a secret key
import urllib.request
import json

app = Flask(__name__)

@app.route('/')
def home():
	return "Hello World!"

@app.route('/clicker')
def clicker():
	return render_template("clicker.html")

if __name__ == "__main__":
	app.debug = True;
	app.run();
