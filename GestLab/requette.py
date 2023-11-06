import random
import string
from sqlalchemy import text
from .connexionPythonSQL import *
from hashlib import sha256
from datetime import datetime, timedelta
import random
import string
cnx = ouvrir_connexion()

def get_cnx():
    return cnx

def afficher_table(cnx, table):

    result = cnx.execute(text("select * from " + table + " natural join MATERIEL;"))
    for row in result:
        print(row)

def get_password_with_email(cnx, email):
    result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
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

# get_last_id(cnx, "STOCK", "idMateriel")

def get_nom_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIEL where idMateriel = " + str(id) + ";"))
        result = result.first()
        return result
    except:
        print("erreur de l'id")
        raise

def get_nom_dom_cat_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIEL natural join DOMAINE natural join CATEGORIE where idMateriel = " + str(id) + ";"))
        result = result.first()
        print("domaine : " + result[4], " | categorie : ",result[5])
    except:
        print("erreur de l'id")
        raise

# get_nom_dom_cat_materiel_with_id(cnx, 1)

def ajoute_materiel(cnx, nom, idDom, idCat):
    try:
        last_id = int(get_last_id(cnx, "MATERIEL", "idMateriel")) + 1
        cnx.execute(text("insert into MATERIEL (idMateriel,nomMat, idDom, idCat) values (" + str(last_id) + ", '" + nom + "', " + str(idDom) + ", " + str(idCat) + ");"))
        cnx.commit()
        print("materiel ajouté")
    except:
        print("erreur d'ajout du materiel")
        raise

def ajout_quantite(cnx, idMateriel, quantite):
    try:
        cnx.execute(text("insert into STOCK (idMateriel, quantite) values (" + str(idMateriel) + ", " + str(quantite) + ");"))
        cnx.commit()
        print("quantite ajouté dans un nouveau stock")
    except:
        print("id deja utiliser")
        try:
            cnx.execute(text("update STOCK set quantite = quantite + " + str(quantite) + " where idMateriel = " + str(idMateriel) +";"))
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

def get_MATERIEL(cnx):
    result = cnx.execute(text("select * from MATERIEL_RECHERCHE;"))
    for row in result:
        print(row[0])

# get_MATERIEL(cnx)


def update_email_utilisateur(cnx, new_email, nom, mdp):
    try:
        mdp_hash = hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("email mis a jour")
        return True
    except:
        print("erreur de mise a jour de l'email")
        return False

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


def update_mdp_utilisateur(cnx, email,mdp, new_mdp):
    try:
        init_mdp = hasher_mdp(mdp)
        new_mdp_hash = hasher_mdp(new_mdp)
        mdp_get = get_password_hashed_with_email(cnx, email)
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
        
def get_password_hashed_with_email(cnx, email):
    result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]

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

def generer_mot_de_passe():
    caracteres = string.ascii_letters + string.digits
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

    return mot_de_passe

def hasher_mdp(mdp):
    m = sha256()
    m.update(mdp.encode("utf-8"))
    return m.hexdigest()


def get_nom_and_statut_and_email(cnx, email):
    result = cnx.execute(text("select nom, idStatut from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0], row[1])
        return (row[0], row[1], email)


def get_user_with_statut(cnx, nomStatut):
    liste = []
    result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where nomStatut = '" + str(nomStatut) + "';"))
    for row in result:
        print(row[0],row[2],row[3])
        liste.append((row[0],row[2],row[3]))
    return liste

def get_all_user(cnx, idStatut=None):
    liste = []
    if idStatut is None:
        result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where idStatut != 1;"))
    else:
        result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where idStatut = '" + str(idStatut) + "';"))
    for row in result:
        liste.append((row[1],row[0],row[2],row[3],row[4]))
    return (liste, len(liste))

def get_all_information_to_Materiel(cnx, nomcat=None):
    my_list = []
    if nomcat is None:
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire  from MATERIEL natural left join STOCKLABORATOIRE natural left join DATEPEREMPTION natural left join DOMAINE natural left join CATEGORIE natural join FDS;"))
        for row in result:
            my_list.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    else:
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire  from MATERIEL natural left join STOCKLABORATOIRE natural left join DATEPEREMPTION natural left join DOMAINE natural left join CATEGORIE natural join FDS where nomCategorie = '" + nomcat + "';"))
        for row in result:
            my_list.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    print(my_list)
    return my_list

def get_categories(cnx):
    liste = []
    result = cnx.execute(text("select * from CATEGORIE;"))
    for row in result:
        liste.append((row[0],row[1]))
    return liste

def get_nb_alert(cnx):
    try:
        # Calculer la date qui est 1 mois à partir de maintenant
        today = datetime.now()
        ten_days_from_now = datetime.now() + timedelta(days=10)
        # Exécuter la requête SQL
        result = cnx.execute(
            text(
                "SELECT COUNT(*) FROM MATERIEL NATURAL JOIN DATEPEREMPTION WHERE datePeremption < '" + ten_days_from_now.strftime('%Y-%m-%d') + "' OR datePeremption <= '" + today.strftime('%Y-%m-%d') + "';"))
        count = result.first()[0]
        print(count)
        return count
    except Exception as e:
        print("Erreur lors de la récupération du nombre d'alertes :", str(e))
        raise

def get_info_materiel_alert(cnx):
    try:
        # Calculer la date qui est 1 mois à partir de maintenant
        today = datetime.now()
        ten_days_from_now = datetime.now() + timedelta(days=10)
        # Exécuter la requête SQL
        result = cnx.execute(
            text(
                "SELECT nomMateriel,idMateriel FROM MATERIEL NATURAL JOIN DATEPEREMPTION WHERE datePeremption < '" + ten_days_from_now.strftime('%Y-%m-%d') + "' OR datePeremption <= '" + today.strftime('%Y-%m-%d') + "';"))
        liste_nom = []
        for row in result:
            liste_nom.append(row)
        return liste_nom
    except Exception as e:
        print("Erreur lors de la récupération du nombre d'alertes :", str(e))
        raise

def get_nb_demande(cnx):
    try:
        result = cnx.execute(text("SELECT count(*) FROM DEMANDE NATURAL JOIN BONCOMMANDE NATURAL JOIN ETATCOMMANDE WHERE nomEtat = 'En attente';"))
        count = result.first()[0]
        print(count)
        return count
    except Exception as e:
        print("Erreur lors de la récupération du nombre de demandes :", str(e))
        raise
    
def get_info_demande(cnx):
    try:
        result = cnx.execute(text("SELECT idDemande, nom, prenom, idBonCommande from UTILISATEUR natural join DEMANDE natural join BONCOMMANDE;"))
        info_commande = []
        for row in result:
            info_commande.append(row)
        return  info_commande
    except Exception as e:
        print("Erreur lors de la récupération des informations sur les commandes :", str(e))
        raise

def get_info_demande_with_id(cnx, idDemande):
    try:
        result = cnx.execute(text("SELECT nom, prenom, quantite, nomMateriel, idBonCommande from UTILISATEUR natural join DEMANDE natural join AJOUTERMATERIEL natural join MATERIEL natural join BONCOMMANDE where idDemande =" + str(idDemande) + ";"))
        info_demande = []
        for row in result:
            info_demande.append(row)
        return info_demande
    except Exception as e:
        print("Erreur lors de la récupération des informations sur les commandes :", str(e))
        raise

def ajout_professeur(cnx, nom, prenom, email, idStatut = 2):
    
    try:
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
        cnx.commit()
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False

def ajout_gestionnaire(cnx, nom, prenom, email, idStatut = 3):
    
    try:
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
        cnx.commit()
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False

def ajout_laborantin(cnx, nom, prenom, email, idStatut = 4):
    
    try:
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
        cnx.commit()
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False


def get_all_information_utilisateur_with_id(cnx,id):
    try:
        result = cnx.execute(text("select nom,prenom,email,nomStatut from UTILISATEUR natural join STATUT where idUtilisateur = " + str(id) + ";"))
        for row in result:
            print(row)
            return row
    except:
        print("erreur de l'id")
        raise

def get_all_information_to_Materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire  from MATERIEL natural left join STOCKLABORATOIRE natural left join DATEPEREMPTION natural left join DOMAINE natural left join CATEGORIE natural join FDS where idMateriel = " + str(id) + ";"))
        for row in result:
            return row
    except:
        print("erreur de l'id")
        raise

def update_all_information_utillisateur_with_id(cnx,id,nom,prenom,email,idStatut):
    try:
        cnx.execute(text( "update UTILISATEUR set nom = '" + nom + "', prenom = '" + prenom + "', email = '" + email + "', idStatut = '" + str(idStatut) + "' where idUtilisateur = " + str(id) + ";"))
        cnx.commit()
        return True
    except:
        print("erreur de l'id")
        return False

def recherche_all_in_utilisateur_with_search(cnx, search):
    try:
        list = []
        result = cnx.execute(text("select * from UTILISATEUR where nom like '%" + search + "%'" or " prenom like '%" + search + "%' ;"))
        for row in result:
            list.append(row)
        return (list, len(list))
    except:
        print("erreur de recherche")
        raise

# recherche_all_in_utilisateur_with_search(cnx, "jo")

def recherche_all_in_materiel_with_search(cnx, search):
    try:
        list = []
        result = cnx.execute(text("select * from MATERIEL where nomMateriel like '%" + search + "%' ;"))
        for row in result:
            print(row)
            list.append(row)
        return list
    except:
        print("erreur de recherche")
        raise

def get_domaine(cnx):
    try:
        list = []
        result = cnx.execute(text("select * from DOMAINE ;"))
        for row in result:
            print(row)
            list.append(row)
        return list
    except:
        print("erreur de l'id")
        raise

def get_all_information_to_Materiel_cat_com(cnx):
    try:
        list = []
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite from MATERIEL  NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE ;"))
        for row in result:
            print(row)
            list.append(row)
        return list
    except:
        print("erreur de l'id")
        raise

def get_info_rechercheMateriel(cnx):
    try:
        result = cnx.execute(text("SELECT * from RECHERCHEMATERIELS;"))
        info_rechercheMateriel = []
        for row in result:
            info_rechercheMateriel.append(row[0])
        return  info_rechercheMateriel
    except:
        print("Erreur lors de la récupération des informations sur les commandes :", str(e))
        raise
