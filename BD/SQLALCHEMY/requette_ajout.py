import connexionPythonSQL as conn
import requette_get as req_get
import requette_annexe as req_annexe
from sqlalchemy import text
from hashlib import sha256


cnx = conn.get_cnx()

def ajout_proffesseur(cnx, nom, prenom, email, mdp, idSt = 1):
    
    try:
        last_id = int(req_get.get_last_id(cnx, "UTILISATEUR", "idUt")) + 1
        try:
            cnx.execute(text("insert into UTILISATEUR (idUt, nom, prenom, email, mdp, idSt) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idSt) + "');"))
            cnx.commit()
            print("utilisateur ajouté")
        except:
            print("erreur d'ajout de l'utilisateur")
            raise
    except:
        print("erreur d'ajout de l'utilisateur")
        raise

# ajout_proffesseur(cnx, "lucidor", "leo", "leo@", "leo")

def ajout_administrateur(cnx, nom, prenom, email, idSt = 2):
    
    try:
        mdpRandom = req_annexe.generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = req_annexe.hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (nom, prenom, email, mdp, idSt) values ('" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "', '" + str(idSt) + "');"))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise

# ajout_administrateur(cnx, "admin", "admin", "admin@testhash2")

def ajout_gestionnaire(cnx, nom, prenom, email, idSt = 3):
        
        try:
            mdpRandom = req_annexe.generer_mot_de_passe()
            # envoyer mail avec mdpRandom
            print(mdpRandom)
            mdphash = req_annexe.hasher_mdp(mdpRandom)
            cnx.execute(text("insert into UTILISATEUR (nom, prenom, email, mdp, idSt) values ('" +  nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "', '" + str(idSt) + "');"))
            cnx.commit()
            print("utilisateur ajouté")
        except:
            print("erreur d'ajout de l'utilisateur")
            raise


ajout_gestionnaire(cnx, "leo", "leo", "leo@kd")


def ajout_fournisseur(cnx, nom, adresse,mail, tel):
    try:
        cnx.execute(text("insert into FOURNISSEUR (idFournisseur, nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values (" +  nom + "', '" + adresse + "', '"  + mail + "', '"+ tel + "');"))
        cnx.commit()
        print("fournisseur ajouté")
    except:
        print("erreur d'ajout du fournisseur")
        raise

def ajoute_materiel(cnx, nom, idDom, idCat):
    try:
        last_id = int(req_get.get_last_id(cnx, "MATERIAUX", "idMat")) + 1
        cnx.execute(text("insert into MATERIAUX (idMat,nomMat, idDom, idCat) values (" + str(last_id) + ", '" + nom + "', " + str(idDom) + ", " + str(idCat) + ");"))
        cnx.commit()
        print("materiel ajouté")
    except:
        print("erreur d'ajout du materiel")
        raise

def ajout_quantite(cnx, idMat, quantite):
    try:
        cnx.execute(text("insert into STOCK (idMat, quantite) values (" + str(idMat) + ", " + str(quantite) + ");"))
        cnx.commit()
        print("quantite ajouté dans un nouveau stock")
    except:
        print("id deja utiliser")
        try:
            cnx.execute(text("update STOCK set quantite = quantite + " + str(quantite) + " where idMat = " + str(idMat) +";"))
            cnx.commit()
            print("quantite ajouté")
        except:
            print("erreur d'ajout de la quantité")
            raise

# ajout_quantite(cnx, 3, 50)
