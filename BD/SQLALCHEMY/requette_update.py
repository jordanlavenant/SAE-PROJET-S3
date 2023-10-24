
import connexionPythonSQL as conn
from sqlalchemy import text

cnx = conn.get_cnx()


def update_email_utilisateur(cnx, new_email, nom, mdp):
    try:
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and mdp = '" + mdp + "';"))
        cnx.commit()
        print("email mis a jour")
    except:
        print("erreur de mise a jour de l'email")
        raise

# update_email_utilisateur(cnx,"newErwan@gmail.com", "blandeau" ,"erwanB")


def update_droit_utilisateur(cnx, id, idSt):
    try:
        cnx.execute(text("update UTILISATEUR set idSt = '" + str(idSt) + "' where idUt = '" + id + "';"))
        cnx.commit()
        print("droit mis a jour")
    except:
        print("erreur de mise a jour du droit")
        raise

# update_droit_utilisateur(cnx, "testG", 2)


def update_mdp_utilisateur(cnx, email, new_mdp):
    try:
        cnx.execute(text("update UTILISATEUR set mdp = '" + new_mdp + "' where email = '" + email + "';"))
        cnx.commit()
        print("mdp mis a jour")
    except:
        print("erreur de mise a jour du mdp")
        raise

# update_mdp_utilisateur(cnx, "newDupont@gmail.com", "newMdp")

def update_nom_utilisateur(cnx, email, new_nom):
    try:
        cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "';"))
        cnx.commit()
        print("nom mis a jour")
    except:
        print("erreur de mise a jour du nom")
        raise

# update_nom_utilisateur(cnx, "newDupont@gmail.com", "newDupont")

def update_prenom_utilisateur(cnx, email, new_prenom):
    try:
        cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "';"))
        cnx.commit()
        print("prenom mis a jour")
    except:
        print("erreur de mise a jour du prenom")
        raise

# update_prenom_utilisateur(cnx, "newDupont@gmail.com", "newPierre")