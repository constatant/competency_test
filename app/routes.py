#!/usr/bin/python

from app import application
from flask import render_template, request, redirect, url_for, session
from re import match
from werkzeug.security import check_password_hash, generate_password_hash
from app import mysql
import uuid


def ensure_schema():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS respondents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            email VARCHAR(255),
            code VARCHAR(255),
            status VARCHAR(20) DEFAULT 'pending'
        )
        """
    )
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN report_status VARCHAR(20) DEFAULT 'pending'")
    except Exception:
        pass
    conn.commit()
    cursor.close()
    conn.close()


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
def api_auth_login():
    email    = request.form['email']
    password = request.form['password']

    conn   = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        return redirect(url_for('customer_profile'))

    return render_template('customer_login.html', error='Неверный логин или пароль')


@application.route('/api/auth/logout', methods=['POST'])
def api_auth_logout():
    """Clear the user session and redirect to the homepage."""
    session.pop('user_id', None)
    return redirect(url_for('homepage'))


@application.route('/customer/profile')
def customer_profile():
    if 'user_id' not in session:
        return redirect(url_for('customer_login'))

    ensure_schema()
    user_id = session['user_id']
    conn   = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, email, code, status FROM respondents WHERE user_id = %s", (user_id,))
    respondents = [
        {'id': r[0], 'email': r[1], 'code': r[2], 'status': r[3]}
        for r in cursor.fetchall()
    ]

    cursor.execute("SELECT report_status FROM users WHERE id = %s", (user_id,))
    report_status = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    has_completed = any(r['status'] == 'completed' for r in respondents)

    return render_template(
        'customer_profile.html',
        respondents=respondents,
        has_completed=has_completed,
        report_status=report_status,
        message=request.args.get('msg')
    )


@application.route('/api/respondents/add', methods=['POST'])
def api_respondents_add():
    if 'user_id' not in session:
        return redirect(url_for('customer_login'))

    ensure_schema()
    email = request.form['email']
    code = uuid.uuid4().hex[:8]

    conn   = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO respondents (user_id, email, code, status) VALUES (%s, %s, %s, 'pending')",
        (session['user_id'], email, code)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('customer_profile'))


@application.route('/api/respondents/send', methods=['POST'])
def api_respondents_send():
    if 'user_id' not in session:
        return redirect(url_for('customer_login'))
    # Mailing logic would be implemented here
    return redirect(url_for('customer_profile', msg='emails_sent'))


@application.route('/api/report/prepare', methods=['POST'])
def api_report_prepare():
    if 'user_id' not in session:
        return redirect(url_for('customer_login'))

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET report_status = 'prepared' WHERE id = %s", (session['user_id'],))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('customer_profile', msg='report_prepared'))


@application.route('/respondent', methods=['GET', 'POST'])
def respondent():
    ensure_schema()
    if request.method == 'POST':
        code = request.form['code']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, status FROM respondents WHERE code = %s", (code,))
        respondent = cursor.fetchone()
        cursor.close()
        conn.close()
        if respondent:
            session['respondent_id'] = respondent[0]
            if respondent[1] == 'completed':
                return render_template('respondent_test.html', completed=True)
            return render_template('respondent_test.html', completed=False)
        return render_template('respondent_code.html', error='Неверный код')
    return render_template('respondent_code.html')


@application.route('/respondent/complete', methods=['POST'])
def respondent_complete():
    respondent_id = session.get('respondent_id')
    if not respondent_id:
        return redirect(url_for('respondent'))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE respondents SET status='completed' WHERE id=%s", (respondent_id,))
    conn.commit()
    cursor.close()
    conn.close()
    session.pop('respondent_id', None)
    return render_template('respondent_test.html', completed=True)


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
