from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() :
    return render_template('web/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login() :
    return render_template('web/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register() :
    return render_template('web/register.html')

if __name__ == '__main__' :
    app.run(debug=True)