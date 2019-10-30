"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DB_Project import app
from sqlalchemy import Column, String, create_engine
import cx_Oracle

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    host='140.117.69.58'
    port='1521'
    sid='ORCL'
    user='Group7'
    password='group77'
    sid = cx_Oracle.makedsn(host, port, sid=sid)

    cstr = 'oracle://{user}:{password}@{sid}'.format(
        user=user,
        password=password,
        sid=sid
    )

    engine =  create_engine(
        cstr,
        convert_unicode=False,
        pool_recycle=10,
        pool_size=50,
        echo=True
    )
    
    conn = engine.connect()
    query_one_query = 'SELECT TEST_1 FROM TEST_1'
    result = conn.execute(query_one_query)
    for item in result:
        print(item)
    conn.close()

    return render_template(
        'index.html',
        title=result,
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
