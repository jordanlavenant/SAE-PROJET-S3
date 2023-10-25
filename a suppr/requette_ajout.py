from requette import get_cnx
import requette_get as req_get
import requette_annexe as req_annexe
from sqlalchemy import text
from hashlib import sha256


cnx = get_cnx()

def ajout_proffesseur(cnx, nom, prenom, email, mdp, idStatut = 1):
    
    try:
        last_id = int(req_get.get_last_id(cnx, "UTILISATEUR", "idUt")) + 1
        try:
            cnx.execute(text("insert into UTILISATEUR (idUt, nom, prenom, email, mdp, idStatut) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idStatut) + "');"))
            cnx.commit()
            print("utilisateur ajouté")
        except:
            print("erreur d'ajout de l'utilisateur")
            raise
    except:
        print("erreur d'ajout de l'utilisateur")
        raise

# ajout_proffesseur(cnx, "lucidor", "leo", "leo@", "leo")

def ajout_administrateur(cnx, nom, prenom, email, idStatut = 2):
    
    try:
        mdpRandom = req_annexe.generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = req_annexe.hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (nom, prenom, email, mdp, idStatut) values ('" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "', '" + str(idStatut) + "');"))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise

# ajout_administrateur(cnx, "admin", "admin", "admin@testhash2")

def ajout_gestionnaire(cnx, nom, prenom, email, idStatut = 3):
        
        try:
            mdpRandom = req_annexe.generer_mot_de_passe()
            # envoyer mail avec mdpRandom
            print(mdpRandom)
            mdphash = req_annexe.hasher_mdp(mdpRandom)
            cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" +  nom + "', '" + prenom + "', '" + email +  "', '" + mdphash + "');"))
            cnx.commit()
            print("utilisateur ajouté")
        except:
            print("erreur d'ajout de l'utilisateur")
            raise


# ajout_gestionnaire(cnx, "colin", "colin", "colin@")

def add_proffesseur(cnx, nom, prenom, email, mdp, idSt = 1):
    
    try:
        mdpRandom = req_annexe.generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = req_annexe.hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR ( nom, prenom, email, mdp, idSt) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idSt) + "');"))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise


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
        cnx.execute(text("insert into MATERIAUX (idMateriel,idDom, idCategorie, idFDS, nomMateriel ) values (" + str(last_id) + ", '" + nom + "', " + str(idDom) + ", " + str(idCat) + ");"))
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




def delete_utilisateur(cnx, idUt):
    try:
        cnx.execute(text( "delete from UTILISATEUR where idUtilisateur = '" + str(idUt) + " ';"))
        cnx.commit()
        print("utilisateur supprimé")
    except:
        print("erreur de suppression de l'utilisateur")
        raise

# def ajout_blob_in_risques(cnx, idFDS, idRisque, file_path):
#     try:
#         blob = req_annexe.convert_data(file_path)
#         cnx.execute("insert into RISQUE (idRisque, nomRisque, pictogramme) values (%s, %s, %s);", idFDS, idRisque, blob)
#         cnx.commit()
#         print("Blob ajouté")
#     except Exception as e:
#         raise

# ajout_blob_in_risques(cnx, 4, 1, "r.png")
