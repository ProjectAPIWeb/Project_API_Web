from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
import uuid
import requests
import re

app = Flask(__name__)
app.secret_key = 'Mac126218'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:ECZcnl63136@node4707-env-0491803.th.app.ruk-com.cloud:5432/WebDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model) :
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

class Order(db.Model) :
    __tablename__ = 'Order'
    id = Column(String(35), primary_key=True, unique=True)
    product = Column(String(100))
    id_user = Column(Integer, ForeignKey('User.id'))
    quantity = Column(Integer)

    def __init__ (self, order=None, product=None, quantity=None) :
        self.id = uuid.uuid4().hex
        self.id_user = id_user
        self.product = product
        self.quantity = quantity
    
    def __repr__(self):
        return '<Order_Product {}>'.format(self.id_user + " "+ self.product)


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

@app.route('/home')
def home():
    if 'logged_in' in session:
        return render_template('home.html', username=session['name'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register() :
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        id = len(User.query.all()) + 1
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = User(id=id, name=username, email=email, password=password)
        Check = db.session.query(User).filter_by(name=username).first()
        if Check is not None:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
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
                session['logged_in'] = True
                session['id'] = account.id
                session['name'] = account.name
                return redirect(url_for('home'))
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
    if request.method == "POST" :
        if session['logged_in'] is True :
            if request.form.get("cart") :
                print(request.form.get("cart"))
                print(session['id'])
        else :
            Top = "Hi"
            msg = 'Please Login First'
            return render_template('menu.html', a=a, b=b, c=c, msg=msg, Top=Top)
    return render_template('menu.html', a=a, b=b, c=c)

@app.route('/cart', methods=["GET", "POST"])
def Cart() :
    return render_template('cart.html')

@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   session.pop('id', None)
   session.pop('name', None)
   return redirect(url_for('login'))

if __name__ == '__main__' :
    app.run(debug=True)

