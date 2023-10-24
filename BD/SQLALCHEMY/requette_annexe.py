import connexionPythonSQL as conn
from sqlalchemy import text

cnx = conn.get_cnx()

def connexion_utilisateur(cnx, email,mot_de_passe):
    result = cnx.execute(text("select * from UTILISATEUR where email = '" + email + "' and mdp = '" + mot_de_passe + "';"))
    for _ in result:
        return True
    return False

# print(connexion_utilisateur(cnx, "DUPONT@gmail.com", "azerty"))

def supprimer_utilisateur(cnx, idUt):
    try:
        cnx.execute(text( "delete from UTILISATEUR where idUt = '" + str(idUt) + " ';"))
        cnx.commit()
        print("utilisateur supprimé")
    except:
        print("erreur de suppression de l'utilisateur")
        raise