#!/usr/bin/python

from app import application
from flask import render_template, request, redirect, url_for
from re import match
from werkzeug.security import check_password_hash, generate_password_hash
from app import mysql

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

        hashed_password = generate_password_hash(password)
        
        if max(len(last_name),
               len(first_name),
               len(email),
               len(password)) > 255:
            return render_template('customer_register.html', error='Одно из полей содержит слишком много символов')
        
        conn   = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        found_user = cursor.fetchone()

        if found_user:
            cursor.close()
            conn.close()
            return render_template('customer_register.html', error='Пользователь с данной почтой уже существует')
        
        cursor.execute(
            "INSERT INTO users (last_name, first_name, birth_year, email, password) VALUES (%s, %s, %s, %s, %s)",
            (last_name, first_name, birth_year, email, hashed_password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('customer_login'))

    return render_template('customer_register.html')
