#coding=utf-8
"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, request,g
from DB_Project import app
from sqlalchemy import Column, String, create_engine
import cx_Oracle
import json
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app.secret_key = 'Your Key'
login_manager = LoginManager(app)
class User(UserMixin):
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    

@login_manager.user_loader  
def user_loader(user_id):

    if user_id is None:
        return None

    user = User()  
    user.id = user_id  
    return user

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/home')
def home():
     return render_template(
        'index.html',
        title='中山國際轉運站',
        year=datetime.now().year,
    )

@app.route('/memberCenter',methods=['GET', 'POST'])
def member():
    if request.method == 'POST': 
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
        sql = "SELECT 1 FROM TB_USER WHERE user_id = '{username}' AND u_passwd = '{password}'".format(
             username = request.form['username'],
             password = request.form['password']
            )
        result = conn.execute(sql)

       
        if result.fetchone() is None:  
            conn.close()
            return render_template('login.html')
        else:
        #  實作User類別  
            user = User()  
        #  設置id  
            user.id = request.form['username']  
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。  
            login_user(user)  
        #  登入成功，轉址  
            conn.close()
            return render_template('index.html')
    if g.user is not None :
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/registered',methods=['GET', 'POST'])
def registered():
    if request.method == 'POST': 
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
        sql = "INSERT INTO GROUP7.TB_USER (USER_ID, U_EMAIL, U_PASSWD, U_NAME, U_ADDRESS, U_TEL, U_PERMISSION) VALUES ('{USER_ID}', '{U_EMAIL}', '{U_PASSWD}', '{U_NAME}', '{U_ADDRESS}', '{U_TEL}', '{U_PERMISSION}')".format(
             USER_ID = request.form['account'],
             U_EMAIL = request.form['email'],
             U_PASSWD = request.form['password'],
             U_NAME = request.form['username'],
             U_ADDRESS = request.form['address'],
             U_TEL = request.form['tel'],
             U_PERMISSION = request.form['permission']
            )
        result = conn.execute(sql)

        conn.close()     
        return render_template('login.html')


    return render_template('registered.html')

@app.route('/overseasare',methods=['GET', 'POST'])
def overseasare():

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
    sql = "SELECT U_NAME FROM TB_USER WHERE user_id = '{username}'".format(
             username = g.user.id
            )
    sql2 = "SELECT W_COUNTRY,W_ADDRESS,W_TEL,W_EMAIL FROM TB_OVERSEAS_WAREHOUSE"
    result = conn.execute(sql)

    USER_NAME = result.fetchone()[0]
    result2 = conn.execute(sql2).fetchall()

    for row in result2:
        print(row)

    conn.close()     
    return render_template('overseasarehouse.html',
                           UserName = USER_NAME,
                           HOUSE = result2 )