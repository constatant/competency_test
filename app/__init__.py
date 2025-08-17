#!/usr/bin/python

from flask import Flask
from app.config import CURRENT_CONFIG
from flaskext.mysql import MySQL

application = Flask(__name__)

application.secret_key = CURRENT_CONFIG['secret_key']
application.config['MYSQL_DATABASE_HOST']       = CURRENT_CONFIG['host']
application.config['MYSQL_DATABASE_USER']       = CURRENT_CONFIG['user']
application.config['MYSQL_DATABASE_PASSWORD']   = CURRENT_CONFIG['password']
application.config['MYSQL_DATABASE_DB']         = CURRENT_CONFIG['db']

mysql = MySQL()
mysql.init_app(application)

