import click
import sqlalchemy  
from .app import app
import os.path

# @app.cli.command()
# def syncdb():
#     '''Creates all missing tables.'''
#     db. create_all()

# @app.cli.command()
# @click.argument('username')
# @click.argument('password')
# def newuser(username, password ):
#     '''Adds a new user.'''
#     from .models import User
#     from hashlib import sha256
#     m = sha256()
#     m.update(password.encode())
#     u = User(username=username ,password=m.hexdigest())
#     db.session.add(u)
#     db.session.commit()

# @app.cli.command()
# @click.argument('username')
# @click.argument('password')
# def passwd(username, password) :
#     '''Change user's password'''
#     from hashlib import sha256
#     from .models import user_in_bd, get_user, User
#     m = sha256()
#     m.update(password.encode())
#     if user_in_bd(username) is None :
#         print("L'utilisateurs n'est pas enregistre dans la bd \nVeuillez faire : flask newuser " + username + " " + password)
#     else :
#         u = get_user(username)
#         u.password = m.hexdigest()
#         db.session.commit()