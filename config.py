import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
'data_storage.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'nl.4.5@534.3271AnTx67$'


