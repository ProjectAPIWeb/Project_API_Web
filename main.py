from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import requests
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:ECZcnl63136@node4707-env-0491803.th.app.ruk-com.cloud:11031/WebDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model) :
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

@app.route('/', methods=['GET', 'POST'])
def index() :
    url = "http://api-5496804.th.app.ruk-com.cloud/product"
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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        id = len(User.query.all()) + 1
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = User(id=id, name=name, email=email, password=password)
        Check = db.session.query(User).filter_by(name=name).first()
        if name == Check.name :
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            db.session.add(account)
            db.session.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login() : 
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        name = request.form['username']
        password = request.form['password']

        account = db.session.query(User).filter_by(name=name).first()

        if account :
            if name == account.name and password == account.password :
                msg = "Login Successfully"
                return render_template('index.html', msg=msg)
            else :
                msg = 'Incorrect username/password!' 
        else :
            msg = 'Incorrect username/password!'  

    return render_template('login.html', msg=msg)

@app.route('/contact', methods=['GET', 'POST'])
def contact() :
    return render_template('contact.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu() :
    url = "http://api-5496804.th.app.ruk-com.cloud/product"
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

@app.route('/cart', methods=["GET", "POST"])
def Cart() :
    return render_template('cart.html')

if __name__ == '__main__' :
    app.run(debug=True, host='127.0.0.2')

'''a = []
    b = []
    c = []
    for i in result :
        if 1 <= i['id'] <= 24 :
            a.append(i)
        if 25 <= i['id'] <= 48 :
            b.append(i)
        if 49 <= i['id'] <= 72 :
            c.append(i)


    return render_template('menu.html', a=a, b=b, c=c)'''