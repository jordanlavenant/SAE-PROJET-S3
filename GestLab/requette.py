from sqlalchemy import text
from .connexionPythonSQL import * 
from hashlib import sha256
cnx = ouvrir_connexion()

def get_cnx():
    return cnx

def afficher_table(cnx, table):

    result = cnx.execute(text("select * from " + table + " natural join MATERIAUX;"))
    for row in result:
        print(row)

def get_password_with_email(cnx, email):
    result = cnx.execute(text("select mdp from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]


# afficher_table(cnx, "STOCK")

def get_last_id(cnx , table, id):
    try:
        result = cnx.execute(text("select max("+ id +") from " + table + ";"))
        result = result.first()[0]
        print(result)
        return result
    except:
        print("erreur du nom de l'id ou du nom de la table")
        raise

# get_last_id(cnx, "STOCK", "idMat")

def get_nom_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIAUX where idMat = " + str(id) + ";"))
        result = result.first()
        print(result[1])
    except:
        print("erreur de l'id")
        raise

# get_nom_materiel_with_id(cnx, 3)

def get_nom_dom_cat_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIAUX natural join DOMAINE natural join CATEGORIE where idMat = " + str(id) + ";"))
        result = result.first()
        print("domaine : " + result[4], " | categorie : ",result[5])
    except:
        print("erreur de l'id")
        raise

# get_nom_dom_cat_materiel_with_id(cnx, 1)


def ajoute_materiel(cnx, nom, idDom, idCat):
    try:
        last_id = int(get_last_id(cnx, "MATERIAUX", "idMat")) + 1
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


def ajout_fournisseur(cnx, nom, adresse,mail, tel):
    try:
        last_id = int(get_last_id(cnx, "FOURNISSEUR", "idFournisseur")) + 1
        cnx.execute(text("insert into FOURNISSEUR (idFournisseur, nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values (" + str(last_id) + ", '" + nom + "', '" + adresse + "', '"  + mail + "', '"+ tel + "');"))
        cnx.commit()
        print("fournisseur ajouté")
    except:
        print("erreur d'ajout du fournisseur")
        raise

def connexion_utilisateur(cnx, email,mot_de_passe):
    result = cnx.execute(text("select * from UTILISATEUR where email = '" + email + "' and mdp = '" + mot_de_passe + "';"))
    for _ in result:
        return True
    return False

# print(connexion_utilisateur(cnx, "DUPONT@gmail.com", "azerty"))


def get_nom_whith_email(cnx, email):
    result = cnx.execute(text("select nom from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]
    
#get_nom_whith_email(cnx, "DUPONT@gmail.com")

def get_materiaux(cnx):
    result = cnx.execute(text("select * from MATERIAUX_RECHERCHE;"))
    for row in result:
        print(row[0])

# get_materiaux(cnx)

def ajout_proffesseur(cnx, nom, prenom, email, mdp, idSt = 1):
    
    try:
        last_id = int(get_last_id(cnx, "UTILISATEUR", "idUt")) + 1
        cnx.execute(text("insert into UTILISATEUR (idUt, nom, prenom, email, mdp, idSt) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idSt) + "');"))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise

# ajout_proffesseur(cnx, "blandeau", "erwan", "test@gmail.com", "erwanB")


def ajout_gestionnaire(cnx, nom, prenom, email, mdp, idSt = 3):
        
        try:
            last_id = int(get_last_id(cnx, "UTILISATEUR", "idUt")) + 1
            cnx.execute(text("insert into UTILISATEUR (idUt, nom, prenom, email, mdp, idSt) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idSt) + "');"))
            cnx.commit()
            print("utilisateur ajouté")
        except:
            print("erreur d'ajout de l'utilisateur")
            raise

# ajout_gestionnaire(cnx, "blandeauG", "erwang", "testG", "erwanBG")


def update_email_utilisateur(cnx, new_email, nom, mdp):
    try:
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and mdp = '" + mdp + "';"))
        cnx.commit()
        print("email mis a jour")
    except:
        print("erreur de mise a jour de l'email")
        raise

# update_email_utilisateur(cnx,"newErwan@gmail.com", "blandeau" ,"erwanB")


def modification_droit_utilisateur(cnx, id, idSt):
    try:
        cnx.execute(text("update UTILISATEUR set idSt = '" + str(idSt) + "' where idUt = '" + id + "';"))
        cnx.commit()
        print("droit mis a jour")
    except:
        print("erreur de mise a jour du droit")
        raise

# modification_droit_utilisateur(cnx, "testG", 2)


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

def hasher_mdp(mdp):
    m = sha256()
    m.update(mdp.encode("utf-8"))
    return m.hexdigest()

def get_nom_and_statut_and_email(cnx, email):
    result = cnx.execute(text("select nom, idSt from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0], row[1])
        return (row[0], row[1], email)
