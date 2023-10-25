
import requette_annexe as req_annexe
import requette_get as req_get
from sqlalchemy import text

def update_email_utilisateur(cnx, new_email, nom, mdp):
    try:
        mdp_hash = req_annexe.hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("email mis a jour")
    except:
        print("erreur de mise a jour de l'email")
        raise

# update_email_utilisateur(cnx,"leo@", "leo" ,"12oXevnYPs")


def update_droit_utilisateur(cnx, id, idSt):
    try:
        cnx.execute(text( "update UTILISATEUR set idStatut = '" + str(idSt) + "' where idUtilisateur = '" + str(id) + "';"))
        cnx.commit()
        print("droit mis a jour")
    except:
        print("erreur de mise a jour du droit")
        raise

# update_droit_utilisateur(cnx, 5 , 1)


def update_mdp_utilisateur(cnx, email,mdp, new_mdp):
    try:
        init_mdp = req_annexe.hasher_mdp(mdp)
        new_mdp_hash = req_annexe.hasher_mdp(new_mdp)
        mdp_get = req_get.get_password_hashed_with_email(cnx, email)
        if mdp_get != init_mdp:
            print("mdp incorrect")
            return False
        else:
            cnx.execute(text(" update UTILISATEUR set motDePasse = '" + new_mdp_hash + "' where email = '" + email + "' and motDePasse = '" + init_mdp + "'"))
            cnx.commit()
            print("mdp mis a jour")
            return True
    except:
        print("erreur de mise a jour du mdp")
        return None

# update_mdp_utilisateur(cnx, "leo@", "leo","leoo")







# normalement on ne les utilise pas #

def update_nom_utilisateur(cnx, email, new_nom, mdp):
    try:
        mdp_hash = req_annexe.hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("nom mis a jour")
    except:
        print("erreur de mise a jour du nom")
        raise

#update_nom_utilisateur(cnx, "leo@kd", "lucidor", "leo")

def update_prenom_utilisateur(cnx, email, new_prenom, mdp):
    try:
        mdp_hash = req_annexe.hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("prenom mis a jour")
    except:
        print("erreur de mise a jour du prenom")
        raise

# update_prenom_utilisateur(cnx, "newDupont@gmail.com", "newPierre")