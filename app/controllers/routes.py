from flask import render_template, flash, request, redirect, url_for
from app import db, app, loginManager
from app.models.forms import LoginForm, DataForm
from app.models.tables import User, Data_Input, Execution
from flask_login import login_user, logout_user
from .threads import Worker
import joblib as jb
import pandas as pd
import logging
import time
#import threading

mdl = jb.load('app/models/mdl.pkl.z')

@loginManager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/db')
def db_create_all():
    db.create_all()
    return 'Tables created'

@app.route("/user/<info>")
@app.route("/user/", defaults={"info":None})
def teste(info):
    i = User("T721914", "python")
    db.session.add(i)
    db.session.commit()
        
    r = User.query.filter_by(username="T722913").all()
    print(r)
    return "OK" 

#Insert User in Database
@app.route("/user/<info>")
@app.route("/user/", defaults={"info":None})
def user(info):
    i = User("T722913", "python")
    db.session.add(i)
    db.session.commit()
    
    r = User.query.filter_by(username="T722913").all()
    print(r)
    return "OK"

#Home
@app.route("/home")
def home():
    return render_template("home.html")

#Login
@app.route("/login", methods=['GET','POST']) 
def login():  
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Logged in.')
            return redirect(url_for("get_data"))
        else:
            flash('Invalid Login.')
    else:
        print(form.errors)
    return render_template("login.html", form=form)

base_url = 'http://127.0.0.1:5000/get_data'

def get_response(url):
    response = get(url, stream=True)

#Func 1: Get data
@app.route("/get_data/", methods=['GET', 'POST'])
def get_data():
    # Tempo sem threads: 0.0128s
    # Tempo com threads: 0.0128s

    start = time.perf_counter()

    get_data_start_time = time.process_time()
    if request.method == 'GET':    
        return render_template('get_data.html')
    else:
        request_data = request.get_json()
        logging.info(request_data)
        in_data = Data_Input(data_input=request.form["data_input"])
        db.session.add(in_data)
        db.session.commit()

    end = time.perf_counter()

    print("Get data time:", end - start)

    return redirect(url_for("result"))

#Func 2: Result
@app.route("/result", methods=['GET', 'POST'])
def result():

    # Tempo sem threads: 0.0368s  
    # Tempo com threads: 0.04377s 

    start = time.perf_counter()

    mdl = jb.load('app/models/mdl.pkl.z')

    if request.method == 'GET':
        df = db.session.execute('SELECT * FROM data_input ORDER BY ID DESC LIMIT 1')
        df_pd = pd.DataFrame(df)
        title = df_pd.iat[0, 1]

        result = mdl.predict_proba([title])[0][1]
        db.session.query(Data_Input).delete()
        db.session.commit()

        t = Worker(target=execution_db, name='Thread1')
        t.start()

        end = time.perf_counter()

        print("Result time:", end - start)
        
        return render_template("result.html", result=result, title=title)

# Func II Thread
#@app.route('/exec')
def execution_db():
    # Tempo sem threads = 10.0487s 
    # Tempo com threads = 10.1384s

    db.session.query(Execution).delete()
    db.session.commit()

    start = time.perf_counter()


    tpoooo = Execution("tpoooo", "tpoooo", "tpoooo", "tpoooo")
    tmoooo = Execution("tmoooo", "tmoooo", "tmoooo", "tmoooo")
    tnxooo = Execution("tnxooo", "tnxooo", "tnxooo", "tnxooo")
    tozooo = Execution("tozooo", "tozooo", "tozooo", "tozooo")

    db.session.add(tpoooo)
    db.session.add(tmoooo)
    db.session.add(tnxooo)
    db.session.add(tozooo)

    db.session.commit()

    print('Dados de execução gravados na tabela.')

    time.sleep(10)
    
    end = time.perf_counter()
    
    print("Execution time:", end - start)


"""
# Func I Thread
@app.route("/running", methods=['GET', 'POST'])
def running_model():

    mdl = jb.load('app/models/mdl.pkl.z')

    def raw_data():

        if request.method == 'GET':
            return render_template('get_data.html')
        else:
            in_data = Data_Input(data_input=request.form["data_input"])
            db.session.add(in_data)
            db.session.commit()

            df = db.session.execute('SELECT * FROM data_input ORDER BY ID DESC LIMIT 1')
            df_pd = pd.DataFrame(df)
            title = df_pd.iat[0, 1]
            return title

    title = raw_data()
    result = mdl.predict_proba([title])[0][1]
    return render_template("result.html", result=result, title=title)
"""

#Logout
@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('home'))


"""#------------------------  Case II: Many requests -------------------------------
#Func1: Get first data
@app.route("/get_data", methods=['GET', 'POST'])
def get_data():

    if request.method == 'GET':
        return render_template('get_data.html')
    else:
        in_data = Data_Input(data_input=request.form["data_input"])
        print(type(in_data))
        print(in_data)
        db.session.add(in_data)
        db.session.commit()
            
    return redirect(url_for("get_more_data", data_input=in_data))

#Get more data
@app.route("/get_more_data", methods=['GET', 'POST'])
def more_data():

    if request.method == 'GET':
        return render_template('get_more_data.html')
    else:
        return redirect(url_for('get_data'))
"""
