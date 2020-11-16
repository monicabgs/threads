from flask import render_template, flash, request, redirect, url_for
from app import db, app, loginManager
from app.models.forms import LoginForm, DataForm
from app.models.tables import User, Data_Input, Execution
from flask_login import login_user, logout_user
from .threads import Worker
import joblib as jb
import pandas as pd
import time

mdl = jb.load('app/models/mdl.pkl.z')
event = Event()
queue = Queue(maxsize=2)

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
    i = User("T721913", "python")
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

#Func 1: Get data
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
            
    return redirect(url_for("result"))

#Func 2: Result
@app.route("/result", methods=['GET', 'POST'])
def result():
    # Time to run without threads: 0.011029571999999987
    # Time to run with threads: 0.1369100889999999

    main_start = time.process_time()

    mdl = jb.load('app/models/mdl.pkl.z')

    if request.method == 'GET':
        df = db.session.execute('SELECT * FROM data_input ORDER BY ID DESC LIMIT 1')
        df_pd = pd.DataFrame(df)
        title = df_pd.iat[0, 1]

        queue = 

        result = mdl.predict_proba([title])[0][1]
        thread = Worker(target = execution_db)
        thread.run()
        db.session.query(Data_Input).delete()
        db.session.commit()
        print("Main time:", time.process_time() - main_start)
        
        return render_template("result.html", result=result, title=title)

# Func II Thread
@app.route('/exec')
def execution_db():
    # Time without threads = 0.11640994299999996
    # Time with threads = 0.12400040699999992

    exec_start = time.process_time()
    tpoooo = Execution("tpoooo", "tpoooo", "tpoooo", "tpoooo")
    tmoooo = Execution("tmoooo", "tmoooo", "tmoooo", "tmoooo")
    tnxooo = Execution("tnxooo", "tnxooo", "tnxooo", "tnxooo")
    tozooo = Execution("tozooo", "tozooo", "tozooo", "tozooo")

    db.session.add(tpoooo)
    db.session.add(tmoooo)
    db.session.add(tnxooo)
    db.session.add(tozooo)

    db.session.commit()
    time.sleep(10)
    db.session.query(Execution).delete()
    db.session.commit()
    
    print("Execution time:", time.process_time() - exec_start)
    
    return "OK"

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
