from flask import render_template, flash, request, redirect, url_for, session
from app.models.forms import DataForm
from app.models.tables import Data_Input, User, Execution
from app import app, db
import pandas as pd
import joblib as jb
from app.controllers,threads import Worker


#Rodar modelo

# Case I:
@app.route("/get_title", methods=['GET', 'POST'])
def get_title():

# Entrada do modelo - request (string): 
# Recebe várias requisições simultâneamente: 
# target threads = title

    if request.method == 'GET':
        return render_template('get_data.html')
    else:
        in_data = Data_Input(data_input=request.form["data_input"])
        db.session.add(in_data)
        db.session.commit()

        df = db.session.execute('SELECT * FROM data_input ORDER BY ID DESC LIMIT 1')
        df_pd = pd.DataFrame(df)
        title = df_pd.iat[0, 1]

    return result

@app.route("/get_result", methods=['GET', 'POST'])
def run_model():

    mdl = jb.load('app/models/mdl.pkl.z')

    title = get_title()

    result = mdl.predict_proba([title])[0][1]

    return result

#Juntando os dois
#Processo I:
@app.route("/running_model", methods=['GET', 'POST'])
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

def initial_info():
    e = Execution("teste1")
    db.session.add(e)
    db.session.commit(e)
    
    e = Execution("teste2")
    db.session.add(e)
    db.session.commit(e)


#thread_list = ["Worker-1","Worker-2"]










