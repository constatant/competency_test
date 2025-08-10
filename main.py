#!/usr/bin/python

from flask import Flask, render_template
from flaskext.mysql import MySQL
from scripts.config import CURRENT_CONFIG

application = Flask(__name__)

application.secret_key = CURRENT_CONFIG['secret_key']

application.config['MYSQL_DATABASE_HOST']       = CURRENT_CONFIG['host']
application.config['MYSQL_DATABASE_USER']       = CURRENT_CONFIG['user']
application.config['MYSQL_DATABASE_PASSWORD']   = CURRENT_CONFIG['password']
application.config['MYSQL_DATABASE_DB']         = CURRENT_CONFIG['db']

mysql = MySQL()

@application.route('/home')
def homepage():
    return render_template('homepage.html')

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)