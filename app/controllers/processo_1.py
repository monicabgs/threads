@app.route('/start_task')
def start_task():
    def do_work(value):
        # do something that takes a long time
        import time
        time.sleep(value)

    thread = Thread(target=do_work, kwargs={'value': request.args.get('value', 20))
    thread.start()
    return 'started'




@app.route('/start_task')
def start_task():

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