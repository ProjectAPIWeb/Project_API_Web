# ส่วนของการ import

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
import uuid
import requests
from datetime import datetime
import re

# ส่วนของการตั้งค่าเชื่อมต่อ Database

app = Flask(__name__)
app.secret_key = 'Mac126218'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:IKVtfl61980@node4912-env-3420079.th.app.ruk-com.cloud:5432/WebDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ส่วนของการตั้งค่า table

class User(db.Model) :
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)

class Contact(db.Model) :
    __tablename__ = "Contact"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    msg = Column(String)

class Order(db.Model) :
    __tablename__ = 'Order'
    id = Column(String(35), primary_key=True, unique=True)
    id_user = Column(Integer)
    time = Column(Integer)
    address = Column(String)
    date = Column(String)
    Type = Column(Integer)

class PreOrder(db.Model) :
    __tablename__ = 'PreOrder'
    id = Column(String(35), primary_key=True)
    id_user = Column(Integer)
    product = Column(String(100))
    price = Column(Integer)
    qty = Column(Integer)
    time = Column(Integer)

# หน้า main

@app.route('/index', methods=['GET', 'POST'])
def index() :
    if 'logged_in' in session : # ตรวจสอบว่า login หรือยัง

        # ดึง API

        url = "http://api-7720715.th.app.ruk-com.cloud/product"
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
        
# Run html file

        return render_template('index.html', a=a , b=b ,c=c)
    else :

# เรียกฟังชัน login

        return redirect(url_for("login"))

# หน้า home 

@app.route('/home',methods=["GET", "POST"])
def home(text):
    if 'logged_in' in session : # ตรวจสอบว่า login หรือยัง
        return render_template('home.html', text=text) # Run html file
    else :
        return redirect(url_for('login')) # เรียกฟังชัน login

# หน้า register

@app.route('/register', methods=['GET', 'POST'])
def register() :
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : # ตรวจสอบค่าที่ได้รับมา
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
            db.session.add(account)                         # Add ข้อมูลเข้า Table
            db.session.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':  
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)  # Run html file

@app.route('/admin', methods=['GET', 'POST'])
def admin() :
    if session['logged_in'] == True : # ตรวจสอบว่า login หรือยัง
        if session['name'] == 'Admin' :   # เช็คคนที่เข้าใช้ page staff
            U = db.session.query(User).all()
            Username = []
            for i in U :
                for j in db.session.query(Order).filter_by(id_user=i.id).all() :
                    if j.Type < 4 :
                        if j.Type == 1 :
                            Type = "In Queue"
                        elif j.Type == 2 :
                            Type = "On Cooking"
                        elif j.Type == 3 :
                            Type = "On Delivery"
                    Value = {'Name' : i.name, "ID Order" : j.id, "Date": j.date, "Type" : Type}
                    Username.append(Value)
            if request.method == 'POST' : # ตรวจสอบค่าที่ได้รับมา
                if request.form.get("Type") : 
                    O = db.session.query(Order).filter_by(id=request.form.get('ID')).first()
                    if 5 > int(request.form.get("Type")) > 0 :
                        O.Type = int(request.form.get("Type")) # Update ข้อมูลเข้า Table
                        db.session.commit()
                        return redirect(url_for('admin')) # เรียกฟังชัน admin
                    else :
                        msg = "Error Input"
                        return render_template('admin.html', L=Value, msg=msg) # Run html file
                if request.form.get("Search") :
                    return detail(request.form.get("Search")) 
            if Value == [] :
                return render_template('admin.html', L=Username, msg="No Order Now") # Run html file
            msg = ''
            return render_template('admin.html', L=Username) # Run html file

        else :
            text = "Staff Only"
            return home(text) # เรียกฟังชัน home
    else :
        return redirect(url_for('login'))  # เรียกฟังชัน login

# หน้า login

@app.route('/', methods=['GET', 'POST'])
def login() : 
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form : # ตรวจสอบค่าที่ได้รับมา
        name = request.form['username']
        password = request.form['password']
        account = db.session.query(User).filter_by(name=name).first()
        if account : # ตรวจสอบค่าที่ได้รับมาว่ามีอยู่ใน table ไหม
            if name == account.name and password == account.password : # ตรวจสอบ username และ password
                # กำหนดค่า session ต่างๆ
                session['logged_in'] = True
                session['id'] = account.id
                session['name'] = account.name
                session["password"] = account.password
                session["email"] = account.email
                session["phone"] = account.phone
                Pre_Order = db.session.query(PreOrder).filter_by(id_user=session['id']).all()
                Order_Time = db.session.query(Order).filter_by(id_user=session['id']).all()
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
                return home(text) # เรียกฟังชัน home
            else :
                msg = 'Incorrect username/password!' 
        else :
            msg = 'Incorrect username/password!'  

    return render_template('login.html', msg=msg) # Run html file

# หน้า contact

@app.route('/contact', methods=['GET', 'POST'])
def contact() :
    if 'logged_in' in session : # ตรวจสอบว่า login หรือยัง
        if request.method == "POST" and "First" in request.form and "Last" in request.form and "Email" in request.form and "Phone" in request.form and "msg" in request.form : # ตรวจสอบค่าที่ได้รับมา
            id = len(Contact.query.all()) + 1
            comment = Contact(id=id, name=request.form.get('First') + request.form.get('Last'), email=request.form.get('Email'), phone=request.form.get("Phone"), msg=request.form.get("msg"))
            db.session.add(comment) # Add ข้อมูลเข้า Table
            db.session.commit()

        return render_template('contact.html')   # Run html file
    else :
        return redirect(url_for("login")) # เรียกฟังชัน login

# หน้า Menu

@app.route('/menu', methods=['GET', 'POST'])
def menu() :
    if 'logged_in' in session : # ตรวจสอบว่า login หรือยัง
        # ดึงค่า API
        url = "http://api-7720715.th.app.ruk-com.cloud/product"
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
        if request.method == "POST" : # ตรวจสอบค่าที่ได้รับมา
            if request.form.get("cart") : # Add menu ที่เราเลือกลง cart
                # กำหนดค่าต่างๆ
                id = uuid.uuid4().hex
                product = str(request.form.get("cart")).split(',')
                Pre_Order = db.session.query(PreOrder).filter_by(id_user=session['id']).all()
                Order_Time = db.session.query(Order).filter_by(id_user=session['id']).all()
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
                    pre_order = PreOrder(id=id, id_user=session['id'], product=product[0], price=float(product[1]),qty=1,time=session['time'])
                    db.session.add(pre_order) # Add ค่าลง table
                    db.session.commit()
                else :
                    for i in Pre_Order :
                        if product[0] == i.product and i.time == session['time']:
                            i.qty = i.qty + 1 # Update ค่า จำนวนสินค้าขึ้น table
                            db.session.commit()

        return render_template('menu.html', a=a, b=b, c=c) # Run html file
    else :
        return redirect(url_for('login'))  # เรียกฟังชัน login

# หน้า detail

@app.route('/detail', methods=['GET', "POST"])
def detail(ID) :
# ดึงค่า detail order จาก table เพื่อนำมาแสดง
    Order_User = db.session.query(Order).filter_by(id=ID).first()
    Pre_Order = db.session.query(PreOrder).filter_by(id_user=Order_User.id_user,time=Order_User.time).all()
    product = []
    for i in Pre_Order :
        value = {'name' : i.product, 'qty' : i.qty, 'price' : i.price}
        product.append(value)
    return render_template('detail.html', a=product, ID=ID) # Run html file


# หน้าเปลี่ยน ชื่อ

@app.route('/edit_name', methods=["GET", "POST"])
def edit_name() :
    msg = ''
    if request.method == 'POST' and 'username' in request.form :  # ตรวจสอบค่าที่ได้รับมา
        username = request.form.get('username')
        account = db.session.query(User).filter_by(name=username).first()
        if account is not None :  # ตรวจสอบว่ามีชื่อที่อยู่ในระบบไหม
            msg = 'This name is use already'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else : 
            df = db.session.query(User).filter_by(id=session['id']).first()
            session['name'] = username # Update ค่า name
            df.name = username
            db.session.commit()
            return redirect(url_for('profile')) # เรียกฟังชัน profile
    return render_template('edit_name.html',msg=msg)  # Run html file

# หน้าเปลี่ยน email

@app.route('/edit_email', methods=["GET", "POST"])
def edit_email() :
    msg = ''
    if request.method == 'POST' and 'email' in request.form : # ตรวจสอบค่าที่ได้รับมา
        email = request.form.get('email')
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email) : # ตรวจสอบว่าเป็น email ไหม
            msg = 'Invalid email address!'
        else : 
            df = db.session.query(User).filter_by(id=session['id']).first()
            session['email'] = email # Update ค่า email
            df.email = email
            db.session.commit()
            return redirect(url_for('profile'))  # เรียกฟังชัน profile
    return render_template('edit_email.html',msg=msg)  # Run html file

# หน้าเปลี่ยนเบอร์

@app.route('/edit_phone', methods=["GET", "POST"])
def edit_phone() :
    msg = ''
    if request.method == 'POST' and 'phone' in request.form : # ตรวจสอบค่าที่ได้รับมา
        phone= request.form.get('phone')
        if not re.match(r'[0-9]+', phone) : # ตรวจสอบว่าเป็นเบอร์ไหม
            msg = 'Phone number must only number'
        else : 
            df = db.session.query(User).filter_by(id=session['id']).first()
            session['phone'] = phone  # Update ค่า Phone
            df.phone = phone
            db.session.commit()
            return redirect(url_for('profile')) # เรียกฟังชัน profile
    return render_template('edit_phone.html',msg=msg) # Run html file
 
# เปลี่ยน Password

@app.route('/edit_password', methods=["GET", "POST"])
def edit_password() :
    msg = ''
    if request.method == 'POST' and 'newpassword' in request.form and 'oldpassword'in request.form and 'confirmpassword' in request.form : # ตรวจสอบค่าที่ได้รับมา
        new = request.form.get('newpassword')
        confirm = request.form.get('confirmpassword')
        old = request.form.get('oldpassword')
        if new != confirm :  # ตรวจสอบค่าnew password กับ confirm
            msg = 'Password Not Match'
        else : 
            df = db.session.query(User).filter_by(id=session['id']).first()
            if old == df.password : # ตรวจpassword ว่าถูกไหม
                session['password'] = new  # Update ค่า Password
                df.password = new
                db.session.commit()
                return redirect(url_for('profile')) # เรียกฟังชัน profile
            else :
                msg = 'Old Password Not Correct'
    return render_template('edit_password.html', msg=msg) # Run html file

# หน้า Profile

@app.route('/profile', methods=["GET", "POST"])
def profile() :
    if 'logged_in' in session : # ตรวจสอบว่า login หรือยัง
        ID = request.form.get("Order_id")
        Time = db.session.query(Order).filter_by(id=ID).first()
        if request.method == "POST" :   # ตรวจสอบค่าที่ได้รับมา
            if 'Order_id' in request.form :
                if Time.time == 1 : # Cancel Order
                    db.session.query(PreOrder).filter_by(id_user=session['id'], time=Time.time).delete()
                    db.session.query(Order).filter_by(id=ID).delete()
                    db.session.commit() 
                    text = "Cancel Order Success"
                    return home(text)
                else :
                    text = "Cancel This Order"
                    return home(text)
            if request.form.get("Detail") :
                return detail(request.form.get("Detail")) 
        
        # เรียกค่า account เพื่อไปแสดงใน profile

        account = {"name" : session["name"], "password" : session["password"], "email" : session["email"], 'phone' : session['phone']}
        User_Order = db.session.query(Order).filter_by(id_user=session['id']).all()
        User_Order_Name = db.session.query(PreOrder).filter_by(id_user=session['id']).all()
        id_order = []

        # เรียกค่า order เพื่อไปแสดงใน profile

        for i in User_Order : 
            User_Order_Name = db.session.query(PreOrder).filter_by(id_user=session['id'], time=i.time).all()
            num = 0
            p = 0
            for j in User_Order_Name : 
                if j.time == i.time :
                    num += j.qty
                    p += j.price
            if i.Type == 1 :
                Type = "In Queue"
            elif i.Type == 2 :
                Type = "On Cooking"
            elif i.Type == 3 :
                Type = "On Delivery"
            elif i.Type == 4 :
                Type = "Success"
            value = {"ID" : i.id, "Address" : i.address, "Order" : num, 'Price' : p , "Date" : i.date, "Type" : Type}
            id_order.append(value)
        if id_order == [] :
            text = 'No Order'
            return render_template("profile.html", account=account, id=id_order, text=text) # Run html file
        else :
            return render_template("profile.html", account=account, id=id_order, text='') # Run html file
    else :
        return redirect(url_for("login")) # เรียกฟังชัน login

# หน้า Cart

@app.route('/cart', methods=["GET", "POST"])
def Cart() :
    if 'logged_in' in session : # ตรวจสอบว่า login หรือยัง
        Pre_Order = db.session.query(PreOrder).filter_by(id_user=session['id']).all()
        P = [] 
        product_name = []
        for i in Pre_Order :
            P.append(int(i.time))
        if P == [] or session['time'] not in P : # ตรวจสอบว่ามีค่าอยู่ใน cart ไหม
            text = "Please Should Your Order First"
            return home(text) # เรียกฟังชัน home
        else :

# ดึงค่า Pre Order เพื่อไปแสดง

            for i in Pre_Order :
                if i.product not in product_name and i.time == session['time']  :
                    value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                    product_name.append(value)
                if request.method == "POST" : # ตรวจสอบค่าที่ได้รับมา
                    if session['logged_in'] is True :
                        if request.form.get("Order") :
                            return redirect(url_for('New'))
                        if request.form.get("Remove") : # ลบออก
                            for i in Pre_Order :
                                if i.product == request.form.get("Remove") :
                                    db.session.query(PreOrder).filter_by(id=i.id).delete()
                                    db.session.commit()
                                    return redirect(url_for('Cart'))
                        if request.form.get("Add") : # เพิ่มจำนวน
                            for i in Pre_Order :
                                if i.product == request.form.get("Add") and i.time == session["time"] :
                                    if int(request.form.get('qty')) > 0 :
                                        i.qty = request.form.get('qty')
                                        db.session.commit()
                                    else :
                                        i.qty = 1
                                        db.session.commit()
                            return redirect(url_for("Cart"))
        
        return render_template('cart.html', a=product_name) # Run html file
    else :
        return redirect(url_for("login")) # เรียกฟังชัน login

# หน้า Total

@app.route('/New', methods=['GET', 'POST'])
def New() :
    if 'logged_in' in session : # ตรวจสอบว่า login หรือยัง
        Pre_Order = db.session.query(PreOrder).filter_by(id_user=session['id']).all()
        product_name = []
        price = 0
        Cart = 0

# ดึงค่า Pre Order ออกมา

        for i in Pre_Order:
            if i.product not in product_name  and i.time == session['time'] :
                print(i.product)
                value = {"product" : i.product, "price" : i.price, "qty" : i.qty}
                product_name.append(value)
                price += (i.price * i.qty)
                i.price = i.price * i.qty
                Cart += i.qty
        if request.method == "POST" : # ตรวจสอบค่าที่ได้รับมา
            if request.form.get("Order") :
                ad = request.form.get('address') + ',' + request.form.get('city')
                text = "Thank for your order"
                date = datetime.now()
                Date = str(date.date()) + ' ' + date.strftime("%X")
                Order_Total = Order(id=uuid.uuid4().hex, id_user=session["id"],time=session['time'], address=ad ,date=Date, Type=1)
                session["time"] = None
                db.session.add(Order_Total) # Add Order ลง ใน table
                db.session.commit()
                return home(text) # เรียกฟังชัน home

        return render_template('New.html', a=product_name, b=price, c=Cart) # Run html file
    else :
        return redirect(url_for('login')) # เรียกฟังชัน login
#  หน้า logout

@app.route('/logout')
def logout():
    if 'logged_in' in session : # ตรวจสอบว่า login ไหม เพิ่ม logout
        session.pop('logged_in', None) # นำค่าออกจาก session
        session.pop('id', None) 
        session.pop('name', None)
        return redirect(url_for('login'))   # เรียกฟังชัน login
    else :
        return redirect(url_for('login'))   # เรียกฟังชัน login

# set ค่า run        
if __name__ == '__main__' :
    app.run(debug=True, host='0.0.0.0', port=80)

