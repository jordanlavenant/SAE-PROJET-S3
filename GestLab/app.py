from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager(app)
#login_manager.login_view = "login"

# def mkpath(p):
#     return os.path.normpath (os.path.join(os.path.dirname( __file__ ),p))

# app. config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
# db = SQLAlchemy(app) 