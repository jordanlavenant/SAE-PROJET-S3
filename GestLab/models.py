#from .app import db
from flask_login import UserMixin
#from .app import login_manager

# class User(db.Model, UserMixin):
#     username = db.Column(db.String(50), primary_key=True)
#     password = db.Column(db.String(64))

#     def get_id(self):
#         return self.username

# @login_manager.user_loader
# def load_user(username):
#     return User.query.get(username)

# def user_in_bd(username):
#     return User.query.filter_by(username=username).first()

