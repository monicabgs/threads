from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_wtf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')#Aplicar configurações feitas no arquivo (sem o .py)

db = SQLAlchemy(app)
migrate = Migrate(app, db) #Responsável pelas alterações realizadas no db

manager = Manager(app)
manager.add_command('db', MigrateCommand) #Responsável pelos comandos que vou dar para a aplicação

loginManager = LoginManager()
loginManager.init_app(app)

csfr = CsrfProtect(app)

from app.models import tables
from app.controllers import routes