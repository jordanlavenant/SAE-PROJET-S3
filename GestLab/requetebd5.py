import random
import string
from numpy import split
from sqlalchemy import text
from .connexionPythonSQL import *
from hashlib import sha256
from datetime import datetime, timedelta
import random
import string
from .models import *



cnx = ouvrir_connexion()

def get_cnx():
    return cnx

#marche BD 5
def get_nom_dom_cat_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select nomDomaine,nomCategorie from MATERIEL natural join DOMAINE natural join CATEGORIE where idMateriel = " + str(id) + ";"))
        result = result.first()
        return result
    except:
        print("erreur de l'id")
        raise
    
#marche BD 5
def ajoute_materiel(cnx, reFerenceMateriel, nomMateriel, idCategorie, seuilAlerte, caracteristiquesComplementaires,informationsComplementairesEtSecurite):
    try:
        cnx.execute(text("insert into MATERIEL (reFerenceMateriel, idFDS, nomMateriel, idCategorie, seuilAlerte, caracteristiquesComplementaires,informationsComplementairesEtSecurite ) values ('" + reFerenceMateriel + "', 1, '" + nomMateriel + "', '" + str(idCategorie) + "', '" + str(seuilAlerte) + "', '" + caracteristiquesComplementaires + "', '" + informationsComplementairesEtSecurite + "');"))
        cnx.commit()
        print("materiel ajouté")
    except:
        print("erreur d'ajout du materiel")
        raise


#marche BD 5
# est ce que pour ajouter du materiel on est obliger de passer par materiel unique ?

# def ajout_quantite_with_id(cnx, idMateriel, quantite):
#     try:
#         cnx.execute(text("insert into STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) values (" + str(idMateriel) + ", " + str(quantite) + ");"))
#         cnx.commit()
#         print("quantite ajouté dans un nouveau STOCKLABORATOIRE")
#     except:
#         print("id deja utiliser")
#         try:
#             cnx.execute(text("update STOCKLABORATOIRE set quantiteLaboratoire = quantiteLaboratoire + " + str(quantite) + " where idMateriel = " + str(idMateriel) +";"))
#             cnx.commit()
#             print("quantite ajouté")
#         except:
#             print("erreur d'ajout de la quantité")
#             raise


#marche BD 5
def ajout_fournisseur(cnx, nom, adresse,mail, tel):
    try:
        cnx.execute(text( "insert into FOURNISSEUR (nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values ('" + nom + "', '" + adresse + "', '" + mail + "', '" + tel + "');"))
        cnx.commit()
        print("fournisseur ajouté")
    except:
        print("erreur d'ajout du fournisseur")
        raise

#marche BD 5
def generer_mot_de_passe():
    caracteres = string.ascii_letters + string.digits
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

    return mot_de_passe

#marche BD 5
def hasher_mdp(mdp):
    m = sha256()
    m.update(mdp.encode("utf-8"))
    return m.hexdigest()

#marche BD 5
def ajout_professeur(cnx, nom, prenom, email):
    try:
        idStatut = 2
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
        cnx.commit()
        envoyer_mail_nouveau_compte(email, mdpRandom)
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False

#marche BD 5
def ajout_gestionnaire(cnx, nom, prenom, email):
    
    try:
        idStatut = 4
        mdpRandom = generer_mot_de_passe()
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
        cnx.commit()
        envoyer_mail_nouveau_compte(email, mdpRandom)
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False
    
def ajout_administrateur(cnx, nom, prenom, email):
    try:
        idStatut = 1
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
        cnx.commit()
        envoyer_mail_nouveau_compte(email, mdpRandom)
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False


def ajout_laborantin(cnx, nom, prenom, email):
    
    try:
        idStatut = 3
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
        cnx.commit()
        envoyer_mail_nouveau_compte(email, mdpRandom)
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False

#marche BD 5
def get_nom_whith_email(cnx, email):
    result = cnx.execute(text("select nom from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]

#marche BD 5
def get_MATERIEL(cnx):
    result = cnx.execute(text("select * from RECHERCHEMATERIELS;"))
    for row in result:
        print(row[0])

#marche BD 5
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


# le trigger  "emailUtilisateurUniqueUpdate" bloque les updates vers Utilisateur comme si dessous >>> voir Anna

#marche BD 5
def modification_droit_utilisateur(cnx, idut, idSt):
    try:
        cnx.execute(text(  "update UTILISATEUR set idStatut = '" + str(idSt) + "' where idUtilisateur = '" + str(idut) + "';"))
        cnx.commit()
        print("droit mis a jour")
    except:
        print("erreur de mise a jour du droit")
        raise

#marche BD 5
def get_password_with_email(cnx, email):
    result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        return row[0]
    
#marche BD 5
def update_mdp_utilisateur(cnx, email,mdp, new_mdp):
    try:
        init_mdp = hasher_mdp(mdp)
        new_mdp_hash = hasher_mdp(new_mdp)
        mdp_get = get_password_with_email(cnx, email)
        if mdp_get != init_mdp:
            print("mdp incorrect")
            return False
        else:
            cnx.execute(text("update UTILISATEUR set motDePasse = '" + new_mdp_hash + "' where email = '" + email + "' and motDePasse = '" + init_mdp + "'"))
            cnx.commit()
            print("mdp mis a jour")
            return True
    except:
        print("erreur de mise a jour du mdp")
        return None        

#marche BD 5
def update_nom_utilisateur(cnx, email, new_nom):
    try:
        cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "';"))
        cnx.commit()
        print("nom mis a jour")
    except:
        print("erreur de mise a jour du nom")
        raise

#marche BD 5
def update_prenom_utilisateur(cnx, email, new_prenom):
    try:
        cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "';"))
        cnx.commit()
        print("prenom mis a jour")
    except:
        print("erreur de mise a jour du prenom")
        raise


#marche BD 5
def get_nom_and_statut_and_email(cnx, email):
    result = cnx.execute(text("select nom, idStatut from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0], row[1])
        return (row[0], row[1], email)

#marche BD 5
def get_user_with_statut(cnx, nomStatut):
    liste = []
    result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where nomStatut = '" + str(nomStatut) + "';"))
    for row in result:
        liste.append((row[4]))
    return liste

#marche BD 5
def get_all_user(cnx, idStatut=None):
    liste = []
    if idStatut is None:
        result = cnx.execute(text("select * from UTILISATEUR where idStatut != 1;"))
    else:
        result = cnx.execute(text("select * from UTILISATEUR where idStatut = '" + str(idStatut) + "';"))
    for row in result:
        liste.append((row[1],row[0],row[2],row[3],row[4]))
    return (liste, len(liste))

# def get_all_information_to_Materiel(cnx, nomcat=None):
#     my_list = []
#     if nomcat is None:
#         result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire  from MATERIEL natural left join MATERIELUNIQUE natural left join STOCKLABORATOIRE  natural left join DOMAINE natural left join CATEGORIE natural join FDS;"))
#         for row in result:
#             print(row[1],row[2],row[6])
#             my_list.append((row[1],row[2],row[6]))
#     else:
#         result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire  from MATERIEL natural left join STOCKLABORATOIRE  natural left join DOMAINE natural left join CATEGORIE natural join FDS where nomCategorie = '" + nomcat + "';"))
#         for row in result:
#             my_list.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
#     return my_list


#marhce BD 5
def get_categories(cnx):
    liste = []
    result = cnx.execute(text("select * from CATEGORIE;"))
    for row in result:
        liste.append((row[0],row[2],row[1]))
    return liste

def get_nb_alert(cnx):
    try:
        cpt = 0
        result = cnx.execute(text("SELECT * FROM ALERTESENCOURS"))
        for _ in result:
            cpt += 1
        return cpt
    except Exception as e:
        print("Erreur lors de la récupération du nombre d'alertes :", str(e))
        raise

def get_nb_alert_id(cnx):
    try:
        list = []
        result = cnx.execute(text("SELECT * FROM ALERTESENCOURS natural join TYPESALERTES"))
        for row in result:
            list.append((row))
        print(list)
        return list
    except Exception as e:
        print("Erreur lors de la récupération du nombre d'alertes :", str(e))
        raise

#marche BD 5
def get_all_information_to_Materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,pictogramme,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL LEFT JOIN RISQUES NATURAL LEFT JOIN RISQUE WHERE idMateriel = " + str(id) + ";"))
        for row in result:
            return row
    except:
        print("erreur de l'id")
        raise

def get_info_materiel_alert(cnx):
    try:
        list = []
        result = cnx.execute(text("select * from MATERIEL natural join MATERIELUNIQUE natural join ALERTESENCOURS;"))    
        for row in result: 
            list.append((row))
        print(list)
        return list
    except Exception as e:
        print("Erreur lors de la récupération du nombre d'alertes :", str(e))
        raise

def get_nb_demande(cnx):
    try:
        result = cnx.execute(text("select nombreDemandesEnAttente();"))
        for row in result:
            return row[0]
    except Exception as e:
        print("Erreur lors de la récupération du nombre de demandes :", str(e))
        raise

get_nb_demande(cnx)

#marhce BD 5
def get_all_information_utilisateur_with_id(cnx,id):
    try:
        result = cnx.execute(text("select nom,prenom,email,nomStatut from UTILISATEUR natural join STATUT where idUtilisateur = " + str(id) + ";"))
        for row in result:
            print(row)
            return row
    except:
        print("erreur de l'id")
        raise



def get_all_information_to_Materiel(cnx):
    try:
        list = []
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,pictogramme,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL LEFT JOIN RISQUES NATURAL LEFT JOIN RISQUE ;"))
        for row in result:
            print(row)
            list.append(row)
        return list
    except:
        print("erreur de l'id")
        raise

#marche BD 5
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

#marche BD 5
def update_all_information_utillisateur_with_id(cnx,id,idStatut,nom,prenom,email):
    try:
        cnx.execute(text("update UTILISATEUR set idStatut = '" + str(idStatut) + "', nom = '" + nom + "', prenom = '" + prenom + "', email = '" + email + "' where idUtilisateur = '" + str(id) + "';"))
        cnx.commit()
        print("utilisateur mis a jour")
        return True
    except:
        print("erreur de l'id")
        return False
    


#marche BD 5
def recherche_all_in_utilisateur_with_search(cnx, search):
    try:
        list = []
        result = cnx.execute(text("select * from UTILISATEUR where nom like '%" + search + "%'" or " prenom like '%" + search + "%' ;"))
        for row in result:
            print(row)
            list.append(row)
        return (list, len(list))
    except:
        print("erreur de recherche")
        raise

#marche BD 5
def recherche_all_in_materiel_with_search(cnx, search):
    try:
        list = []
        result = cnx.execute(text("select idMateriel,nomMateriel,referenceMateriel,idFDS,idFDS,seuilAlerte,caracteristiquesComplementaires,caracteristiquesComplementaires from MATERIEL where nomMateriel like '%" + search + "%' ;"))
        for row in result:
            print(row)
            list.append(row)
        return list
    except:
        print("erreur de recherche")
        raise


def get_all_info_from_domaine(cnx):
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

# def get_info_demande(cnx):
#     try:
#         result = cnx.execute(text("SELECT idDemande, nom, prenom, idBonCommande from UTILISATEUR natural join DEMANDE, natural join BONCOMMANDE;"))
#         info_commande = []
#         for row in result:
#             info_commande.append(row)
#         return  info_commande
#     except Exception as e:
#         print("Erreur lors de la récupération des informations sur les commandes :", str(e))
#         raise

# get_info_demande(cnx)


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


def get_all_user(cnx, idStatut=None):
    liste = []
    if idStatut is None:
        result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where idStatut != 1;"))
    else:
        result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where idStatut = '" + str(idStatut) + "';"))
    for row in result:
        print(row)
        liste.append((row[1],row[0],row[2],row[3],row[4]))
    return (liste, len(liste))


def recuperation_de_mot_de_passe(cnx, email):
    try:
        mdpRandom = generer_mot_de_passe()
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("update UTILISATEUR set motDePasse = '" + mdphash + "' where email = '" + email + "';"))
        cnx.commit()
        print("mdp mis a jour")
        return True
    except:
        print("erreur de mise a jour du mdp")
        return False
