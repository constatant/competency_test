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

conn = mysql.connect()
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS `contests` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `title` varchar(255) NOT NULL,
                  `start_time` datetime NOT NULL,
                  `end_time` datetime NOT NULL,
                  PRIMARY KEY(`id`));''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS `customers` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `last_name` varchar(255) NOT NULL,
                  `first_name` varchar(255) NOT NULL,
                  `birth_year` int NOT NULL,
                  `email` varchar(255) NOT NULL UNIQUE,
                  `password` varchar(255) NOT NULL,
                  PRIMARY KEY(`id`));''')
conn.commit()

cursor.close()
conn.close()

from app import routes
