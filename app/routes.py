#!/usr/bin/python

from app import application
from flask import render_template, request

@application.route('/test')
def testpage():
    return render_template('test_page.html')

@application.route('/')
def homepage():
    return render_template('homepage.html')

@application.route('/customer/login')
def customer_login():
    return render_template('customer_login.html')

@application.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    error = None
    if request.method == 'POST':
        last_name        = request.form['last_name']
        first_name       = request.form['first_name']
        birth_year       = request.form['birth_year']
        email            = request.form['email']
        password         = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('customer_register.html', error='Не удалось подтвердить пароль')


    return render_template('customer_register.html')
