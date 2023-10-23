import connexionPythonSQL

cnx= connexionPythonSQL.ouvrir_connexion()
cnx.close()

cnx.execute("requette")