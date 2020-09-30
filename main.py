from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() :
    