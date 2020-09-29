from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home() :
    return render_template('index.html')

@app.route('/login')
def login() :
    return render_template('login.html')

@app.route('/profile')
def profile() :
    return render_template('profile.html')

@app.route('/register')
def register() :
    return render_template('register.html')

if __name__ == "__main__" :
    app.run(debug=True)