#coding=utf-8
"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, request,g,redirect,url_for,session
from DB_Project import app
from sqlalchemy import Column, String, create_engine
import cx_Oracle
import json
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user


app.config['TESTING'] = False
app.secret_key = 'Your Key'
login_manager = LoginManager(app)
login_manager.login_view = "member"
login_manager.login_message = u"请登录！"
login_manager.login_message_category = "info"

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
    user.permission = session.get('permission')
    user.username = session.get('username')
    user.userId = session.get('userId')
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

@app.route('/logout')  
def logout():  
    #logout\_user會將所有的相關session資訊給pop掉 
    logout_user()  
    return redirect(url_for('home'))

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
        sql = "SELECT U_PERMISSION,U_NAME,USER_ID FROM TB_USER WHERE U_EMAIL = '{username}' AND U_PASSWD = '{password}'".format(
             username = request.form['username'],
             password = request.form['password']
            )
        result = conn.execute(sql).fetchone()

       
        if result is None:  
            conn.close()
            return render_template('login.html')
        else:
        #  實作User類別  
            user = User()  
        #  權限判斷
            user.permission = result[0]
            user.username = result[1]
            user.userId = result[2]
            session['permission'] = result[0]
            session['username'] = result[1]
            session['userId'] = result[2]
        #  設置id  
            user.id = request.form['username']  
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。  
            login_user(user)
        #  登入成功，轉址  
            conn.close()
            return render_template('index.html')

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('overseasare'))
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
        SEQ_SQL = "UPDATE TB_COUNT_SEQ SET SEQ = (SELECT (SEQ + 1) FROM TB_COUNT_SEQ FETCH FIRST 1 ROWS ONLY)"
        conn.execute(SEQ_SQL)
        sql = "INSERT INTO GROUP7.TB_USER (USER_ID, U_EMAIL, U_PASSWD, U_NAME, U_ADDRESS, U_TEL, U_PERMISSION) VALUES ((SELECT 'U'||(LPAD(SEQ, 5, '0')) FROM TB_COUNT_SEQ FETCH FIRST 1 ROWS ONLY), '{U_EMAIL}', '{U_PASSWD}', '{U_NAME}', '{U_ADDRESS}', '{U_TEL}', '{U_PERMISSION}')".format(
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
@login_required
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
    print(g.user.userId)
    conn = engine.connect()
    sql = "SELECT U_NAME FROM TB_USER WHERE user_id = '{username}'".format(
             username = g.user.userId
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
                           UserId = g.user.userId,
                           HOUSE = result2 )


@app.route('/package_manage',methods=['GET', 'POST'])
@login_required
def package_manage():
    if request.method == 'GET': 
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
        
        
        sql = "SELECT P_ID, P_DATE_DECLARATION, P_DATE_IN, P_DATE_OUT, W_COUNTRY, P_STATUS_CODE FROM TB_PACKAGE WHERE USER_ID = '{username}' ORDER BY P_STATUS_CODE  ".format(
             username = g.user.userId
            )
        result = conn.execute(sql).fetchall()

        #已申報貨件，顯示貨件編號，貨件申報日期,寫法是否正確？
        list1 = [] 
        list2 = [] 
        list3 = [] 
        list4 = [] 
        list5 = [] 

        for row in result:
            if row[5] == 0:
                list1.append(row)
            if row[5] == 1:
                list2.append(row)
            if row[5] == 2:
                list3.append(row)
            if row[5] == 3:
                list4.append(row)
            if row[5] == 4:
                list5.append(row)


    conn.close() 
    return render_template('package_manage.html',
                            SOURCE1 = list1,
                            SOURCE2 = list2,
                            SOURCE3 = list3,
                            SOURCE4 = list4,
                            SOURCE5 = list5)


@app.route('/package_declaration',methods=['POST'])
@login_required
def package_declaration():
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
        #用戶點擊按此申報貨件,P_ID暫時手動輸入
        sql6 = "INSERT INTO GROUP7.TB_PACKAGE (P_ID, USER_ID, W_COUNTRY, D_EXPRESS, D_TRACK_NO, P_DATE_DECLARATION) VALUES ('{P_ID}', '{USER_ID}', '{W_COUNTRY}', '{D_EXPRESS}', '{D_TRACK_NO}',SYSDATE)".format(
             P_ID = request.form['P_ID'],
             USER_ID = g.user.userId,
             W_COUNTRY = request.form['W_COUNTRY'],
             D_EXPRESS = request.form['D_EXPRESS'],
             D_TRACK_NO = request.form['D_TRACK_NO'],
            )
        sql7="INSERT INTO GROUP7.TB_GOODS_INFO (P_ID, G_NAME, QUANTITY, UNIT_PRICE) VALUES ('{P_ID}', '{G_NAME}', '{QUANTITY}', '{UNIT_PRICE}')".format(
            P_ID = request.form['P_ID'],
            G_NAME = request.form['G_NAME'],
            QUANTITY = request.form['QUANTITY'],
            UNIT_PRICE = request.form['UNIT_PRICE'],
            )
        #用戶點擊提交後
        result6 = conn.execute(sql6)
        result7 = conn.execute(sql7)
    conn.close()     
    return render_template('package_manage.html')

