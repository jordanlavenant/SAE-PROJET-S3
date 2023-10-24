
import connexionPythonSQL as conn
import requette_annexe as req_annexe
from sqlalchemy import text

cnx = conn.get_cnx()


def update_email_utilisateur(cnx, new_email, nom, mdp):
    try:
        mdp_hash = req_annexe.hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and mdp = '" + mdp_hash + "';"))
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


def update_mdp_utilisateur(cnx, email,mdp, new_mdp):
    try:
        init_mdp = req_annexe.hasher_mdp(mdp)
        new_mdp_hash = req_annexe.hasher_mdp(new_mdp)
        cnx.execute(text(" update UTILISATEUR set mdp = '" + new_mdp_hash + "' where email = '" + email + "' and mdp = '" + init_mdp + "'"))
        cnx.commit()
        print("mdp mis a jour")
    except:
        print("erreur de mise a jour du mdp")
        raise

# update_mdp_utilisateur(cnx, "leo@kd", "jI2cFCkCQ9","leo")

def update_nom_utilisateur(cnx, email, new_nom, mdp):
    try:
        mdp_hash = req_annexe.hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "' and mdp = '" + mdp_hash + "';"))
        cnx.commit()
        print("nom mis a jour")
    except:
        print("erreur de mise a jour du nom")
        raise

#update_nom_utilisateur(cnx, "leo@kd", "lucidor", "leo")

def update_prenom_utilisateur(cnx, email, new_prenom, mdp):
    try:
        mdp_hash = req_annexe.hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "' and mdp = '" + mdp_hash + "';"))
        cnx.commit()
        print("prenom mis a jour")
    except:
        print("erreur de mise a jour du prenom")
        raise

# update_prenom_utilisateur(cnx, "newDupont@gmail.com", "newPierre")