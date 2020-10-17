from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
import uuid
import requests
import re

app = Flask(__name__)
app.secret_key = 'Mac126218'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:ECZcnl63136@node4707-env-0491803.th.app.ruk-com.cloud:11031/WebDatabase'
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
    name = Column(String(100))
    time = Column(Integer)

class PreOrder(db.Model) :
    __tablename__ = 'PreOrder'
    id = Column(String(35), primary_key=True)
    name_user = Column(String(100))
    product = Column(String(100))
    price = Column(Integer)
    qty = Column(Integer)
    time = Column(Integer)

@app.route('/index', methods=['GET', 'POST'])
def index() :
    if 'logged_in' in session :
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
    else :
        return redirect(url_for("login"))

@app.route('/home',methods=["GET", "POST"])
def home(text):
    if 'logged_in' in session :
        return render_template('home.html', text=text)
    else :
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

@app.route('/', methods=['GET', 'POST'])
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
                text = f"Welcome Back {session['name']}"
                return home(text)
            else :
                msg = 'Incorrect username/password!' 
        else :
            msg = 'Incorrect username/password!'  

    return render_template('login.html', msg=msg)

@app.route('/contact', methods=['GET', 'POST'])
def contact() :
    if 'logged_in' in session :
        return render_template('contact.html')
    else :
        return redirect(url_for("login"))

@app.route('/menu', methods=['GET', 'POST'])
def menu() :
    if 'logged_in' in session :
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
                    id = uuid.uuid4().hex
                    name_user = session['name']
                    product = str(request.form.get("cart")).split(',')
                    Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
                    Order_Time = db.session.query(Order).filter_by(name=session['name']).all()
                    P = []
                    T = []
                    for j in Order_Time :
                        T.append(int(j.time))
                    if T == [] :
                        session['time'] = 1
                    if T != [] :
                        session['time'] = max(T) + 1
                    for i in Pre_Order :
                        if i.time == session['time'] :
                            P.append(i.product)
                    if product[0] not in P :
                        pre_order = PreOrder(id=id, name_user=name_user, product=product[0], price=float(product[1]),qty=1,time=session['time'])
                        db.session.add(pre_order)
                        db.session.commit()
                    else :
                        for i in Pre_Order :
                            if product[0] == i.product and i.time == session['time']:
                                i.qty = i.qty + 1
                                db.session.commit()
            else :
                Top = "Hi"
                msg = 'Please Login First'
                return render_template('menu.html', a=a, b=b, c=c, msg=msg, Top=Top)
        return render_template('menu.html', a=a, b=b, c=c)
    else :
        return redirect(url_for('login'))

@app.route('/cart', methods=["GET", "POST"])
def Cart() :
    if 'logged_in' in session :
        Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
        product_name = []
        
        for i in Pre_Order :
            if i.product not in product_name and i.time == session['time']  :
                value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                product_name.append(value)
        if session["time"] != 0 :
            print(session['time'])
            if request.method == "POST" :
                if session['logged_in'] is True :
                    if request.form.get("Order") :
                        return redirect(url_for('total'))
                    if request.form.get("Remove") :
                        for i in Pre_Order :
                            if i.product == request.form.get("Remove") :
                                db.session.query(PreOrder).filter_by(id=i.id).delete()
                                db.session.commit()
                    if request.form.get("Add") :
                        for i in Pre_Order :
                            if i.product == request.form.get("Add") and i.time == session["time"] :
                                if int(request.form.get('qty')) > 0 :
                                    i.qty = request.form.get('qty')
                                    print(i.qty)
                                    db.session.commit()
                                else :
                                    i.qty = 1
                                    db.session.commit()
            
        return render_template('cart.html', a=product_name)
    else :
        return redirect(url_for("login"))
@app.route('/total', methods=['GET', 'POST'])
def total() :
    if 'logged_in' in session :
        Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
        product_name = []
        price = 0
        Cart = 0
        for i in Pre_Order:
            if i.product not in product_name  :
                print(i.product)
                value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                product_name.append(value)
                price += (i.price * i.qty)
                Cart += i.qty
        if request.method == "POST" :
            if request.form.get("Order") :
                text = "Thank for your order"
                Order_Total = Order(id=uuid.uuid4().hex, name=session["name"],time=session['time'])
                session["time"] = None
                db.session.add(Order_Total)
                db.session.commit()
                return home(text)
            

        return render_template('total.html', a=product_name, b=price, c=Cart)
    else :
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'logged_in' in session :
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('name', None)
        return redirect(url_for('login'))
    else :
        return redirect(url_for('login'))

if __name__ == '__main__' :
    app.run(debug=True)

