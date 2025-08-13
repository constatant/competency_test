#!/usr/bin/python

from app import application
from flask import render_template
from flaskext.mysql import MySQL

mysql = MySQL()

@application.route('/test')
def testpage():
    return render_template('test_page.html')

@application.route('/')
def homepage():
    return render_template('homepage.html')

@application.route('/customer/login')
def customer_login():
    return render_template('customer_login.html')