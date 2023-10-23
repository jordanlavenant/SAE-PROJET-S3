import click
import sqlalchemy  
from .app import app
import os.path


# @app.cli.command()
# @click.argument('filename')
# def loaddb(filename):
#     '''Creates the tables and populates them with data. '''

#     # création de toutes les tables
#     db.create_all()

#     # chargement de notre jeu de données
#     import yaml
#     books = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "data.yml")))

#     # import des modèles
#     from.models import Author, Book

#     # première passe: création de tous les auteurs
#     authors = {}
#     for b in books:
#         a = b["author"]
#         if a not in authors:
#             o = Author(name=a)
#             db.session.add(o)
#             authors[a] = o
#     db.session.commit()

#     # deuxième passe: création de tous les livres
#     for b in books:
#         a = authors[b["author"]]
#         o = Book(price = b["price"],
#                 title = b["title"],
#                 url = b["url"],
#                 img = b["img"],
#                 author_id = a.id)
#         db.session.add(o)
#     db.session.commit()

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