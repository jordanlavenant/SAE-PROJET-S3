from hashlib import sha256
import connexionPythonSQL as conn
from sqlalchemy import text
import random
import string


cnx = conn.get_cnx()

def utilisateur_is_in_db_with_email_passwrd(cnx, email,mot_de_passe):
    result = cnx.execute(text("select * from UTILISATEUR where email = '" + email + "' and mdp = '" + mot_de_passe + "';"))
    for _ in result:
        return True
    return False

# print(utilisateur_is_in_db_with_email_passwrd(cnx, "DUPONT@gmail.com", "azerty"))

def delete_utilisateur(cnx, idUt):
    try:
        cnx.execute(text( "delete from UTILISATEUR where idUt = '" + str(idUt) + " ';"))
        cnx.commit()
        print("utilisateur supprimé")
    except:
        print("erreur de suppression de l'utilisateur")
        raise


def generer_mot_de_passe():
    caracteres = string.ascii_letters + string.digits
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

    return mot_de_passe

def hasher_mdp(mdp):
    m = sha256()
    m.update(mdp.encode("utf-8"))
    return m.hexdigest()



