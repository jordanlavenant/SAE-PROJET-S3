import sqlalchemy
from sqlalchemy import text, create_engine
import loginSQL as log
import pymysql

pymysql.install_as_MySQLdb()

def ouvrir_connexion():
    try:
        login = log.getLogin()
        passwd = log.getPasswd()
        serveur = log.getServeur()
        bd = log.getBd()
        
        engine = create_engine(f"mysql+mysqldb://{login}:{passwd}@{serveur}/{bd}")
        cnx = engine.connect()
    except Exception as err:
        print(err)
        raise err
    print("connexion réussie")
    return cnx
