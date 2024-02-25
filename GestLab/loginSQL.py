login = "blandeau" # pip install pymysql
passwd = "Loulou34230."
serveur= "mysql-blandeau.alwaysdata.net"
bd = "blandeau_gestlab25"

def getLogin():
    """
    Renvoie le login.

    Returns:
        str: Le login.
    """
    return login

def getPasswd():
    """
    Renvoie le mot de passe.

    Returns:
        str: Le mot de passe.
    """
    return passwd

def getServeur():
    """
    Renvoie le nom du serveur utilisé pour la connexion à la base de données.

    Returns:
        str: Le nom du serveur.
    # Code implementation goes here
    Returns the value of the serveur variable.
    """
    return serveur

def getBd():
    """
    Renvoie la base de données utilisée par l'application.

    Returns:
        bd (str): Le nom de la base de données.
    """
    return bd