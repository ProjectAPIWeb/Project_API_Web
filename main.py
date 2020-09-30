from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() :
    return render_template('/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login() :
    return render_template('/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register() :
    return render_template('/register.html')

@app.route('/account', methods=['GET', 'POST'])
def account() :
    return render_template('/account.html')

@app.route('/about', methods=['GET', 'POST'])
def about() :
    return render_template('/about.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout() :
    return render_template('/checkout.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact() :
    return render_template('/contact.html')

@app.route('/events', methods=['GET', 'POST'])
def events() :
    return render_template('/events.html')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery() :
    return render_template('/gallery.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu() :
    return render_template('/menu.html')

if __name__ == '__main__' :
    app.run(debug=True)