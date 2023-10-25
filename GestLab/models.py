#from .app import db
from flask_login import UserMixin
from .app import login_manager
from .requette import *

@login_manager.user_loader
def load_user(email):
    cnx = get_cnx()
    return get_nom_whith_email(cnx, email)


