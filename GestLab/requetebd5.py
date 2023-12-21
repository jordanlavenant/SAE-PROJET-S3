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
from datetime import datetime

cnx = ouvrir_connexion()

def get_cnx():
    return cnx

class Table:
    
    class Get:
        
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

class Utilisateur:
    
    class Get :

        def get_nom_whith_email(cnx, email):
            result = cnx.execute(text("select nom from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                print(row[0])
            return row[0]

        def get_id_utilisateur_from_email(cnx, email) :
            try:
                result = cnx.execute(text("SELECT idUtilisateur FROM UTILISATEUR WHERE email = '" + email + "';"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de l'utilisateur")
                raise

        def get_password_with_email(cnx, email):
            result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                return row[0]
            
        def get_nom_and_statut_and_email(cnx, email):
            result = cnx.execute(text("select nom, idStatut, prenom from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                print(row[0], row[1], row[2], email)
                return (row[0], row[1], email, row[2])

 
        def get_user_with_statut(cnx, nomStatut):
            liste = []
            result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where nomStatut = '" + str(nomStatut) + "';"))
            for row in result:
                liste.append((row[4]))
            return liste

         
        def get_all_user(cnx, idStatut=None):
            liste = []
            if idStatut is None:
                result = cnx.execute(text("select * from UTILISATEUR where idStatut != 1;"))
            else:
                result = cnx.execute(text("select * from UTILISATEUR where idStatut = '" + str(idStatut) + "';"))
            for row in result:
                liste.append((row[1],row[0],row[2],row[3],row[4]))
            return (liste, len(liste))
        
        def get_uri_with_email(cnx, email):
            result = cnx.execute(text("select uri from 2FA where email = '" + email + "';"))
            for row in result:
                print(row[0])
                return row[0]
            
        def get_id_with_email(cnx, email):
            result = cnx.execute(text("select idUtilisateur from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                return row[0]
            
        def get_all_information_utilisateur_with_id(cnx,id):
            try:
                result = cnx.execute(text("select nom,prenom,email,nomStatut from UTILISATEUR natural join STATUT where idUtilisateur = " + str(id) + ";"))
                for row in result:
                    return row
            except:
                print("erreur de l'id")
                raise
           
    class Update:
        
        def update_email_utilisateur(cnx,new_email,nom,mdp, old_email):
            try:

                Utilisateur.Update.update_email_utilisateur_in_ut(cnx, new_email, nom, mdp)
                Utilisateur.Update.update_email_utilisateur_in_2fa(cnx, old_email,new_email)
                print("email mis a jour")
                return True
            except:
                print("erreur de mise a jour de l'email")
                return False


        def update_email_utilisateur_in_ut(cnx, new_email, nom, mdp):
            try:
                mdp_hash = Mots_de_passe.hasher_mdp(mdp)
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

         
        def modification_droit_utilisateur(cnx, idut, idSt):
            try:


                bonCommande = cnx.execute(text("select idBonCommande from BONCOMMANDE where idUtilisateur = '" + str(idut) + "' and idEtat = 1;"))
                for row in bonCommande:
                    cnx.execute(text("delete from COMMANDE where idBonCommande = '" + str(row[0]) + "';"))
                    Bon_commande.Delete.delete_bonCommande_with_id(cnx,row[0])
                    print("bon de commande supprimé")

                demande = cnx.execute(text("select idDemande from DEMANDE where idUtilisateur = '" + str(idut) + "' and idEtatD = 1;"))
                for row in demande:
                    cnx.execute(text("delete from AJOUTERMATERIEL where idDemande = '" + str(row[0]) + "';"))
                    Demande.Delete.delete_demande(cnx,row[0])
                    print("demande supprimé")


                cnx.execute(text("update UTILISATEUR set idStatut = '" + str(idSt) + "' where idUtilisateur = '" + str(idut) + "';"))
                cnx.commit()


                if idSt == 3 :
                    Utilisateur.Insert.ajout_laborantin_into_demande(cnx,idut)
                if idSt == 4 :
                    Utilisateur.Insert.ajout_gest_into_boncommande(cnx,idut)

                print("droit mis a jour")
            except:
                print("erreur de mise a jour du droit")
                raise

        def update_mdp_utilisateur(cnx, email,mdp, new_mdp):
            try:
                init_mdp = Mots_de_passe.hasher_mdp(mdp)
                new_mdp_hash = Mots_de_passe.hasher_mdp(new_mdp)
                mdp_get = Utilisateur.Get.get_password_with_email(cnx, email)
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

         
        def update_nom_utilisateur(cnx, email, new_nom):
            try:
                cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "';"))
                cnx.commit()
                print("nom mis a jour")
            except:
                print("erreur de mise a jour du nom")
                raise

         
        def update_prenom_utilisateur(cnx, email, new_prenom):
            try:
                cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "';"))
                cnx.commit()
                print("prenom mis a jour")
            except:
                print("erreur de mise a jour du prenom")
                raise

        def update_all_information_utillisateur_with_id(cnx,id,idStatut,nom,prenom,email):
            try:
                cnx.execute(text("update UTILISATEUR set nom = '" + nom + "', prenom = '" + prenom + "', email = '" + email + "' where idUtilisateur = '" + str(id) + "';"))
                cnx.commit()
                Utilisateur.Update.modification_droit_utilisateur(cnx, id, idStatut)
                print("utilisateur mis a jour")
                return True
            except:
                print("erreur de l'id")
                return False
            
    class Insert:

        def ajout_fournisseur(cnx, nom, adresse,mail, tel):
            try:
                cnx.execute(text( "insert into FOURNISSEUR (nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values ('" + nom + "', '" + adresse + "', '" + mail + "', '" + tel + "');"))
                cnx.commit()
                print("fournisseur ajouté")
            except:
                print("erreur d'ajout du fournisseur")
                raise

        
        def ajout_gest_into_boncommande(cnx, id):
            try:
                etat = 1
                date = DATE.Get.get_date(cnx)
                
                # Insérer la date convertie en string dans le format SQL approprié (YYYY-MM-DD)
                cnx.execute(text("INSERT INTO BONCOMMANDE (idEtat, idUtilisateur, dateBonCommande) VALUES (" + str(etat) + ", " + str(id) + ", '" + str(date) + "');"))
                
                cnx.commit()
                print("Bon de commande ajouté")
            except Exception as e:
                print("Erreur d'ajout du bon de commande :", str(e))
                raise

        def ajout_laborantin_into_demande(cnx, idut):
            try:
                etat = 1
                cnx.execute(text("INSERT INTO DEMANDE (idUtilisateur, idEtatD) VALUES (" + str(idut) + ", " + str(etat) + ");")) 
                cnx.commit()
                print("Demande ajoutée")
            except:
                print("erreur d'ajout de la demande")
                raise
            
        def ajout_professeur(cnx, nom, prenom, email):
            try:
                idStatut = 2
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
                cnx.commit()
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False

        def ajout_gestionnaire(cnx, nom, prenom, email):
            
            try:
                idStatut = 4
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
                cnx.commit()
                id = Utilisateur.Get.get_id_with_email(cnx, email)
                Utilisateur.Insert.ajout_gest_into_boncommande(cnx,id)
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False  
        
        def ajout_administrateur(cnx, nom, prenom, email):
            try:
                idStatut = 1
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
                cnx.commit()
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False


        def ajout_laborantin(cnx, nom, prenom, email):
            
            try:
                idStatut = 3
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
                cnx.commit()
                id = Utilisateur.Get.get_id_with_email(cnx, email)
                Utilisateur.Insert.ajout_laborantin_into_demande(cnx,id)
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False
                
    class Delete:
            
            def delete_utilisateur(cnx, idut):
                try:
                    bonCommande = cnx.execute(text("select idBonCommande from BONCOMMANDE where idUtilisateur = '" + str(idut) + "';"))
                    for row in bonCommande:
                        cnx.execute(text("delete from COMMANDE where idBonCommande = '" + str(row[0]) + "';"))
                        
                    demande = cnx.execute(text("select idDemande from DEMANDE where idUtilisateur = '" + str(idut) + "';"))
                    for row in demande:
                        cnx.execute(text("delete from AJOUTERMATERIEL where idDemande = '" + str(row[0]) + "';"))
                    
                    cnx.execute(text("delete from DEMANDE where idUtilisateur = '" + str(idut) + "';"))
                    cnx.execute(text("delete from BONCOMMANDE where idUtilisateur = '" + str(idut) + "';"))
                    cnx.execute(text("delete from 2FA where idUtilisateur = '" + str(idut) + "';"))
                    cnx.execute(text("delete from UTILISATEUR where idUtilisateur = '" + str(idut) + "';"))
                    cnx.commit()
                    print("utilisateur supprimé")
                except:
                    print("erreur de suppression de l'utilisateur")
                    raise
    
            def delete_utilisateur_with_email(cnx, email):
                try:
                    cnx.execute(text("delete from UTILISATEUR where email = '" + email + "';"))
                    cnx.commit()
                    print("utilisateur supprimé")
                except:
                    print("erreur de suppression de l'utilisateur")
                    raise

    

class Materiel:
    
    class Get :

        def get_idMateriel_with_nomMateriel(cnx, nomMateriel):
            try:
                result = cnx.execute(text("SELECT idMateriel FROM MATERIEL WHERE nomMateriel = '" + nomMateriel + "';"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du matériel")
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

        def get_all_information_to_Materiel_with_id(cnx, id):
            try:
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL LEFT JOIN RISQUES NATURAL LEFT JOIN RISQUE WHERE idMateriel = " + str(id) + ";"))
                for row in result:
                    return row
            except:
                print("erreur de l'id")
                raise

        def get_all_information_to_Materiel(cnx):
            try:
                list = []
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,0,0,0,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE WHERE quantiteLaboratoire > 0 ;"))
                for row in result:
                    id = row[0]
                    result_count = cnx.execute(text("select idMateriel, count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE NATURAL JOIN RESERVELABORATOIRE where idMateriel =" + str(id) + ";"))
                    for row_count in result_count:
                        print((row_count[1]))
                        list.append((row,row_count[1]))
                return list, len(list)
            except:
                print("erreur de l'id")
                raise

        def get_materiels_existants(cnx):
            try:
                result = cnx.execute(text("SELECT idMateriel, nomMateriel FROM MATERIEL;"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération des matériels existants")
                raise


        def get_materiel_commande(cnx,idbc):
            try:
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, informationsComplementairesEtSecurite,referenceMateriel, idFDS, idBonCommande,quantite FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
                liste = []
                for row in result:
                    print(row)
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise

        def get_materiel_demande(cnx,idDemande):
            try:
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, informationsComplementairesEtSecurite,referenceMateriel, idFDS, idDemande,quantite FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                liste = []
                for row in result:
                    print(row)
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la demande")
                raise

        def get_id_materiel_from_id_materiel_unique(cnx, id_materiel_unique) :
            try:
                result = cnx.execute(text("SELECT idMateriel FROM MATERIELUNIQUE NATURAL JOIN MATERIEL WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du matériel")
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
            
        def get_all_materiel_for_pdf_in_bon_commande(cnx, idut):
            try:
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT nomMateriel, referenceMateriel, nomDomaine,nomCategorie, quantite from COMMANDE NATURAL JOIN MATERIEL NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE WHERE idBonCommande = " + str(idbc) + ";"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise

        def get_all_materiel_for_pdf_in_bon_commande_after(cnx, idbc):
            try:
                result = cnx.execute(text("SELECT nomMateriel, referenceMateriel, nomDomaine,nomCategorie, quantite from COMMANDE NATURAL JOIN MATERIEL NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE WHERE idBonCommande = " + str(idbc) + ";"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise
            
        def get_materiel_in_bonDeCommande(cnx,idut):
            try:
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT idMateriel, nomMateriel,referenceMateriel, quantite FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise
            
        def get_nom_dom_cat_materiel_with_id(cnx, id):
            try:
                result = cnx.execute(text("select nomDomaine,nomCategorie from MATERIEL natural join DOMAINE natural join CATEGORIE where idMateriel = " + str(id) + ";"))
                result = result.first()
                return result
            except:
                print("erreur de l'id")
                raise


    class Delete:

        def delete_materiel_in_BonCommande_whith_id(cnx, idMateriel, idbc):
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idMateriel = " + str(idMateriel) + " AND idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_materiel_in_AjouterMateriel_whith_id(cnx, idMateriel, idDemande):
            try:
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idMateriel = " + str(idMateriel) + " AND idDemande = " + str(idDemande) + ";"))
                result = cnx.execute(text("SELECT COUNT(*) FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) +  ";"))
                for row in result:
                    nbmat_in_demande = row[0]
                if nbmat_in_demande == 0:
                    Demande.Delete.delete_demande(cnx,idDemande)
                    print("Materiel & Demande supprimée")
                    cnx.commit()
                    return True
                print("Matériel supprimé")
                cnx.commit()
                return False
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_materiel(cnx, idMateriel):
            try:
                Materiel.Delete.delete_all_materiel_in_Stocklaboratoire_with_idMat(cnx, idMateriel)
                Materiel.Delete.delete_all_materiel_in_Commande_with_idMat(cnx, idMateriel)
                Materiel.Delete.delete_all_materiel_in_AjouterMateriel_with_idMat(cnx, idMateriel)
                MaterielUnique.Delete.delete_all_materiel_unique_with_idMateriel(cnx, idMateriel)
                cnx.execute(text("DELETE FROM MATERIEL WHERE idMateriel = " + str(idMateriel) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel")
                raise

        def delete_all_materiel_in_commande(cnx, idut):
            try:
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                cnx.execute(text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_all_materiel_in_AjouterMateriel(cnx, idut):
            try:
                idDemande = Demande.Get.get_id_demande_actuel(cnx, idut)
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_all_materiel_in_AjouterMateriel_with_idMat( cnx, idMat):
            try:
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idMateriel = " + str(idMat) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise
        
        def delete_all_materiel_in_Commande_with_idMat( cnx, idMat):
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idMateriel = " + str(idMat) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_all_materiel_in_Stocklaboratoire_with_idMat (cnx, idMat):
            try:
                cnx.execute(text("DELETE FROM STOCKLABORATOIRE WHERE idMateriel = " + str(idMat) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans le stock")
                raise
            

    class Update:

        def modifie_materiel(cnx, idMateriel, categorie, nom, reference, caracteristiques, infossup, seuilalerte):
            try:
                if seuilalerte is None or seuilalerte == "None":
                    seuilalerte = "NULL"

                query = (
                    "UPDATE MATERIEL SET idCategorie = {}, "
                    "nomMateriel = '{}', referenceMateriel = '{}', "
                    "caracteristiquesComplementaires = '{}', "
                    "informationsComplementairesEtSecurite = '{}', "
                    "seuilAlerte = {} WHERE idMateriel = {};".format(
                        categorie,
                        nom.replace("'", "''"),  # Properly escape single quotes
                        reference.replace("'", "''"),
                        caracteristiques.replace("'", "''"),
                        infossup.replace("'", "''"),
                        seuilalerte,
                        idMateriel,
                    )
                )

                cnx.execute(text(query))
                cnx.commit()
                return True
            except Exception as e:
                print("Erreur lors de la modification du matériel:", str(e))
                raise


        def set_all_quantite_from_ajouterMat_to_boncommande(cnx, idDemande,idut, boolajouterMat=False):
            try:
                result = cnx.execute(text("SELECT idMateriel,quantite from AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                for row in result:
                    Materiel.Insert.ajout_materiel_in_commande(cnx, row[0], idut, row[1], boolajouterMat)
                    MaterielUnique.Delete.delete_materiel_unique_in_demande(cnx, idDemande, row[0])
                
            except:
                print("Erreur lors de la mise à jour de la quantité dans la demande")
                raise
            



    class Insert: 

        def insere_materiel(
            cnx, idCategorie, nomMateriel, referenceMateriel,
            caracteristiquesComplementaires, informationsComplementairesEtSecurite, seuilAlerte
        ):
            try:
                if seuilAlerte == '':
                    seuilAlerte = "NULL"

                query = (
                    "INSERT INTO MATERIEL (idCategorie, nomMateriel, referenceMateriel, "
                    "caracteristiquesComplementaires, informationsComplementairesEtSecurite, seuilAlerte) "
                    "VALUES ({}, '{}', '{}', '{}', '{}', {});".format(
                        idCategorie,
                        nomMateriel.replace("'", "''"),  # Properly escape single quotes
                        referenceMateriel.replace("'", "''"),
                        caracteristiquesComplementaires.replace("'", "''"),
                        informationsComplementairesEtSecurite.replace("'", "''"),
                        seuilAlerte
                    )
                )

                cnx.execute(text(query))
                cnx.commit()
                return True
            except sqlalchemy.exc.OperationalError as e:
                print(f"SQL OperationalError: {e}")
                return False
            except sqlalchemy.exc.IntegrityError as e:
                print(f"SQL IntegrityError: {e}")
                return False


        def ajout_materiel_in_commande(cnx, idmat, idut, quantite, boolajouterMat):
            try:
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                result = cnx.execute(text("select idMateriel from COMMANDE where idBonCommande = " + str(idbc)+ ";"))
                if quantite != 0 :
                    query = text("INSERT INTO COMMANDE (idBonCommande, idMateriel, quantite) VALUES (" + str(idbc) + ", " + str(idmat) + ", " + str(quantite) + ");")
                    for mat in result:
                        if int(mat[0]) == int(idmat) :
                            if int(quantite) == 0 :
                                query = text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + " AND idMateriel = " + str(idmat) + ";")
                            else :
                                if boolajouterMat is False :
                                    query = text("UPDATE COMMANDE SET quantite = " + str(quantite) + " WHERE idBonCommande = " + str(idbc) + " AND idMateriel = " + str(idmat) + ";")
                                else:
                                    query = text("UPDATE COMMANDE SET quantite = quantite + " + str(quantite) + " WHERE idBonCommande = " + str(idbc) + " AND idMateriel = " + str(idmat) + ";")
                    cnx.execute(query)
                    cnx.commit()
                else:
                    cnx.execute(text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + " AND idMateriel = " + str(idmat) + ";"))
                    cnx.commit()
            except:
                print("Erreur lors de l'ajout du matériel dans la commande")
                raise

        def ajout_materiel_in_AjouterMateriel(cnx, idmat, idut, quantite, boolajouterMat):
            try:
                idDemande = Demande.Get.get_id_demande_actuel(cnx, idut)
                result = cnx.execute(text("select idMateriel from AJOUTERMATERIEL where idDemande = " + str(idDemande)+ ";"))
                if quantite != 0 :
                    query = text("INSERT INTO AJOUTERMATERIEL (idDemande, idMateriel, quantite) VALUES (" + str(idDemande) + ", " + str(idmat) + ", " + str(quantite) + ");")
                    for mat in result:
                        if int(mat[0]) == int(idmat) :
                            if int(quantite) == 0 :
                                query = text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idmat) + ";")
                            else :
                                if boolajouterMat is False :
                                    query = text("UPDATE AJOUTERMATERIEL SET quantite = " + str(quantite) + " WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idmat) + ";")
                                else:
                                    query = text("UPDATE AJOUTERMATERIEL SET quantite = quantite + " + str(quantite) + " WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idmat) + ";")
                    cnx.execute(query)
                    cnx.commit()
                else:
                    cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idmat) + ";"))
                    cnx.commit()
            except:
                print("Erreur lors de l'ajout du matériel dans la commande")
                raise
    
class MaterielUnique:
    
    class Get:
        
        def get_materiel_unique(cnx, idMaterielUnique) :
            try:
                materiel = []
                result = cnx.execute(text("SELECT * FROM MATERIELUNIQUE WHERE idMaterielUnique = " + str(idMaterielUnique) + " ;"))
                for row in result:
                    materiel.append(row)
                return materiel
            except:
                print("Erreur lors de la récupération du matériel unique")
                raise
    
        def get_nb_materiel_unique_in_demande(cnx, idDemande):
            try:
                result = cnx.execute(text("SELECT COUNT(*) FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) +  ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération du nombre de matériel unique dans la demande")
                raise
            
        def get_all_information_to_MaterielUnique_with_id(cnx, id):
            try:
                list = []
                result = cnx.execute(text("select * from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
                for row in result:
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

        def get_last_id(cnx) :
            try :
                result = cnx.execute(text("SELECT idMaterielUnique FROM MATERIELUNIQUE ORDER BY idMaterielUnique DESC LIMIT 1 ;"))
                for row in result:
                    return row[0]
            except :
                print("Erreur lors de la récupération du dernier id")

    class Delete:

        def delete_all_materiel_unique_with_idMateriel(cnx, id_materiel):
            try:
                cnx.execute(text("DELETE FROM ALERTESENCOURS WHERE idMaterielUnique IN (SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE idMateriel = " + str(id_materiel) + ");"))
                cnx.execute(text("DELETE FROM RESERVELABORATOIRE WHERE idMaterielUnique IN (SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE idMateriel = " + str(id_materiel) + ");"))
                cnx.execute(text("DELETE FROM MATERIELUNIQUE WHERE idMateriel = " + str(id_materiel) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression de tous les matériels uniques")
                raise

        def delete_materiel_unique_in_demande(cnx, idDemande, idMateriel):
            try:
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idMateriel) + ";"))
                cnx.commit()
                nbmat_in_demande = MaterielUnique.Get.get_nb_materiel_unique_in_demande(cnx, idDemande)
                if nbmat_in_demande == 0:
                    Demande.Delete.delete_demande(cnx,idDemande)
            except:
                print("Erreur lors de la suppression du matériel unique dans la demande")
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
            
            
    class Update:
        def modifie_materiel_unique(cnx, idMaterielUnique, idRangement, dateReception, datePeremption, commentaireMateriel, quantiteApproximative) :
            try:
                if datePeremption is None or datePeremption == 'None' or datePeremption == "" :
                    datePeremption = "NULL"
                else :
                    datePeremption = f"'{str(datePeremption)}'"
                
                query = (
                    "UPDATE MATERIELUNIQUE SET idRangement = {}, "
                    "dateReception = '{}', datePeremption = {}, "
                    "commentaireMateriel = '{}', "
                    "quantiteApproximative = {} "
                    "WHERE idMaterielUnique = {};".format(
                        idRangement,
                        dateReception,
                        datePeremption,
                        commentaireMateriel.replace("'", "''"),  # Properly escape single quotes
                        quantiteApproximative,
                        idMaterielUnique,
                    )
                )
                cnx.execute(text(query))
                cnx.commit()

            except:
                print("Erreur lors de la modification du matériel unique")
                raise

        
            
    class Insert:
                
        def insere_materiel_unique(cnx, id_materiel, position, date_reception, date_peremption, commentaire, quantite_approximative):
            try:
                if date_peremption is None or date_peremption == 'None' or date_peremption == "":
                    date_peremption = "NULL"
                else:
                    date_peremption = f"'{str(date_peremption)}'"

                dernier_id = MaterielUnique.Get.get_last_id(cnx) 
                nouvel_id = dernier_id + 1
                print("nouvel id" + str(nouvel_id))

                query = (
                    "INSERT INTO MATERIELUNIQUE (idMaterielUnique, idMateriel, idRangement, dateReception, datePeremption, "
                    "commentaireMateriel, quantiteApproximative) VALUES ('{}','{}', '{}', '{}', {}, '{}', {});".format(
                        nouvel_id,
                        id_materiel,
                        position,
                        str(date_reception),
                        date_peremption,
                        commentaire.replace("'", "''"),  # Properly escape single quotes
                        quantite_approximative
                    )
                )

                cnx.execute(text(query))
                cnx.commit()
                return nouvel_id
            except sqlalchemy.exc.OperationalError as e:
                print(f"SQL OperationalError: {e}")
                return -1
            except sqlalchemy.exc.IntegrityError as e:
                print(f"SQL IntegrityError: {e}")
                return -1




class Recherche:
    
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

    def recherche_all_in_utilisateur_with_search(cnx, search):
        try:
            list = []
            result = cnx.execute(text("select * from UTILISATEUR where idStatut != 1 and nom like '%" + search + "%'" or " prenom like '%" + search + "%' ;"))
            for row in result:
                print(row)
                list.append(row)
            return (list, len(list))
        except:
            print("erreur de recherche")
            raise

    
    def recherche_all_in_materiel_with_search(cnx, idbc, search):
        try:
            liste = []
            result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + " and nomMateriel like '%" + search + "%';"))
            result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ") and nomMateriel like '%" + search + "%';"))
            for row in result:
                    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            for row in result2:
                idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            return liste
        except:
            print("erreur de recherche")
            raise

    def recherche_all_in_materiel_demande_with_search(cnx, idDemande, search):
        try:
            liste = []
            result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idDemande) + " and nomMateriel like '%" + search + "%';"))
            result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idDemande) + ") and nomMateriel like '%" + search + "%';"))
            for row in result:
                    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            for row in result2:
                idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            return liste
        except:
            print("erreur de recherche")
            raise

    def recherche_all_in_inventaire(cnx):
            try:
                list = []
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE;"))
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

    def recherche_all_in_inventaire_with_search(cnx, search):
            try:
                list = []
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE where nomMateriel like '%" + search + "%' ;"))
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

class Mots_de_passe:
    
    def generer_mot_de_passe():
        caracteres = string.ascii_letters + string.digits
        mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

        return mot_de_passe

    
    def hasher_mdp(mdp):
        m = sha256()
        m.update(mdp.encode("utf-8"))
        return m.hexdigest()
    
    def recuperation_de_mot_de_passe(cnx, email):
        try:
            mdpRandom = Mots_de_passe.generer_mot_de_passe()
            print(mdpRandom)
            mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
            cnx.execute(text("update UTILISATEUR set motDePasse = '" + mdphash + "' where email = '" + email + "';"))
            cnx.commit()
            envoyer_mail_mdp_oublie(email, mdpRandom)
            print("mdp mis a jour")
            return True
        except:
            print("erreur de mise a jour du mdp")
            return False


class Authentification:
    
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
        Authentification.add_two_authenticator_in_bd(cnx,key ,email,Utilisateur.Get.get_id_with_email(cnx, email) )
        return pyotp.totp.TOTP(key).provisioning_uri(name= email, issuer_name= "GestLab")

    def create_qr_code_utilisateur_deja_existant(cnx,email):
        uri = Utilisateur.Get.get_uri_with_email(cnx,email)
        qrcode.make(uri).save("qrcode.png")

    def create_qr_code_nouvel_utlisateur(email, mdp):
        key = Authentification.random_key()
        uri = Authentification.create_uri(key,email)
        qrcode.make(uri).save("qrcode.png")
        envoyer_mail(email,mdp, key)

    def verify(key, code):
        return pyotp.TOTP(key).verify(code)


class Alert:
    
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


class Demande : 
    
    class Get:

        def get_id_demande_actuel(cnx, idut):
            try:
                result = cnx.execute(text("SELECT idDemande FROM DEMANDE WHERE idUtilisateur = " + str(idut) + " AND idEtatD = 1;"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de la demande")
                raise
        
        def get_nb_demande(cnx):
            try:
                result = cnx.execute(text("SELECT COUNT(DEMANDE.idDemande) FROM DEMANDE WHERE DEMANDE.idEtatD = 2;"))
                for row in result:
                    return row[0]
            except Exception as e:
                print("Erreur lors de la récupération du nombre de demandes :", str(e))
                raise
            
        def get_info_demande(cnx):
            try:         
                result = cnx.execute(text("SELECT idDemande, nom, prenom from UTILISATEUR natural join DEMANDE where idEtatD = 2;"))
                info_commande = []
                for row in result:
                    info_commande.append(row)
                return info_commande
            except Exception as e:
                print("Erreur lors de la récupération des informations sur les commandes :", str(e))
                raise
            
        def get_info_demande_with_id(cnx, idDemande):
            try:
                rowRes = []
                result = cnx.execute(text("SELECT nom, prenom, quantite, nomMateriel, idMateriel, referenceMateriel from UTILISATEUR natural join DEMANDE natural join AJOUTERMATERIEL natural join MATERIEL where idDemande =" + str(idDemande) + ";"))
                for row in result:
                    cpt = MaterielUnique.Get.get_nb_materiel_to_MaterielUnique_with_id(cnx, row[4])
                    print(cpt)
                    rowRes.append((row[0], row[1], row[2], row[3], row[4], row[5], cpt))
                return rowRes
            except Exception as e:
                print("Erreur lors de la récupération des informations sur les commandes :", str(e))
                raise

        def get_demande_with_statut(cnx, idetat):
            try:
                list = []
                result = cnx.execute(text("SELECT * FROM DEMANDE WHERE idEtatD = " + str(idetat) + ";"))
                for row in result:
                    list.append(row)
                return list
            except:
                print("Erreur lors de la récupération des commandes")
                raise

        def afficher_demande(cnx, idut): #get
            try:
                idD = Demande.Get.get_id_demande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idD) + ";"))
                result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idD) + ");"))
                liste = []
                for row in result:
                    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                for row in result2:
                    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                return liste
            except:
                print("Erreur lors de l'affichage de la table")
                raise

    class Update:
        def tout_commander_with_idDemmande_and_idUt (cnx, idDemande, idUt):
            try:
                result = cnx.execute(text("SELECT idMateriel, quantite FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                for row in result:
                    Materiel.Insert.ajout_materiel_in_commande(cnx, row[0], idUt, row[1], True)
                    Materiel.Delete.delete_materiel_in_AjouterMateriel_whith_id(cnx, row[0], idDemande)
                cnx.commit()  
            except:
                print("Erreur lors de la mise à jour de la quantité dans la demande")
                raise
        

    class Delete:
        
        def delete_demande(cnx,idDemande):
            try:
                print("test")
                cnx.execute(text("DELETE FROM DEMANDE WHERE idDemande = " + str(idDemande) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression de la demande")
                raise

        def delete_materiel_demande(cnx, idut, idMateriel):
            try:
                idDemande = Demande.Get.get_id_demande_actuel(cnx, idut)
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idMateriel) + ";"))        
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la demande")

                raise

    class Insert:

        def changer_etat_demande(cnx, idut):
            try:
                idDemande = Demande.Get.get_id_demande_actuel(cnx, idut)
                cnx.execute(text("UPDATE DEMANDE SET idEtatD = 2 WHERE idDemande = " + str(idDemande) + ";"))
                cnx.commit()
                Utilisateur.Insert.ajout_laborantin_into_demande(cnx, idut)
            except:
                print("Erreur lors de la modification de l'état de la demande")
                raise

        
class Categories:
    
    def get_categories(cnx):
        liste = []
        result = cnx.execute(text("select * from CATEGORIE;"))
        for row in result:
            liste.append((row[0],row[2],row[1]))
        return liste
    
    
class Domaine: 
    
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
        
        
    def get_id_domaine_from_categorie(cnx, id_categorie) :
        try:
            result = cnx.execute(text("SELECT idDomaine FROM CATEGORIE WHERE idCategorie = " + str(id_categorie) + ";"))
            for row in result:
                return row[0]
        except:
            print("Erreur lors de la récupération du domaine")
            raise

class Bon_commande:
    
    class Get:
        
        def afficher_bon_commande(cnx, idut): #get
            try:
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
                result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ");"))
                liste = []
                for row in result:
                    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                for row in result2:
                    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                return liste
            except:
                print("Erreur lors de l'affichage de la table")
                raise
            
        def get_id_bonCommande_actuel(cnx, idut):
            try:
                result = cnx.execute(text("SELECT idBonCommande FROM BONCOMMANDE WHERE idUtilisateur = " + str(idut) + " AND idEtat = 1;")) #enlever  AND idEtat = 1 si on delete le bon de commande validée
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du bon de commande")
                raise
            
        def get_bon_commande_with_id(cnx, idbc):
            try:
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires,referenceMateriel, quantite, informationsComplementairesEtSecurite, idFDS, idBonCommande FROM COMMANDE NATURAL JOIN MATERIEL natural join BONCOMMANDE WHERE idBonCommande = " + str(idbc) + " and idEtat != 1;"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise
            
        def consulter_bon_commande_without_table(cnx):
            try:
                list = []
                result = cnx.execute(text(" SELECT * FROM BONCOMMANDE WHERE idEtat != 1 and idEtat != 4;"))
                for row in result:
                    list.append(row)
                return list
            except:
                print("Erreur lors de la récupération des commandes")
                raise

        def get_bon_commande_with_statut(cnx, idetat):
            try:
                list = []
                result = cnx.execute(text("SELECT * FROM BONCOMMANDE WHERE idEtat = " + str(idetat) + ";"))
                for row in result:
                    list.append(row)
                return list
            except:
                print("Erreur lors de la récupération des commandes")
                raise

        def get_bon_commande_with_statut_fusion(cnx, idetat):
            try:
                list = []
                result = cnx.execute(text("SELECT * FROM BONCOMMANDE natural join COMMANDE WHERE idEtat = " + str(idetat) + ";"))
                for row in result:
                    list.append(row)
                return list
            except:
                print("Erreur lors de la récupération des commandes")
                raise
            
        def get_max_id_bon_commande(cnx):
            try:
                result = cnx.execute(text("SELECT MAX(idBonCommande) FROM BONCOMMANDE;"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du bon de commande")
                raise
            
    class Update:
        
        def changer_etat_bonCommande(cnx, idut):
            try:
                idetat = 2
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                cnx.execute(text("UPDATE BONCOMMANDE SET idEtat = " + str(idetat) + " WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
                Utilisateur.Insert.ajout_gest_into_boncommande(cnx,idut)
            except:
                print("Erreur lors du changement d'état du bon de commande")
                raise

        def changer_etat_bonCommande_with_id(cnx, idbc, idetat):
            try:
                cnx.execute(text("UPDATE BONCOMMANDE SET idEtat = " + str(idetat) + " WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors du changement d'état du bon de commande")
                raise

            

    class Delete:
        
        def delete_bonCommande_with_id(cnx, idbc):
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.execute(text("DELETE FROM BONCOMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du bon de commande")
                raise

    class Insert:

        def fusion_bon_commande(cnx, liste_bon_commande, idUt):
            try:
                # partie bon commande
                id_bon = Bon_commande.Get.get_max_id_bon_commande(cnx) + 1
                
                date = DATE.Get.get_date(cnx)
                
                cnx.execute(text("INSERT INTO BONCOMMANDE (idBonCommande, idEtat, idUtilisateur, dateBonCommande) VALUES ("+str(id_bon)+", 2, "+str(idUt)+ ", " + str(date) +");"))
                cnx.commit()
                # partie commande
                for commande in liste_bon_commande:
                    if cnx.execute(text("SELECT * FROM COMMANDE WHERE idBonCommande = "+str(id_bon)+" AND idMateriel = "+str(commande[4])+";")).first() is None:
                        cnx.execute(text("INSERT INTO COMMANDE (idBonCommande, idMateriel, quantite) VALUES ("+str(id_bon)+", "+str(commande[4])+", "+str(commande[5])+");"))
                    else:
                        cnx.execute(text("UPDATE COMMANDE SET quantite = quantite + "+str(commande[5])+" WHERE idBonCommande = "+str(id_bon)+" AND idMateriel = "+str(commande[4])+";"))
                    Bon_commande.Delete.delete_bonCommande_with_id(cnx, commande[0])
                    cnx.commit()   
            except:
                print("Erreur lors de l'ajout du bon de commande")
                raise

class Suggestion_materiel:
    
    def get_all_information_to_Materiel_suggestions(cnx):
            try:
                list = []
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL JOIN RISQUES NATURAL JOIN RISQUE ;"))
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

class Recherche_materiel:
    
    def get_MATERIEL(cnx):
        result = cnx.execute(text("select * from RECHERCHEMATERIELS;"))
        for row in result:
            print(row[0])
            
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

class Rangement:
    
    class Get:
        
        def get_id_endroit_from_id_rangement(cnx, idRangement) :
            try:
                result = cnx.execute(text("SELECT idEndroit FROM RANGEMENT WHERE idRangement = " + str(idRangement) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de l'endroit")
                raise


class Commande :

    class Get:
        
        def get_statut_from_commande_with_id_boncommande(cnx, id_boncommande):
            try:
                result = cnx.execute(text("SELECT idEtat, nomEtat FROM ETATCOMMANDE NATURAL JOIN BONCOMMANDE WHERE idBonCommande = " + str(id_boncommande) + ";"))
                liste = []
                for row in result:
                    liste.append(row[0])
                return liste
            except:
                print("Erreur lors de la récupération du statut de la commande")
                raise

        def get_statut_from_commande_with_id_etat(cnx, id_etat):
            try:
                result = cnx.execute(text("SELECT idEtat, nomEtat FROM ETATCOMMANDE WHERE idEtat = " + str(id_etat) + ";"))
                liste = []
                for row in result:
                    liste.append(row[0])
                return liste
            except:
                print("Erreur lors de la récupération du statut de la commande")
                raise

        def get_statut_from_commande(cnx):
            try:
                result = cnx.execute(text("SELECT * FROM ETATCOMMANDE;"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du statut de la commande")
                raise

class STOCKLABORATOIRE:
    class Get:
        def get_quantite_with_idMateriel(cnx, idMateriel):
            try:
                result = cnx.execute(text("SELECT quantiteLaboratoire FROM STOCKLABORATOIRE natural join MATERIEL WHERE idMateriel = " + str(idMateriel) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de la quantité")
                raise

        def materiel_dans_stock(cnx, idMateriel):
            try:
                result = cnx.execute(text("SELECT COUNT(*) FROM STOCKLABORATOIRE WHERE idMateriel = " + str(idMateriel) + ";"))
                print(text("SELECT COUNT(*) FROM STOCKLABORATOIRE WHERE idMateriel = " + str(idMateriel) + ";"))
                for row in result:
                    return row[0]
                cnx.commit()
            except:
                print("Erreur lors de l'insertion du matériel dans le stock")
                raise
        
    class Insert:
        def insere_materiel_stock(cnx, idMateriel):
            try:
                cnx.execute(text("INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (" + str(idMateriel) + ", 0);"))
                cnx.commit()
            except:
                print("Erreur lors de l'insertion du matériel dans le stock")
                raise

class DATE:
    class Get:
        def get_date(cnx):
            date_result = cnx.execute(text("SELECT CURDATE();")).fetchone()
                
            # Extraire la date du résultat
            date_res = date_result[0] if date_result else datetime.now().date()
            return date_res

        def materiel_dans_stock(cnx, idMateriel):
            try:
                result = cnx.execute(text("SELECT COUNT(*) FROM STOCKLABORATOIRE WHERE idMateriel = " + str(idMateriel) + ";"))
                for row in result:
                    return row[0]
                cnx.commit()
            except:
                print("Erreur lors de l'insertion du matériel dans le stock")
                raise
        
    class Insert:
        def insere_materiel_stock(cnx, idMateriel):
            try:
                cnx.execute(text("INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (" + str(idMateriel) + ", 0);"))
                cnx.commit()
            except:
                print("Erreur lors de l'insertion du matériel dans le stock")
                raise

class ReserveLaboratoire :
    class Get:
        def get_last_id_reserve(cnx) :
            try :
                res = None
                result = cnx.execute(text("SELECT idReserve FROM RESERVELABORATOIRE ORDER BY idReserve DESC LIMIT 1 ;"))

                for row in result:
                    res = row[0]
                if res == None :
                    return 0
                else :
                    return res
            except :
                print("Erreur lors de la récupération du dernier id")
                raise
        
    class Insert:
        def insere_materiel_unique_reserve(cnx, idMaterielUnique):
            last_id_reserve = ReserveLaboratoire.Get.get_last_id_reserve(cnx)+1
            cnx.execute(text("INSERT INTO RESERVELABORATOIRE (idReserve,idMaterielUnique) VALUES (" + str(last_id_reserve) + "," + str(idMaterielUnique) + ");"))
            cnx.commit()
            return True
                
            # print("INSERT INTO RESERVELABORATOIRE (idMaterielUnique) VALUES (" + str(idMaterielUnique) + ");")
            # print("Erreur lors de l'insertion du matériel dans la réserve")
            # return False
            #recuperer que la date 
            date_res = date_res.strftime("%Y-%m-%d")

            return date_res
                
class RELOAD:
    
    def reload_alert(cnx):
        try:
            cnx.execute(text("call gestionAlertes();"))
            cnx.commit()
        except:
            print("Erreur lors du reload des alertes")
            raise


class FDS:
    class Get:
        def get_FDS_with_idMateriel(cnx, idMat):
            try:
                result = cnx.execute(text("SELECT idFDS FROM MATERIEL natural join FDS WHERE idMateriel = " + str(idMat) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de la FDS")
                raise

        def get_idFDS_with_nomFDS(cnx, nomFDS):
            try:
                result = cnx.execute(text("SELECT idFDS FROM FDS WHERE nomFDS = '" + nomFDS + "';"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de la FDS")
                raise
    
    class Insert:
        def ajout_FDS(cnx, nomFDS):
            cnx.execute(text("INSERT INTO FDS (nomFDS) VALUES ('" + nomFDS + "');"))
            cnx.commit()
        
    class Update:
        def update_FDS(cnx, idFDS, idMateriel):
            cnx.execute(text("UPDATE MATERIEL SET idFDS = '" + str(idFDS) + "' WHERE idMateriel = " + str(idMateriel) + ";"))
            cnx.commit()

        

class Risques:
    
    class Get:
        # def get_risque_with_idMateriel(cnx, idMat):
        #     try:
        #         result = cnx.execute(text("SELECT * FROM MATERIEL natural join FDS natural join RISQUES Natural join RISQUE WHERE idFDS = " + str(idMat) + ";"))
        #         for row in result:
        #             return row[0]
        #     except:
        #         print("Erreur lors de la récupération de l'id du risque")
        #         raise
        
        def get_risque_with_idMateriel(cnx, idMat):
            try:
                referenceMateriel = ""
                nomMateriel = ""
                listBooleanTrue = []
                result = cnx.execute(text("SELECT nomRisque, referenceMateriel, nomMateriel FROM MATERIEL natural join FDS natural join RISQUES Natural join RISQUE WHERE idFDS = " + str(idMat) + ";"))
                
                for row in result:
                    listBooleanTrue.append(row[0])
                    nomMateriel = row[2]
                    referenceMateriel = row[1]
                
                listBoolean = []
                if "Toxicité aiguë" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                
                if "Danger incendie" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Explosif" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Gaz sous pression" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Toxicité aquatique" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Effets graves sur l'environement" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Altération de la santé humaine" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Comburant" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Corrosion" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                return referenceMateriel, nomMateriel, listBoolean[0], listBoolean[1], listBoolean[2], listBoolean[3], listBoolean[4], listBoolean[5], listBoolean[6], listBoolean[7], listBoolean[8]
            except:
                print("Erreur lors de la récupération du risque")
                return None
    class Update:
        def update_risque_with_idMateriel(cnx, idMat, estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif):
            try:
                idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, idMat)
                listidRisque = []
                listRisqueAMateriel = []
                
                if estToxique:
                    listRisqueAMateriel.append("Toxicité aiguë")
                if estInflamable:
                    listRisqueAMateriel.append("Danger incendie")
                if estExplosif:
                    listRisqueAMateriel.append("Explosif")
                if est_gaz_sous_pression:
                    listRisqueAMateriel.append("Gaz sous pression")
                if est_CMR:
                    listRisqueAMateriel.append("Toxicité aquatique")
                if est_chimique_environement:
                    listRisqueAMateriel.append("Effets graves sur l'environement")           
                if est_dangereux:
                    listRisqueAMateriel.append("Altération de la santé humaine")          
                if est_comburant:
                    listRisqueAMateriel.append("Comburant")
                if est_corrosif:
                    listRisqueAMateriel.append("Corrosion")
                    
                resultRisque = cnx.execute(text("SELECT idRisque, nomRisque FROM RISQUE;"))
                
                for row in resultRisque:
                    if row[1] in listRisqueAMateriel:
                        listidRisque.append(row[0])
                
                cnx.execute(text("DELETE FROM RISQUES WHERE idFDS = " + str(idFDS) + ";"))
                cnx.commit()
                
                for idRisque in listidRisque:
                    Risques.Insert.ajout_risques_with_idFDS_and_idrisque(cnx, idRisque, idFDS)
            except:
                print("Erreur lors de la modification du risque")
                raise
        
    class Insert:
        def ajout_risques_with_idFDS_and_idrisque(cnx, idRisque, idFDS):
            try:
                cnx.execute(text("INSERT INTO RISQUES (idFDS, idRisque) VALUES (" + str(idFDS) + ", " + str(idRisque) + ");"))
                cnx.commit()
            except:
                print("Erreur lors de l'ajout du risque")
                raise               
            
        
        def ajout_risque_with_idMateriel(cnx, idMat, estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif):
            try:
                idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, idMat)
                listidRisque = []
                listRisqueAMateriel = []
                
                if estToxique:
                    listRisqueAMateriel.append("Toxicité aiguë")
                if estInflamable:
                    listRisqueAMateriel.append("Danger incendie")
                if estExplosif:
                    listRisqueAMateriel.append("Explosif")
                if est_gaz_sous_pression:
                    listRisqueAMateriel.append("Gaz sous pression")
                if est_CMR:
                    listRisqueAMateriel.append("Toxicité aquatique")
                if est_chimique_environement:
                    listRisqueAMateriel.append("Effets graves sur l'environement")           
                if est_dangereux:
                    listRisqueAMateriel.append("Altération de la santé humaine")          
                if est_comburant:
                    listRisqueAMateriel.append("Comburant")
                if est_corrosif:
                    listRisqueAMateriel.append("Corrosion")
                    
                resultRisque = cnx.execute(text("SELECT idRisque, nomRisque FROM RISQUE;"))
                
                for row in resultRisque:
                    if row[1] in listRisqueAMateriel:
                        listidRisque.append(row[0])
                
                for idRisque in listidRisque:
                    Risques.Insert.ajout_risques_with_idFDS_and_idrisque(cnx, idRisque, idFDS)
            except:
                print("Erreur lors de l'ajout du risque")
                raise
    class Delete:

        def delete_risque_with_idMateriel(cnx, idMat):
            try:
                idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, idMat)
                cnx.execute(text("DELETE FROM RISQUES WHERE idFDS = " + str(idFDS) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du risque")
                raise

# Risques.Delete.delete_risque_with_idMateriel()
# Materiel.Delete.delete_materiel()         