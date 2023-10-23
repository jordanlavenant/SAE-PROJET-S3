#from .app import db
from flask_login import UserMixin
from .app import login_manager
from .requette import *

# class User(db.Model, UserMixin):
#     username = db.Column(db.String(50), primary_key=True)
#     password = db.Column(db.String(64))

#     def get_id(self):
#         return self.username

@login_manager.user_loader
def load_user(email):
    cnx = get_cnx()
    return get_nom_whith_email(cnx, email)

# def user_in_bd(username):
#     return User.query.filter_by(username=username).first()

