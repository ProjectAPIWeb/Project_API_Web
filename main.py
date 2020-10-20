from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
import uuid
import requests
import re

app = Flask(__name__)
app.secret_key = 'Mac126218'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mac126218@127.0.0.1:5432/WebDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model) :
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)

class Address(db.Model) :
    __tablename__ = "Address"
    id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)

class Order(db.Model) :
    __tablename__ = 'Order'
    id = Column(String(35), primary_key=True, unique=True)
    name = Column(String(100))
    time = Column(Integer)
    address = Column(String)

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
        url = "http://127.0.0.2:5000/"
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
        phone = request.form['tel']
        account = User(id=id, name=username, email=email, password=password, phone=phone)
        Check = db.session.query(User).filter_by(name=username).first()
        if Check is not None:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[0-9]+', phone) :
            msg = 'Phone number must only number'
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
                session["password"] = account.password
                session["email"] = account.email
                session["phone"] = account.phone
                Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
                Order_Time = db.session.query(Order).filter_by(name=session['name']).all()
                P = []
                T = []
                for i in Pre_Order :
                    P.append(int(i.time))
                for i in Order_Time :
                    T.append(int(i.time))
                if T == [] and P == [] :
                    session['time'] = 1
                if T == [] and P != [] :
                    session['time'] = max(P)
                if T != [] and P != [] :
                    if max(T) == max(P) :
                        session['time'] = max(T) + 1
                    else :
                        session['time'] = max(P)
                
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
                    O = []
                    for j in Order_Time :
                        T.append(int(j.time))
                    for i in Pre_Order :
                        O.append(int(i.time))
                    if T == [] and O == [] :
                        session['time'] = 1
                    elif O != [] and T == [] :
                        session['time'] = max(O)
                    elif O != [] and T != [] :
                        if max(O) == max(T) :
                            session['time'] = max(T) +1
                        elif max(O) > max(T) :
                            session['time'] = max(O)
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

@app.route('/profile', methods=["GET", "POST"])
def profile() :
    if 'logged_in' in session :
        ID = request.form.get("Order_id")
        Time = db.session.query(Order).filter_by(id=ID).first()
        User_Address = db.session.query(Address).filter_by(name=session['name']).first()
        if request.method == 'POST' and 'Order_id' in request.form :
            db.session.query(PreOrder).filter_by(name_user=session['name'], time=Time.time).delete()
            db.session.query(Order).filter_by(id=ID).delete()
            db.session.commit()
            text = "Cancel Order Success"
            return home(text)
        if User_Address is None or User_Address.address is None :
            address = 'Not have Address'
            account = {"name" : session["name"], "password" : session["password"], "email" : session["email"], 'phone' : session['phone']}
            User_Order = db.session.query(Order).filter_by(name=session['name']).all()
            id_order = []
            for i in User_Order :
                id_order.append(i.id)
            if id_order == [] :
                text = 'No Order'
                return render_template("profile.html", account=account, id=id_order, text=text, address=address)
            else :
                return render_template("profile.html", account=account, id=id_order, text='', address=address)
        if User_Address.address != None :
            text = ''
            account = {"name" : session["name"], "password" : session["password"], "email" : session["email"], 'phone' : session['phone']}
            User_Order = db.session.query(Order).filter_by(name=session['name']).all()
            id_order = []
            for i in User_Order :
                id_order.append(i.id)
            if id_order == [] :
                text = 'No Order'
                return render_template("profile.html", account=account, id=id_order, text=text, address=User_Address.address)
            else :
                return render_template("profile.html", account=account, id=id_order, text='', address=User_Address.address)
    else :
        return redirect(url_for("login"))

@app.route('/cart', methods=["GET", "POST"])
def Cart() :
    if 'logged_in' in session :
        Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
        P = [] 
        product_name = []
        for i in Pre_Order :
            P.append(int(i.time))
        if P == [] or session['time'] not in P :
            text = "Please Should Your Order First"
            return home(text)
        else :
            for i in Pre_Order :
                if i.product not in product_name and i.time == session['time']  :
                    value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                    product_name.append(value)
                if request.method == "POST" :
                    if session['logged_in'] is True :
                        if request.form.get("Order") :
                            return redirect(url_for('total'))
                        if request.form.get("Remove") :
                            for i in Pre_Order :
                                if i.product == request.form.get("Remove") :
                                    db.session.query(PreOrder).filter_by(id=i.id).delete()
                                    db.session.commit()
                                    return redirect(url_for('Cart'))
                        if request.form.get("Add") :
                            for i in Pre_Order :
                                if i.product == request.form.get("Add") and i.time == session["time"] :
                                    if int(request.form.get('qty')) > 0 :
                                        i.qty = request.form.get('qty')
                                        db.session.commit()
                                    else :
                                        i.qty = 1
                                        db.session.commit()
                            return redirect(url_for("Cart"))
        
        return render_template('cart.html', a=product_name)
    else :
        return redirect(url_for("login"))
@app.route('/total', methods=['GET', 'POST'])
def total() :
    if 'logged_in' in session :
        Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
        User_Address = db.session.query(Address).filter_by(name=session['name']).all()
        UA = []
        product_name = []
        price = 0
        Cart = 0
        for i in Pre_Order:
            if i.product not in product_name  and i.time == session['time'] :
                print(i.product)
                value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                product_name.append(value)
                price += (i.price * i.qty)
                Cart += i.qty
        for i in User_Address :
            UA.append(i.address)
        if UA == [] :
            if request.method == "POST" :
                if request.form.get("Order") :
                    ad = request.form.get('address') + ',' + request.form.get('city')
                    New_Address = Address(id=uuid.uuid4().hex, name=session["name"], address=ad)
                    text = "Thank for your order"
                    Order_Total = Order(id=uuid.uuid4().hex, name=session["name"],time=session['time'], address=ad)
                    session["time"] = None
                    db.session.add(Order_Total)
                    db.session.add(New_Address)
                    db.session.commit()
                    return home(text)

            return render_template('total1.html', a=product_name, b=price, c=Cart)
        else :
            return render_template('total3.html')
    else :
        return redirect(url_for('login'))

@app.route('/New', methods=['GET', 'POST'])
def New() :
    if 'logged_in' in session :
        Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
        User_Address = db.session.query(Address).filter_by(name=session['name']).all()
        UA = []
        product_name = []
        price = 0
        Cart = 0
        for i in Pre_Order:
            if i.product not in product_name  and i.time == session['time'] :
                print(i.product)
                value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                product_name.append(value)
                price += (i.price * i.qty)
                Cart += i.qty
        if request.method == "POST" :
            if request.form.get("Order") :
                ad = request.form.get('address') + ',' + request.form.get('city')
                New_Address = Address(id=uuid.uuid4().hex, name=session["name"], address=ad)
                text = "Thank for your order"
                Order_Total = Order(id=uuid.uuid4().hex, name=session["name"],time=session['time'], address=ad)
                session["time"] = None
                db.session.add(Order_Total)
                db.session.add(New_Address)
                db.session.commit()
                return home(text)

            return render_template('total1.html', a=product_name, b=price, c=Cart)
    else :
        return redirect(url_for('login'))

@app.route('/Old', methods=['GET', 'POST'])
def Old() :
    if 'logged_in' in session :
        Pre_Order = db.session.query(PreOrder).filter_by(name_user=session['name']).all()
        User_Address = db.session.query(Address).filter_by(name=session['name']).all()
        UA = []
        product_name = []
        price = 0
        Cart = 0
        for i in Pre_Order:
            if i.product not in product_name  and i.time == session['time'] :
                print(i.product)
                value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                product_name.append(value)
                price += (i.price * i.qty)
                Cart += i.qty
        if request.method == "POST" :
            if request.form.get("Order") :
                ad = request.form.get('address') + ',' + request.form.get('city')
                New_Address = Address(id=uuid.uuid4().hex, name=session["name"], address=ad)
                text = "Thank for your order"
                Order_Total = Order(id=uuid.uuid4().hex, name=session["name"],time=session['time'], address=ad)
                session["time"] = None
                db.session.add(Order_Total)
                db.session.add(New_Address)
                db.session.commit()
                return home(text)
                
            return render_template('total2.html', a=product_name, b=price, c=Cart)
    else :
        return redirect(url_for('login'))

@app.route('/total3')
def should() :
    return render_template('total3.html')

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

