from app import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Data_Input(db.Model):
    __tablename__ = "data_input"

    id = db.Column(db.Integer, primary_key=True)
    data_input = db.Column(db.String, nullable=False)

    def __init__(self, data_input):
        self.data_input = data_input


class Model_Result(db.Model):
    __tablename__ = "model_result"

    id = db.Column(db.Integer, primary_key=True)
    model_result = db.Column(db.String, nullable=False)

    def __init__(self, model_result):
        self.model_result = model_result

class Execution(db.Model):
    __tablename__ = "execution"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    data_input = db.Column(db.String, nullable=False) 
    model_result = db.Column(db.String, nullable=False)
    msg_status = db.Column(db.String, nullable=False)


    def __init__(self, username, data_input, model_result, msg_status):
 
        self.username = username
        self.data_input = data_input
        self.model_result = model_result
        self.msg_status = msg_status

    