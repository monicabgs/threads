input_data = "Oi, tudo bem com você?"

def get_data(input_data=str):

    if input_data:
        mdl = jb.load('app/models/mdl.pkl.z')
        result = mdl.predict_proba([input_data])[0][1]
        return result
    return "Error"



