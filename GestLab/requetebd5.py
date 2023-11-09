import random
import string
import pyotp
from sqlalchemy import text
from .connexionPythonSQL import *
from hashlib import sha256
import random
import string
from .models import *
import json
import smtplib
from email.message import EmailMessage
import qrcode

cnx = ouvrir_connexion()

def get_cnx():
    return cnx

def get_id_utilisateur_from_email(cnx, email) :
    try:
        result = cnx.execute(text("SELECT idUtilisateur FROM UTILISATEUR WHERE email = '" + email + "';"))
        for row in result:
            return row[0]
    except:
        print("Erreur lors de la récupération de l'id de l'utilisateur")
        raise
    
def ajout_gest_into_boncommande(cnx,id):
    try:
        etat = 1
        cnx.execute(text("insert into BONCOMMANDETEST (idEtat,idUtilisateur ) values (" + str(etat) + ", " + str(id) + ");"))
        cnx.commit()
        print("bon de commande ajouté")
    except:
        print("erreur d'ajout du bon de commande")
        raise
    
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
def insere_materiel(cnx, idCategorie, nomMateriel, referenceMateriel, caracteristiquesComplementaires, informationsComplementairesEtSecurite, seuilAlerte):
    try:
        if seuilAlerte == '' :
            seuilAlerte = "NULL"
        cnx.execute(text("insert into MATERIEL (idCategorie, nomMateriel, referenceMateriel, caracteristiquesComplementaires, informationsComplementairesEtSecurite, seuilAlerte) values (" + idCategorie + ", '" + nomMateriel + "', '" + referenceMateriel + "', '" + caracteristiquesComplementaires + "', '" + informationsComplementairesEtSecurite + "',  "+ str(seuilAlerte) + ");"))
        cnx.commit()
        return True
    except sqlalchemy.exc.OperationalError as e:
        print(f"SQL OperationalError: {e}")
        return False
    except sqlalchemy.exc.IntegrityError as e:
        print(f"SQL IntegrityError: {e}")
        return False

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

def get_uri_with_email(cnx, email):
    result = cnx.execute(text("select uri from 2FA where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]
    
def get_id_with_email(cnx, email):
    result = cnx.execute(text("select idUtilisateur from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]

def random_key():
    return pyotp.random_base32()

def add_two_authenticator_in_bd(cnx,key, email, id):
    try:
        if id != None:
            cnx.execute(text("insert into 2FA (email,uri,idUtilisateur) values ('" + email + "', '" + key + "', '" + str(id) + "');"))
            cnx.commit()
            print("uri ajouté")
        else:
            print("id non trouvé")
    except:
        print("erreur d'ajout de l'uri")
        raise

def create_uri(key,email):
    cnx = get_cnx()
    add_two_authenticator_in_bd(cnx,key ,email,get_id_with_email(cnx, email) )
    return pyotp.totp.TOTP(key).provisioning_uri(name= email, issuer_name= "GestLab")

def create_qr_code_utilisateur_deja_existant(cnx,email):
    uri = get_uri_with_email(cnx,email)
    qrcode.make(uri).save("qrcode.png")

def create_qr_code_nouvel_utlisateur(email, mdp):
    key = random_key()
    uri = create_uri(key,email)
    qrcode.make(uri).save("qrcode.png")
    envoyer_mail(email,mdp, key)

def random_key():
    return pyotp.random_base32()

def verify(key, code):
    return pyotp.TOTP(key).verify(code)


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
        create_qr_code_nouvel_utlisateur(email, mdpRandom)
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
        create_qr_code_nouvel_utlisateur(email, mdpRandom)
        id = get_id_with_email(cnx, email)
        ajout_gest_into_boncommande(cnx,id)
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
        create_qr_code_nouvel_utlisateur(email, mdpRandom)
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
        create_qr_code_nouvel_utlisateur(email, mdpRandom)
        print("utilisateur ajouté")
        return True
    except:
        print("erreur d'ajout de l'utilisateur")
        return False

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

def update_email_utilisateur(cnx,new_email,nom,mdp, old_email):
    try:

        update_email_utilisateur_in_ut(cnx, new_email, nom, mdp)
        update_email_utilisateur_in_2fa(cnx, old_email,new_email)
        print("email mis a jour")
        return True
    except:
        print("erreur de mise a jour de l'email")
        return False


def update_email_utilisateur_in_ut(cnx, new_email, nom, mdp):
    try:
        mdp_hash = hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("email mis a jour")
        return True
    except:
        print("erreur de mise a jour de l'email")
        return False

def update_email_utilisateur_in_2fa(cnx, old_email,new_email,):
    try:
        cnx.execute(text("update 2FA set email = '" + new_email + "' where email = '" + old_email + "';"))
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

def get_all_information_to_MaterielUnique_with_id(cnx, id):
    try:
        list = []
        result = cnx.execute(text("select * from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
        for row in result:
            print(row)
            list.append(row)
        return list, len(list)
    except:
        print("erreur de l'id")
        raise

def get_nb_materiel_to_MaterielUnique_with_id(cnx, id):
    try:
        result = cnx.execute(text("select count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
        for row in result:
            return row[0]
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



def get_all_information_to_Materiel_suggestions(cnx):
    try:
        list = []
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie, nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,pictogramme,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock, 0  from MATERIEL natural left join STOCKLABORATOIRE NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL LEFT JOIN RISQUES NATURAL LEFT JOIN RISQUE ;"))
        for row in result:
            id = row[0]
            result_count = cnx.execute(text("select idMateriel, count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
            for row_count in result_count:
                print((row_count[1]))
                list.append((row,row_count[1]))
        return list, len(list)
    except:
        print("erreur de l'id")
        raise

def get_all_information_to_Materiel(cnx):
    try:
        list = []
        result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,pictogramme,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL JOIN RISQUES NATURAL JOIN RISQUE ;"))
        for row in result:
            id = row[0]
            result_count = cnx.execute(text("select idMateriel, count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
            for row_count in result_count:
                print((row_count[1]))
                list.append((row,row_count[1]))
        return list, len(list)
    except:
        print("erreur de l'id")
        raise

def nb_alert_par_materiel_dict(cnx):
    try:
        dict = {}
        result = cnx.execute(text("select idMateriel,idMaterielUnique from ALERTESENCOURS natural join MATERIELUNIQUE;"))
        for row in result:
            if row[0] in dict:
                dict[row[0]] += 1
            else:
                dict[row[0]] = 1

        print(dict)
        return dict
    except: 
        raise

def nb_alert_par_materielUnique_dict(cnx):
    try:
        dict = {}
        result = cnx.execute(text("select idMaterielUnique,idMaterielUnique from ALERTESENCOURS natural join MATERIELUNIQUE;"))
        for row in result:
            if row[0] in dict:
                dict[row[0]] += 1
            else:
                dict[row[0]] = 1

        print(dict)
        return dict
    except: 
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

# get_info_demande(cnx)


# def get_domaine(cnx):
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
        result = cnx.execute(text("SELECT * from DOMAINE;"))
        info_commande = []
        for row in result:
            info_commande.append(row)
        return  info_commande
    except Exception as e:
        print("Erreur lors de la récupération des informations sur les commandes :", str(e))
        raise

# get_info_demande(cnx)

def get_info_demande_with_id(cnx, idDemande):
    try:
        result = cnx.execute(text("SELECT nom, prenom, quantite, nomMateriel, idMateriel, referenceMateriel, idBonCommande from UTILISATEUR natural join DEMANDE natural join AJOUTERMATERIEL natural join MATERIEL natural join BONCOMMANDE where idDemande =" + str(idDemande) + ";"))
        info_demande = []
        for row in result:
            info_demande.append(row)
        return info_demande
    except Exception as e:
        print("Erreur lors de la récupération des informations sur les commandes :", str(e))
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
        envoyer_mail_mdp_oublie(email, mdpRandom)
        print("mdp mis a jour")
        return True
    except:
        print("erreur de mise a jour du mdp")
        return False


def get_info_rechercheMateriel(cnx):
    try:
        result =  cnx.execute(text("select * from RECHERCHEMATERIELS;"))
        list = []
        for row in result:
            list.append(row[0])
        return list
    except Exception as e:
        print("Erreur lors de la récupération des informations sur les commandes :", str(e))
        raise


def get_materiel(cnx, idMateriel) :
    try:
        materiel = []
        result = cnx.execute(text("SELECT * FROM MATERIEL WHERE idMateriel = " + str(idMateriel) + ";"))
        for row in result:
            materiel.append(row)
        return materiel
    except:
        print("Erreur lors de la récupération du matériel")
        raise

def modifie_materiel(cnx, idMateriel, categorie, nom, reference, caracteristiques, infossup, seuilalerte) :
    try:
        if seuilalerte is None or seuilalerte == "None" :
            seuilalerte = "NULL"
        cnx.execute(text("UPDATE MATERIEL SET idCategorie = " + str(categorie) + ", nomMateriel = '" + nom + "', referenceMateriel = '" + reference + "', caracteristiquesComplementaires = '" + caracteristiques + "', informationsComplementairesEtSecurite = '" + infossup + "', seuilAlerte = " + str(seuilalerte) + " WHERE idMateriel = " + str(idMateriel) + ";"))     
        cnx.commit()
    except:
        print("Erreur lors de la modification du matériel")
        raise

def get_id_domaine_from_categorie(cnx, id_categorie) :
    try:
        result = cnx.execute(text("SELECT idDomaine FROM CATEGORIE WHERE idCategorie = " + str(id_categorie) + ";"))
        for row in result:
            return row[0]
    except:
        print("Erreur lors de la récupération du domaine")
        raise

def get_id_materiel_from_id_materiel_unique(cnx, id_materiel_unique) :
    try:
        result = cnx.execute(text("SELECT idMateriel FROM MATERIELUNIQUE NATURAL JOIN MATERIEL WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
        for row in result:
            return row[0]
    except:
        print("Erreur lors de la récupération de l'id du matériel")
        raise

def supprimer_materiel_unique_bdd(cnx, id_materiel_unique) :
    try :
        cnx.execute(text("DELETE FROM ALERTESENCOURS WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
        cnx.execute(text("DELETE FROM RESERVELABORATOIRE WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
        cnx.execute(text("DELETE FROM MATERIELUNIQUE WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
        cnx.commit()
    except:
        print("Erreur lors de la suppression du matériel unique")
        raise
    

def get_id_bonCommande_actuel(cnx, idut):
    try:
        result = cnx.execute(text("SELECT idBonCommande FROM BONCOMMANDETEST WHERE idUtilisateur = " + str(idut) + " AND idEtat = 1;")) #enlever  AND idEtat = 1 si on delete le bon de commande validée
        for row in result:
            return row[0]
    except:
        print("Erreur lors de la récupération de l'id du bon de commande")
        raise


#faire trigger before insert pour que si on ajoute un materiel deja dans la commande, on update la quantite
def ajout_materiel_in_commandeTest(cnx, idmat, idut, quantite):
    try:
        idbc = get_id_bonCommande_actuel(cnx, idut)
        result = cnx.execute(text("select idMateriel from COMMANDETEST where idBonCommande = " + str(idbc)+ ";"))
        query = text("INSERT INTO COMMANDETEST (idBonCommande, idMateriel, quantite) VALUES (" + str(idbc) + ", " + str(idmat) + ", " + str(quantite) + ");")
        for mat in result:
            print(int(mat[0]) == int(idmat))
            if int(mat[0]) == int(idmat) :
                if int(quantite) == 0 :
                    query = text("DELETE FROM COMMANDETEST WHERE idBonCommande = " + str(idbc) + " AND idMateriel = " + str(idmat) + ";")
                else :
                    query = text("UPDATE COMMANDETEST SET quantite = " + str(quantite) + " WHERE idBonCommande = " + str(idbc) + " AND idMateriel = " + str(idmat) + ";")
        cnx.execute(query)
        cnx.commit()
    except:
        print("Erreur lors de l'ajout du matériel dans la commande")
        raise
    
def get_materiel_in_bonDeCommande(cnx,idut):
    try:
        idbc = get_id_bonCommande_actuel(cnx, idut)
        result = cnx.execute(text("SELECT idMateriel, nomMateriel,referenceMateriel, quantite FROM COMMANDETEST NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
        liste = []
        for row in result:
            liste.append(row)
        return liste
    except:
        print("Erreur lors de la récupération du matériel dans la commande")
        raise
    

def delete_all_materiel_in_commande(cnx, idut):
    try:
        idbc = get_id_bonCommande_actuel(cnx, idut)
        cnx.execute(text("DELETE FROM COMMANDETEST WHERE idBonCommande = " + str(idbc) + ";"))
        cnx.commit()
    except:
        print("Erreur lors de la suppression du matériel dans la commande")
        raise

def changer_etat_bonCommande(cnx, idut):
    try:
        idetat = 2
        idbc = get_id_bonCommande_actuel(cnx, idut)
        cnx.execute(text("UPDATE BONCOMMANDETEST SET idEtat = " + str(idetat) + " WHERE idBonCommande = " + str(idbc) + ";"))
        cnx.commit()
        ajout_gest_into_boncommande(cnx,idut)
    except:
        print("Erreur lors du changement d'état du bon de commande")
        raise
    

def afficher_table(cnx, table):
    try:
        list = []
        result = cnx.execute(text("SELECT * FROM " + table + ";"))
        for row in result:
            list.append(row)
        return list
    except:
        print("Erreur lors de l'affichage de la table")
        raise


def get_materiel_commande(cnx,idbc):
    try:
        result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, informationsComplementairesEtSecurite,referenceMateriel, idFDS, idBonCommande,quantite FROM COMMANDETEST NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
        liste = []
        for row in result:
            print(row)
            liste.append(row)
        return liste
    except:
        print("Erreur lors de la récupération du matériel dans la commande")
        raise

def delete_materiel_in_BonCommande_whith_id(cnx, idMateriel, idbc):
    try:
        cnx.execute(text("DELETE FROM COMMANDETEST WHERE idMateriel = " + str(idMateriel) + " AND idBonCommande = " + str(idbc) + ";"))
        cnx.commit()
    except:
        print("Erreur lors de la suppression du matériel dans la commande")
        raise
        

def recherche_materiel_commander_search(cnx, search):
    try:
        list = []
        result = cnx.execute(text("select idMateriel,nomMateriel,referenceMateriel,idFDS,idFDS,seuilAlerte,caracteristiquesComplementaires,caracteristiquesComplementaires from MATERIEL where nomMateriel like '%" + search + "%' ;"))
        result1 = cnx.execute(text("select idMateriel,nomMateriel,referenceMateriel,idFDS,idFDS,seuilAlerte,caracteristiquesComplementaires,caracteristiquesComplementaires from MATERIEL where referenceMateriel like '%" + search + "%' ;"))
        for row in result:
            print(row)
            list.append(row)
        for row in result1:
            print(row)
            list.append(row)
        return list
    except:
        print("erreur de recherche")
        raise


def afficher_bon_commande(cnx, idut):
    try:
        idbc = get_id_bonCommande_actuel(cnx, idut)
        result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite FROM COMMANDETEST NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
        result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM COMMANDETEST NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ");"))
        liste = []
        for row in result:
            print(row)
            liste.append(row)
        for row in result2:
            print(row)
            liste.append(row)
        return liste
    except:
        print("Erreur lors de l'affichage de la table")
        raise