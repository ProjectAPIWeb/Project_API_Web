<<<<<<< HEAD
import requests

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/479101/information"

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "f73997d380mshee76f75bdc3642ap12d0b8jsna5c16ec05bbf"
    }

response = requests.request("GET", url, headers=headers)

for i in response.json() :
    print(i)
    for j in i :
        print('\t',j)
=======
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
>>>>>>> 8a60e7c5c30edea37db82cf19c3bb536f7e65dfb
