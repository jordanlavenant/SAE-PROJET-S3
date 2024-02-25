from .connexionPythonSQL import *

cnx = ouvrir_connexion()

def get_cnx():
    """
    Renvoie la connexion à la base de données.

    Returns:
        cnx (object): L'objet de connexion à la base de données.
    """
    return cnx