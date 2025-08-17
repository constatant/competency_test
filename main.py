#!/usr/bin/python

from app import application
from app import routes

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)