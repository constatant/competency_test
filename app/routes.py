#!/usr/bin/python

from app import application, mysql
from flask import render_template, request, redirect, url_for, session

@application.route('/test')
def testpage():
    return render_template('test_page.html')

@application.route('/')
def homepage():
    return render_template('homepage.html')

@application.route('/customer/login')
def customer_login():
    return render_template('customer_login.html')


@application.route('/api/auth/login', methods=['POST'])
def customer_login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, password FROM customers WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and user[1] == password:
        session['user_id'] = user[0]
        return redirect(url_for('customer_profile'))

    return render_template('customer_login.html', error='Неверный логин или пароль')

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


@application.route('/customer/profile')
def customer_profile():
    if 'user_id' not in session:
        return redirect(url_for('customer_login'))
    return render_template('customer_profile.html')
