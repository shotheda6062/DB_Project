#!/usr/bin/python3
"""
This script runs the DB_Project application using a development server.
"""

from os import environ
from DB_Project import app
environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run('157.245.123.212', PORT)
