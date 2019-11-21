from flask import Flask, session, redirect, url_for, request, render_template
from flask import send_from_directory, send_file

app = Flask(__name__)
app.secret_key = "secret_key_string"

@app.route('/')
def index():
	return "Hello!"

app.run('0.0.0.0')
