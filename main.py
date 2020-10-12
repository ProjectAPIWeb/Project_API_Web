from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import requests
import re

app = Flask(__name__)

app.secret_key = 'Mac126218'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'INE@2562'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index() :
    url = "http://127.0.0.1:5000/product"
    response = requests.request("GET", url)
    result = response.json()
    a = []
    b = []
    c = []
    for i in result :
        if 1 <= i['id'] <= 6 :
            a.append(i)
        if 25 <= i['id'] <= 32 :
            b.append(i)
        if 49 <= i['id'] <= 55 :
            c.append(i)
    return render_template('index.html', a=a , b=b ,c=c)

@app.route('/register', methods=['GET', 'POST'])
def register() :
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM useraccounts WHERE username = %s AND password = %s', (username, password))

        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:

            cursor.execute('INSERT INTO useraccounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login() :
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM useraccounts WHERE username = %s AND password = %s', (username, password))

        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = "Successfully"
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username/password!'     
            
    return render_template('login.html', msg=msg)

@app.route('/about', methods=['GET', 'POST'])
def about() :
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact() :
    return render_template('contact.html')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery() :
    return render_template('gallery.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu() :
    url = "http://127.0.0.1:5000/product"
    response = requests.request("GET", url)
    result = response.json()
    a = []
    b = []
    c = []
    for i in result :
        if 1 <= i['id'] <= 24 :
            a.append(i)
        if 25 <= i['id'] <= 48 :
            b.append(i)
        if 49 <= i['id'] <= 72 :
            c.append(i)

        
    return render_template('menu.html', a=a, b=b, c=c)

@app.route('/recipe', methods=['GET', 'POST'])
def recipe() :
    return render_template('recipe.html')

@app.route('/service', methods=['GET', 'POST'])
def service() :
    return render_template('service.html')

if __name__ == '__main__' :
    app.run(debug=True, host='127.0.0.2')