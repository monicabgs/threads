from flask import render_template, flash, request, redirect, url_for
from app import db, app, loginManager
from app.models.forms import LoginForm, DataForm
from app.models.tables import User, Data_Input
from flask_login import login_user, logout_user
import joblib as jb


mdl = jb.load('app/models/mdl.pkl.z')

@loginManager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/db')
def db_create_all():
    db.create_all()
    return 'Tables created'

#Insert User in Database
@app.route("/user/<info>")
@app.route("/user/", defaults={"info":None})
def teste(info):
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

@app.route("/get_data", methods=['GET', 'POST'])
def get_data():

    if request.method == 'GET':
        return render_template('get_data.html')
    else:
        in_data = Data_Input(data_input=request.form["data_input"])
        db.session.add(in_data)
        db.session.commit()
            
    return redirect(url_for("more_data", data_input=in_data))


@app.route("/more_data", methods=['GET', 'POST'])
def more_data():

    if request.method == 'GET':
        return render_template('more_data.html')
    else:
        return redirect(url_for('get_data'))
        

@app.route("/result", methods=['GET', 'POST'])
def result():

    mdl = jb.load('app/models/mdl.pkl.z')

    if request.method == 'GET':
        df = db.session.execute('SELECT * FROM data_model ORDER BY ID DESC LIMIT 1')
        df_pd = pd.DataFrame(df)
        title = df_pd.iat[0, 1]

        result = mdl.predict_proba([title])[0][1]
        db.session.query(Data_Model).delete()
        db.session.commit()
        
        return render_template("result.html", result=result, title=title)
    else:   
        return redirect(url_for("get_data"))

#Logout
@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('home'))



#Logout
@app.route('/ok')
def ok():
    #r = User.query.filter(User.id==id).first()
    #s = User.query.filter_by(User.id==id).first()
    #r = User.query.filter_by(username="T722913").all()


    r = User.query.first(id)

    print (type(r))


    return 'OK'    

    """
    #Insert User in Database
    @app.route("/test/<info>")
    @app.route("/test/", defaults={"info":None})
    def teste(info):
        i = User("T722913", "python")
        db.session.add(i)
        db.session.commit()
        
        r = User.query.filter_by(username="T722913").all()
        print(r)
        return "OK"    

    """