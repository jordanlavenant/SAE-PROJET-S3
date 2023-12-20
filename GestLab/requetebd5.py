import random
import string
import json
import smtplib
from email.message import EmailMessage
from hashlib import sha256
from sqlalchemy import text
import qrcode
import pyotp
from .connexionPythonSQL import *
from .models import *

cnx = ouvrir_connexion()

def get_cnx():
    """
    Cette fonction retourne un objet de connexion (conn).
    
    Returns:
        object: Un objet de connexion.
    """
    return cnx


class Table:
    """
    Classe pour représenter une table de base de données.
    
    Attributs:
        cnx (object): Objet de connexion à la base de données.
        table (str): Nom de la table.
    """
    class Get:
        """
        Classe pour récupérer des informations d'une table de base de données.
        """
        def afficher_table(cnx, table):
            """
            Affiche le contenu d'une table spécifique.
            
            Paramètres:
                cnx (object): Objet de connexion à la base de données.
                table (str): Nom de la table à afficher.
                
            Retourne:
                list: Liste des enregistrements de la table.
                
            Exceptions:
                print("Erreur lors de l'affichage de la table")
            """
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
    """
    Cette classe représente un utilisateur du système. Elle contient des méthodes pour récupérer des informations sur les utilisateurs.
    
    Attributes:
        None
    """

    class Get:
        """
        Cette classe contient des méthodes pour récupérer des informations sur les utilisateurs.
        
        Attributes:
            None
        """

        def get_nom_whith_email(cnx, email):
            """
            Cette méthode récupère le nom d'un utilisateur à partir de son adresse e-mail.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.

            Returns:
                str: Le nom de l'utilisateur.
            """
            result = cnx.execute(text("select nom from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                print(row[0])
            return row[0]

        def get_id_utilisateur_from_email(cnx, email) :
            """
            Cette méthode récupère l'identifiant d'un utilisateur à partir de son adresse e-mail.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.
            
            Returns:
                int: L'identifiant de l'utilisateur.
            """
            try:
                result = cnx.execute(text("SELECT idUtilisateur FROM UTILISATEUR WHERE email = '" + email + "';"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de l'affichage de la table")
                raise

        def get_password_with_email(cnx, email):
            """
            Cette méthode récupère le mot de passe d'un utilisateur à partir de son adresse e-mail.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.
            
            Returns:
                str: Le mot de passe de l'utilisateur.
            """
            result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                return row[0]


        def get_nom_and_statut_and_email(cnx, email):
            """
            Cette méthode récupère le nom, le statut et l'adresse e-mail d'un utilisateur à partir de son adresse e-mail.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.
            
            Returns:
                tuple: Un tuple contenant le nom, le statut et l'adresse e-mail de l'utilisateur.
            """
            result = cnx.execute(text("select nom, idStatut, prenom from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                print(row[0], row[1], row[2], email)
                return (row[0], row[1], email, row[2])


        def get_user_with_statut(cnx, nomStatut):
            """
            Cette méthode récupère tous les utilisateurs ayant un statut spécifique.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                nomStatut (str): Le nom du statut à rechercher.
            
            Returns:
                list: Une liste contenant les identifiants des utilisateurs correspondant au statut spécifié.
            """
            liste = []
            result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where nomStatut = '" + str(nomStatut) + "';"))
            for row in result:
                liste.append((row[4]))
            return liste

        def get_all_user(cnx, idStatut=None):
            """
            Cette méthode récupère tous les utilisateurs de la base de données.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                idStatut (int, optional): Le statut de l'utilisateur. Si cet argument n'est pas fourni, la méthode récupérera tous les utilisateurs.
            
            Returns:
                tuple: Un tuple contenant deux éléments :
                    - Une liste de tuples contenant des informations sur les utilisateurs.
                    - Le nombre total d'utilisateurs récupérés.
            """
            liste = []
            if idStatut is None:
                result = cnx.execute(text("select * from UTILISATEUR where idStatut != 1;"))
            else:
                result = cnx.execute(text("select * from UTILISATEUR where idStatut = '" + str(idStatut) + "';"))
            for row in result:
                liste.append((row[1],row[0],row[2],row[3],row[4]))
            return (liste, len(liste))

        def get_uri_with_email(cnx, email):
            """
            Cette méthode récupère l'URI d'un utilisateur à partir de son adresse e-mail.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.
            
            Returns:
                str: L'URI de l'utilisateur.
            """
            result = cnx.execute(text("select uri from 2FA where email = '" + email + "';"))
            for row in result:
                print(row[0])
                return row[0]

        def get_id_with_email(cnx, email):
            """
            Cette méthode récupère l'identifiant d'un utilisateur à partir de son adresse e-mail.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.
            
            Returns:
                int: L'identifiant de l'utilisateur.
            
            """
            result = cnx.execute(text("select idUtilisateur from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                return row[0]

        def get_all_information_utilisateur_with_id(cnx, id):
            """
            Cette méthode récupère toutes les informations sur un utilisateur à partir de son identifiant.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                id (int): L'identifiant de l'utilisateur.
            
            Returns:
                tuple: Un tuple contenant les informations de l'utilisateur (nom, prénom, adresse e-mail, nom du statut).
            
            Raises:
                Exception: Si une erreur se produit lors de la récupération des informations.
            """
            try:
                result = cnx.execute(text("select nom,prenom,email,nomStatut from UTILISATEUR natural join STATUT where idUtilisateur = " + str(id) + ";"))
                for row in result:
                    return row
            except:
                print("erreur de l'id")
                raise

    class Update:
        """
        Cette classe contient des méthodes pour mettre à jour les informations d'un utilisateur dans la base de données.
        """

        def update_email_utilisateur(cnx, new_email, nom, mdp, old_email):
            """
            Cette méthode met à jour l'adresse e-mail d'un utilisateur dans la base de données.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                new_email (str): La nouvelle adresse e-mail de l'utilisateur.
                nom (str): Le nom de l'utilisateur.
                mdp (str): Le mot de passe de l'utilisateur.
                old_email (str): L'ancienne adresse e-mail de l'utilisateur.
            
            Returns:
                bool: True si la mise à jour a réussi, False sinon.
            """
            try:
                Utilisateur.Update.update_email_utilisateur_in_ut(cnx, new_email, nom, mdp)
                Utilisateur.Update.update_email_utilisateur_in_2fa(cnx, old_email, new_email)
                print("email mis a jour")
                return True
            except:
                print("erreur de mise a jour de l'email")
                return False

        def update_email_utilisateur_in_ut(cnx, new_email, nom, mdp):
            """
            Cette méthode met à jour l'adresse e-mail d'un utilisateur dans la table UTILISATEUR.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                new_email (str): La nouvelle adresse e-mail de l'utilisateur.
                nom (str): Le nom de l'utilisateur.
                mdp (str): Le mot de passe de l'utilisateur.
            
            Returns:
                bool: True si la mise à jour a réussi, False sinon.
            """
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
            """
            Cette méthode met à jour l'adresse e-mail d'un utilisateur dans la table 2FA.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                old_email (str): L'ancienne adresse e-mail de l'utilisateur.
                new_email (str): La nouvelle adresse e-mail de l'utilisateur.
            
            Returns:
                bool: True si la mise à jour a réussi, False sinon.
            """
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
            """
            Cette méthode met à jour le statut d'un utilisateur dans la base de données.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                idut (int): L'identifiant de l'utilisateur.
                idSt (int): L'identifiant du nouveau statut de l'utilisateur.
            
            Returns:
                None
            """
            try:
                cnx.execute(text("update UTILISATEUR set idStatut = '" + str(idSt) + "' where idUtilisateur = '" + str(idut) + "';"))
                cnx.commit()
                print("droit mis a jour")
            except:
                print("erreur de mise a jour du droit")
                raise

        def update_mdp_utilisateur(cnx, email, mdp, new_mdp):
            """
            Cette méthode met à jour le mot de passe d'un utilisateur dans la base de données.
            
            Args:
                cnx (object): Un objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.
                mdp (str): Le mot de passe actuel de l'utilisateur.
                new_mdp (str): Le nouveau mot de passe de l'utilisateur.
            
            Returns:
                bool: True si la mise à jour a réussi, False sinon.
            """
            try:
                init_mdp = Mots_de_passe.hasher_mdp(mdp)
                new_mdp_hash = Mots_de_passe.hasher_mdp(new_mdp)
                mdp_get = Utilisateur.Get.get_password_with_email(cnx, email)
                if mdp_get != init_mdp:
                    print("mdp incorrect")
                    return False
                cnx.execute(text("update UTILISATEUR set mdp = '" + new_mdp_hash + "' where email = '" + email + "';"))
                cnx.commit()
                print("mdp mis a jour")
                return True
            except:
                print("erreur de mise a jour du mdp")
                return False

        def update_nom_utilisateur(self, email, new_nom):
            """
            Cette méthode permet de mettre à jour le nom d'un utilisateur.
            
            Args:
                email (str): email de l'utilisateur.
                new_nom (str): nouveau nom de l'utilisateur.
            
            Returns:
                None.
            """
            try:
                self.cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "';"))
                self.cnx.commit()
                print("nom mis a jour")
            except:
                print("erreur de mise a jour du nom")
                raise


        def update_prenom_utilisateur(self, email, new_prenom):
            """
            Cette méthode permet de mettre à jour le prénom d'un utilisateur.
            
            Args:
                email (str): email de l'utilisateur.
                new_prenom (str): nouveau prénom de l'utilisateur.
            
            Returns:
                None.
            """
            try:
                self.cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "';"))
                self.cnx.commit()
                print("prenom mis a jour")
            except:
                print("erreur de mise a jour du prenom")
                raise

        def update_all_information_utillisateur_with_id(self, id, idStatut, nom, prenom, email):
            """
            Cette méthode permet de mettre à jour toutes les informations d'un utilisateur en utilisant son identifiant.
            
            Args:
                id (int): identifiant de l'utilisateur.
                idStatut (int): nouveau statut de l'utilisateur.
                nom (str): nouveau nom de l'utilisateur.
                prenom (str): nouveau prénom de l'utilisateur.
                email (str): nouveau email de l'utilisateur.
            
            Returns:
                None.
            """
            try:
                self.cnx.execute(text("update UTILISATEUR set idStatut = '" + str(idStatut) + "', nom = '" + nom + "', prenom = '" + prenom + "', email = '" + email + "' where id = '" + str(id) + "';"))
                self.cnx.commit()
                print("toutes les informations de l'utilisateur mises a jour")
            except:
                print("erreur de mise a jour des informations de l'utilisateur")
                raise

    class Insert:
        """
        Cette classe permet d'ajouter des informations dans la base de données.
        """

        def ajout_fournisseur(self, nom, adresse, mail, tel):
            """
            Cette méthode permet d'ajouter un fournisseur à la base de données.
            
            Args:
                nom (str): nom du fournisseur.
                adresse (str): adresse du fournisseur.
                mail (str): email du fournisseur.
                tel (str): téléphone du fournisseur.
            
            Returns:
                None.
            """
            try:
                self.cnx.execute(text("insert into FOURNISSEUR (nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values ('" + nom + "', '" + adresse + "', '" + mail + "', '" + tel + "');"))
                self.cnx.commit()
                print("fournisseur ajouté")
            except:
                print("erreur d'ajout du fournisseur")
                raise

        def ajout_gest_into_boncommande(self, id):
            """
            Cette méthode permet d'ajouter un bon de commande à la base de données avec un état de début à 1.
            
            Args:
                id (int): identifiant de l'utilisateur qui ajoute le bon de commande.
            
            Returns:
                None.
            """
            try:
                etat = 1
                self.cnx.execute(text("insert into BONCOMMANDE (idEtat,idUtilisateur ) values (" + str(etat) + ", " + str(id) + ");"))
                self.cnx.commit()
                print("bon de commande ajouté")
            except:
                print("erreur d'ajout du bon de commande")
                raise

        def ajout_professeur(self, nom, prenom, email):
            """
            Cette méthode permet d'ajouter un professeur à la base de données.
            
            Args:
                nom (str): nom du professeur.
                prenom (str): prénom du professeur.
                email (str): email du professeur.
            
            Returns:
                None.
            """
            try:
                idStatut = 2
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                self.cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash + "');"))
                self.cnx.commit()
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False

        def ajout_gestionnaire(self, nom, prenom, email):
            """
            Cette méthode permet d'ajouter un gestionnaire à la base de données.

            Args:
                nom (str): nom du gestionnaire.
                prenom (str): prénom du gestionnaire.
                email (str): email du gestionnaire.

            Returns:
                None.
            """
            try:
                idStatut = 4
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                self.cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash + "');"))
                self.cnx.commit()
                id = Utilisateur.Get.get_id_with_email(self.cnx, email)
                Utilisateur.Insert.ajout_gest_into_boncommande(self.cnx,id)
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False  

        def ajout_administrateur(self, nom, prenom, email):
            """
            Cette méthode permet d'ajouter un administrateur à la base de données.
            
            Args:
                nom (str): nom de l'administrateur.
                prenom (str): prénom de l'administrateur.
                email (str): email de l'administrateur.
            
            Returns:
                None.
            """
            try:
                idStatut = 1
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                self.cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash + "');"))
                self.cnx.commit()
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False

        def ajout_laborantin(self, nom, prenom, email):
            """
            Cette méthode permet d'ajouter un laborantin à la base de données.
            
            Args:
                nom (str): nom du laborantin.
                prenom (str): prénom du laborantin.
                email (str): email du laborantin.
            
            Returns:
                None.
            """
            try:
                idStatut = 3
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                self.cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash + "');"))
                self.cnx.commit()
                Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False
    class Delete:
        """
        Cette classe permet de supprimer des informations dans la base de données.
        """

        def delete_utilisateur(self, idut):
            """
            Cette méthode permet de supprimer un utilisateur et toutes ses informations associées à partir de son identifiant.
            
            Args:
                idut (int): identifiant de l'utilisateur.
            
            Returns:
                None.
            """
            try:
                bonCommande = self.cnx.execute(text("select idBonCommande from BONCOMMANDE where idUtilisateur = '" + str(idut) + "';"))
                for row in bonCommande:
                    self.cnx.execute(text("delete from COMMANDE where idBonCommande = '" + str(row[0]) + "';"))
                self.cnx.execute(text("delete from BONCOMMANDE where idUtilisateur = '" + str(idut) + "';"))
                self.cnx.execute(text("delete from 2FA where idUtilisateur = '" + str(idut) + "';"))
                self.cnx.execute(text("delete from UTILISATEUR where idUtilisateur = '" + str(idut) + "';"))
                self.cnx.commit()
                print("utilisateur supprimé")
            except:
                print("erreur de suppression de l'utilisateur")
                raise

        def delete_utilisateur_with_email(self, email):
            """
            Cette méthode permet de supprimer un utilisateur et toutes ses informations associées à partir de son email.
            
            Args:
                email (str): email de l'utilisateur.
            
            Returns:
                None.
            """
            try:
                self.cnx.execute(text("delete from UTILISATEUR where email = '" + email + "';"))
                self.cnx.commit()
                print("utilisateur supprimé")
            except:
                print("erreur de suppression de l'utilisateur")
                raise
class Materiel:
    """
    La classe Materiel contient deux sous-classes Get et Modify. La sous-classe Get contient des méthodes pour récupérer des informations sur le matériel. La sous-classe Modify contient des méthodes pour modifier des informations sur le matériel.
    """
    class Get:
        """
        La sous-classe Get contient des méthodes pour récupérer des informations sur le matériel.
        """

        def get_all_information_to_Materiel_cat_com(cnx):
            """
            Récupère toutes les informations sur le matériel depuis la table MATERIEL. Il récupère également des informations sur la catégorie et le domaine.

            Args:
                cnx (object): L'objet de connexion à la base de données.

            Returns:
                list: Une liste de tuples contenant les informations sur le matériel, la catégorie et le domaine.
            """
            try:
                list = []
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite from MATERIEL NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE ;"))
                for row in result:
                    print(row)
                    list.append(row)
                return list
            except:
                print("erreur de l'id")
                raise

        def get_all_information_to_Materiel_with_id(cnx, id):
            """
            Récupère toutes les informations sur le matériel avec un id spécifique depuis la table MATERIEL. Il récupère également des informations sur la catégorie, le domaine, FDS, RISQUES, et STOCKLABORATOIRE.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id (int): L'id du matériel.

            Returns:
                tuple: Un tuple contenant les informations sur le matériel, la catégorie, le domaine, FDS, RISQUES, STOCKLABORATOIRE.
            """
            try:
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,pictogramme,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock from MATERIEL natural left join STOCKLABORATOIRE NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL LEFT JOIN RISQUES NATURAL LEFT JOIN RISQUE WHERE idMateriel = " + str(id) + ";"))
                for row in result:
                    return row
            except:
                print("erreur de l'id")
                raise


        def get_all_information_to_Materiel(cnx):
            """
            Récupère toutes les informations sur le matériel depuis la table MATERIEL. Il récupère également des informations sur la catégorie, le domaine, FDS, RISQUES, et STOCKLABORATOIRE.

            Args:
                cnx (object): L'objet de connexion à la base de données.

            Returns:
                list: Une liste de tuples contenant les informations sur le matériel, la catégorie, le domaine, FDS, RISQUES, STOCKLABORATOIRE.
                int: Le nombre total de lignes renvoyées.
            """
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


        def get_materiel_commande(cnx,idbc):
            """
            Récupère toutes les informations sur le matériel avec un id de bon de commande spécifique depuis la table COMMANDE.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idbc (int): L'id du bon de commande.

            Returns:
                list: Une liste de tuples contenant les informations sur le matériel.
            """
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

        def get_id_materiel_from_id_materiel_unique(cnx, id_materiel_unique) :
            """
            Récupère l'id du matériel avec un id unique du matériel spécifique depuis la table MATERIELUNIQUE.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id_materiel_unique (int): L'id unique du matériel.

            Returns:
                int: L'id du matériel.
            """
            try:
                result = cnx.execute(text("SELECT idMateriel FROM MATERIELUNIQUE NATURAL JOIN MATERIEL WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du matériel")
                raise

        def get_materiel(cnx, idMateriel) :
            """
            Récupère le matériel avec un id du matériel spécifique depuis la table MATERIEL.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMateriel (int): L'id du matériel.

            Returns:
                list: La liste des informations du matériel.
            """
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
            """
            Récupère tous les matériels avec un id d'utilisateur spécifique pour les inclure dans un PDF dans le bon de commande.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idut (int): L'id de l'utilisateur.

            Returns:
                list: La liste des informations des matériels.
            """
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

        def get_all_materiel_for_pdf_in_bon_commande_after(cnx, idbc) :
            """
            Récupère tous les matériels pour les inclure dans un PDF dans le bon de commande après un id de bon de commande spécifique.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idbc (int): L'id du bon de commande.

            Returns:
                list: La liste des informations des matériels.
            """
            try:
                result = cnx.execute(text("SELECT nomMateriel, referenceMateriel, nomDomaine,nomCategorie, quantite from COMMANDE NATURAL JOIN MATERIEL NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE WHERE idBonCommande = " + str(idbc) + ";"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise

        def get_materiel_in_bonDeCommande(cnx, idut) :
            """
            Récupère le matériel avec un id d'utilisateur spécifique dans le bon de commande.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idut (int): L'id de l'utilisateur.

            Returns:
                list: La liste des informations des matériels.
            """
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

        def get_nom_dom_cat_materiel_with_id(cnx, id) :
            """
            Récupère le nom du domaine, le nom de la catégorie et le matériel avec un id de matériel spécifique.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id (int): L'id du matériel.

            Returns:
                tuple: Le nom du domaine, le nom de la catégorie et le matériel.
            """
            try:
                result = cnx.execute(text("select nomDomaine,nomCategorie from MATERIEL natural join DOMAINE natural join CATEGORIE where idMateriel = " + str(id) + ";"))
                result = result.first()
                return result
            except:
                print("erreur de l'id")
                raise


    class Delete:
        """
        Classe qui contient des méthodes pour supprimer des matériels dans des bons de commande.
        """

        def delete_materiel_in_BonCommande_whith_id(cnx, idMateriel, idbc):
            """
            Supprime un matériel spécifique dans le bon de commande avec des id de matériel et de bon de commande spécifiques.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMateriel (int): L'id du matériel.
                idbc (int): L'id du bon de commande.

            Returns:
                None
            """
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idMateriel = " + str(idMateriel) + " AND idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_all_materiel_in_commande(cnx, idut):
            """
            Supprime tous les matériels dans le bon de commande pour un utilisateur spécifique.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idut (int): L'id de l'utilisateur.

            Returns:
                None
            """
            try:
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                cnx.execute(text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

    class Update:
        """
        Classe qui contient des méthodes pour modifier des matériels.
        """
        def modifie_materiel(cnx, idMateriel, categorie, nom, reference, caracteristiques, infossup, seuilalerte):
            """
            Modifie les informations d'un matériel spécifique avec un id de matériel spécifique.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMateriel (int): L'id du matériel.
                categorie (int): L'id de la catégorie.
                nom (str): Le nom du matériel.
                reference (str): La référence du matériel.
                caracteristiques (str): Les caractéristiques du matériel.
                infossup (str): Les informations supplémentaires et de sécurité du matériel.
                seuilalerte (int): Le seuil d'alerte du matériel.

            Returns:
                bool: True si la modification a réussi, False sinon.
            """
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
            """
            Méthode qui met à jour la quantité des matériels dans le bon de commande à partir de la table AJOUTERMATERIEL.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idDemande (int): L'id de la demande.
                idut (int): L'id de l'utilisateur.
                boolajouterMat (bool): Indique si on ajoute ou non un matériel unique à la demande. Vaut False par défaut.

            Returns:
                None
            """
            try:
                result = cnx.execute(text("SELECT idMateriel,quantite from AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                for row in result:
                    Materiel.Insert.ajout_materiel_in_commande(cnx, row[0], idut, row[1], boolajouterMat)
                    MaterielUnique.Delete.delete_materiel_unique_in_demande(cnx, idDemande, row[0])
            except:
                print("Erreur lors de la mise à jour de la quantité dans la demande")
                raise

    class Insert:
        """
        Classe qui contient des méthodes pour insérer des matériels.
        """
        def insere_materiel(
            cnx, idCategorie, nomMateriel, referenceMateriel,
            caracteristiquesComplementaires, informationsComplementairesEtSecurite, seuilAlerte
        ):
            """
            Insère un matériel dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idCategorie (int): L'id de la catégorie.
                nomMateriel (str): Le nom du matériel.
                referenceMateriel (str): La référence du matériel.
                caracteristiquesComplementaires (str): Les caractéristiques du matériel.
                informationsComplementairesEtSecurite (str): Les informations supplémentaires et de sécurité du matériel.
                seuilAlerte (int): Le seuil d'alerte du matériel.

            Returns:
                bool: True si l'insertion a réussi, False sinon.
            """
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
            """
            Méthode qui ajoute un matériel dans la commande actuelle de l'utilisateur.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idmat (int): L'id du matériel.
                idut (int): L'id de l'utilisateur.
                quantite (int): La quantité du matériel.
                boolajouterMat (bool): Indique si on ajoute ou non un matériel unique à la demande. Vaut False par défaut.

            Returns:
                None
            """
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

class MaterielUnique:
    """
    Classe qui contient des méthodes pour gérer les matériels uniques.
    """

    class Get:
        """
        Classe qui contient des méthodes pour récupérer des informations sur les matériels uniques.
        """

        def get_materiel_unique(cnx, idMaterielUnique) :
            """
            Récupère un matériel unique à partir de son id.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMaterielUnique (int): L'id du matériel unique.

            Returns:
                list: La liste des informations du matériel unique.
            """

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
            """
            Récupère le nombre de matériels uniques dans une demande.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idDemande (int): L'id de la demande.

            Returns:
                int: Le nombre de matériels uniques dans la demande.
            """

            try:
                result = cnx.execute(text("SELECT COUNT(*) FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération du nombre de matériel unique dans la demande")
                raise

        def get_all_information_to_MaterielUnique_with_id(cnx, id):
            """
            Récupère toutes les informations sur un matériel unique à partir de son id.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id (int): L'id du matériel.

            Returns:
                tuple: Un tuple contenant une liste des informations du matériel unique et le nombre d'informations.
            """

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
            """
            Récupère le nombre de matériels uniques correspondant à un id de matériel.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id (int): L'id du matériel.

            Returns:
                int: Le nombre de matériels uniques correspondant à l'id de matériel.
            """

            try:
                result = cnx.execute(text("select count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
                for row in result:
                    return row[0]
            except:
                print("erreur de l'id")
                raise

    class Delete:
        """
        Classe qui contient des méthodes pour supprimer des informations sur les matériels uniques.
        """
        def delete_all_materiel_unique_with_idMateriel(cnx, id_materiel):
            """
            Supprime tous les matériels uniques correspondant à un id de matériel.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id_materiel (int): L'id du matériel.
            """
            try:
                cnx.execute(text("DELETE FROM ALERTESENCOURS WHERE idMaterielUnique IN (SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE idMateriel = " + str(id_materiel) + ");"))
                cnx.execute(text("DELETE FROM RESERVELABORATOIRE WHERE idMaterielUnique IN (SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE idMateriel = " + str(id_materiel) + ");"))
                cnx.execute(text("DELETE FROM MATERIELUNIQUE WHERE idMateriel = " + str(id_materiel) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression de tous les matériels uniques")
                raise

        def delete_materiel_unique_in_demande(cnx, idDemande, idMateriel):
            """
            Supprime un matériel unique dans une demande.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idDemande (int): L'id de la demande.
                idMateriel (int): L'id du matériel.
            """
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
            """
            Supprime un matériel unique de la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id_materiel_unique (int): L'id du matériel unique.
            """
            try :
                cnx.execute(text("DELETE FROM ALERTESENCOURS WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
                cnx.execute(text("DELETE FROM RESERVELABORATOIRE WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
                cnx.execute(text("DELETE FROM MATERIELUNIQUE WHERE idMaterielUnique = " + str(id_materiel_unique) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel unique")
                raise

    class Update:
        """
        Classe qui contient des méthodes pour mettre à jour des informations sur les matériels uniques.
        """
        def modifie_materiel_unique(cnx, idMaterielUnique, idRangement, dateReception, datePeremption, commentaireMateriel, quantiteApproximative) :
            """
            Modifie un matériel unique à partir de son id.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMaterielUnique (int): Identifiant du matériel unique à modifier.
                idRangement (int): Nouvel identifiant du rangement.
                dateReception (str): Nouvelle date de réception.
                datePeremption (str): Nouvelle date de péremption.
                commentaireMateriel (str): Nouveau commentaire sur le matériel.
                quantiteApproximative (int): Nouvelle quantité approximative.

            Returns:
                True si la modification a réussi, False sinon.
            """
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
        """
        Classe qui contient des méthodes pour inserer des informations sur les matériels uniques.
        """
        def insere_materiel_unique(
            cnx, id_materiel, position, date_reception, date_peremption, commentaire, quantite_approximative
        ):
            """
            Insère un nouveau matériel unique dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id_materiel (int): Identifiant du matériel.
                position (int): Position du matériel dans le rangement.
                date_reception (str): Date de réception du matériel.
                date_peremption (str): Date de péremption du matériel.
                commentaire (str): Commentaire sur le matériel.
                quantite_approximative (int): Quantité approximative du matériel.

            Returns:
                True si l'insertion a réussi, False sinon.
            """
            try:
                if date_peremption is None or date_peremption == 'None' or date_peremption == "":
                    date_peremption = "NULL"
                else:
                    date_peremption = f"'{str(date_peremption)}'"

                query = (
                    "INSERT INTO MATERIELUNIQUE (idMateriel, idRangement, dateReception, datePeremption, "
                    "commentaireMateriel, quantiteApproximative) VALUES ('{}', '{}', '{}', {}, '{}', {});".format(
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
                return True
            except sqlalchemy.exc.OperationalError as e:
                print(f"SQL OperationalError: {e}")
                return False
            except sqlalchemy.exc.IntegrityError as e:
                print(f"SQL IntegrityError: {e}")
                return False

class Recherche:
    """
    Classe qui contient des méthodes pour tout tyope de recherche dans la base de données.
    """

    def recherche_materiel_commander_search(cnx, search):
        """
        Fonction pour rechercher les matériels commandés avec un mot clé donné.

        Args:
            cnx (object): Objet de connexion à la base de données.
            search (str): Mot clé à rechercher dans les noms de matériels.

        Returns:
            list (list): Liste des matériels correspondant à la recherche.
        """
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
        """
        Fonction pour rechercher tous les utilisateurs correspondant à un mot clé donné.

        Args:
            cnx (object): Objet de connexion à la base de données.
            search (str): Mot clé à rechercher dans les noms d'utilisateurs.

        Returns:
            list (list): Liste des utilisateurs correspondant à la recherche.
        """
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
        """
        Fonction pour rechercher tous les matériels correspondant à un mot clé donné dans une commande.

        Args:
            cnx (object): Objet de connexion à la base de données.
            idbc (int): Identifiant de la commande.
            search (str): Mot clé à rechercher dans les noms de matériels.

        Returns:
            list (list): Liste des matériels correspondant à la recherche.
        """
        try:
            liste = []
            result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + " and nomMateriel like '%" + search + "%';"))
            result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEt Securite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ") and nomMateriel like '%" + search + "%';"))
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

    def recherche_all_in_inventaire_with_search(cnx, search):
        """
        Fonction pour rechercher tous les matériels correspondant à un mot clé donné dans l'inventaire.

        Args:
            cnx (object): Objet de connexion à la base de données.
            search (str): Mot clé à rechercher dans les noms de matériels.

        Returns:
            list (list): Liste des matériels correspondant à la recherche.
        """
        try:
            list = []
            result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,pictogramme,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock from MATERIEL natural left join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL JOIN RISQUES NATURAL JOIN RISQUE where nomMateriel like '%" + search + "%' ;"))
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
    """
    Classe qui contient des méthodes pour gerer les mots de passe.
    """

    def generer_mot_de_passe():
        """
        Fonction pour générer un mot de passe aléatoire.

        Returns:
            mot_de_passe (str): Mot de passe aléatoire.
        """
        caracteres = string.ascii_letters + string.digits
        mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

        return mot_de_passe

    def hasher_mdp(mdp):
        """
        Fonction pour hasher un mot de passe.

        Args:
            mdp (str): Mot de passe à hasher.

        Returns:
            mdphash (str): Mot de passe hashé.
        """
        m = sha256()
        m.update(mdp.encode("utf-8"))
        return m.hexdigest()

    def recuperation_de_mot_de_passe(cnx, email):
        """
        Fonction pour récupérer un mot de passe.

        Args:
            cnx (object): Objet de connexion à la base de données.
            email (str): Adresse email de l'utilisateur.

        Returns:
            bool: True si la récupération a réussi, False sinon.
        """
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
    """
    Classe qui contient des méthodes pour gerer l'authentification.
    """

    def random_key():
        """
        Fonction pour générer une clé aléatoire pour l'authentification à deux facteurs.

        Returns:
            clé (str): Clé aléatoire pour l'authentification à deux facteurs.
        """
        return pyotp.random_base32()

    def add_two_authenticator_in_bd(cnx, key, email, id):
        """
        Fonction pour ajouter une clé de l'authentification à deux facteurs dans la base de données.

        Args:
            cnx (object): Objet de connexion à la base de données.
            key (str): Clé pour l'authentification à deux facteurs.
            email (str): Adresse email de l'utilisateur.
            id (int): Identifiant de l'utilisateur.
        """
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

    def create_uri(key, email):
        """
        Fonction pour créer une URI pour l'authentification à deux facteurs.

        Args:
            key (str): Clé pour l'authentification à deux facteurs.
            email (str): Adresse email de l'utilisateur.

        Returns:
            uri (str): URI pour l'authentification à deux facteurs.
        """
        cnx = get_cnx()
        Authentification.add_two_authenticator_in_bd(cnx, key, email, Utilisateur.Get.get_id_with_email(cnx, email))
        return pyotp.totp.TOTP(key).provisioning_uri(name= email, issuer_name= "GestLab")

    def create_qr_code_utilisateur_deja_existant(cnx, email):
        """
        Fonction pour créer un code QR pour un utilisateur déjà existant.

        Args:
            cnx (object): Objet de connexion à la base de données.
            email (str): Adresse email de l'utilisateur.
        """
        uri = Utilisateur.Get.get_uri_with_email(cnx, email)
        qrcode.make(uri).save("qrcode.png")

    def create_qr_code_nouvel_utlisateur(email, mdp):
        """
        Fonction pour créer un code QR pour un nouvel utilisateur.

        Args:
            email (str): Adresse email de l'utilisateur.
            mdp (str): Mot de passe de l'utilisateur.
        """
        key = Authentification.random_key()
        uri = Authentification.create_uri(key, email)
        qrcode.make(uri).save("qrcode.png")
        envoyer_mail(email, mdp, key)

    def verify(key, code):
        """
        Fonction pour vérifier si le code de l'authentification à deux facteurs est correct.

        Args:
            key (str): Clé pour l'authentification à deux facteurs.
            code (str): Code de l'authentification à deux facteurs.

        Returns:
            bool: True si le code est correct, False sinon.
        """
        return pyotp.TOTP(key).verify(code)


class Alert:
    """
    Classe qui contient des méthodes pour gerer les alertes.
    """

    def get_nb_alert_id(cnx):
        """
        Fonction pour récupérer le nombre d'alertes avec leur identifiant.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste des identifiants des alertes.
        """
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
        """
        Fonction pour récupérer les informations sur le matériel en cas d'alerte.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste des informations sur le matériel en cas d'alerte.
        """
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
        """
        Fonction pour récupérer le nombre total d'alertes.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            int: Nombre total d'alertes.
        """
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
        """
        Fonction pour récupérer le nombre d'alertes par matériel.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            dict: Dictionnaire avec le nombre d'alertes par matériel.
        """
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
        """
        Fonction pour récupérer le nombre d'alertes par matériel unique.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            dict: Dictionnaire avec le nombre d'alertes par matériel unique.
        """
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
    """
    Représente une demande dans le système.
    """

    class Get:
        """
        Méthodes pour récupérer des informations sur les demandes.
        """
        def get_nb_demande(cnx):
            """
            Cette méthode permet de récupérer le nombre de demandes en attente.
            
            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                int: Le nombre de demandes en attente.
            """
            try:
                result = cnx.execute(text("select nombreDemandesEnAttente();"))
                for row in result:
                    return row[0]
            except Exception as e:
                print("Erreur lors de la récupération du nombre de demandes :", str(e))
                raise
            
        def get_info_demande(cnx):
            """
            Cette méthode permet de récupérer les informations sur les demandes.
            
            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                list: Une liste de tuples contenant les informations sur les demandes.
            """
            try:
                result = cnx.execute(text("SELECT idDemande, nom, prenom from UTILISATEUR natural join DEMANDE;"))
                info_commande = []
                for row in result:
                    info_commande.append(row)
                return info_commande
            except Exception as e:
                print("Erreur lors de la récupération des informations sur les commandes :", str(e))
                raise

        def get_info_demande_with_id(cnx, idDemande):
            """
            Cette méthode permet de récupérer les informations sur une demande spécifique.
            
            Args:
                cnx (object): Objet de connexion à la base de données.
                idDemande (int): L'identifiant de la demande dont on veut récupérer les informations.

            Returns:
                list: Une liste de tuples contenant les informations sur la demande spécifique.
            """
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

    class Delete:
        """
        Méthodes pour supprimer des informations sur les demandes.
        """

        def delete_demande(cnx, idDemande):
            """
            Cette méthode permet de supprimer une demande spécifique.
            
            Args:
                cnx (object): Objet de connexion à la base de données.
                idDemande (int): L'identifiant de la demande à supprimer.
            """
            try:
                print("test")
                cnx.execute(text("DELETE FROM DEMANDE WHERE idDemande = " + str(idDemande) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression de la demande")
                raise

class Categories:
    """
    Cette classe inclut une méthode pour récupérer toutes les catégories.
    """

    def get_categories(cnx):
        """
        Cette méthode retourne toutes les catégories de la base de données.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Une liste de tuples contenant les informations sur les catégories.
        """
        liste = []
        result = cnx.execute(text("select * from CATEGORIE;"))
        for row in result:
            liste.append((row[0],row[2],row[1]))
        return liste

class Domaine:
    """
    Cette classe inclut des méthodes pour récupérer toutes les informations sur un domaine,
    récupérer tous les domaines, et récupérer l'identifiant du domaine à partir d'une catégorie.
    """

    def get_all_info_from_domaine(cnx):
        """
        Cette méthode retourne toutes les informations sur un domaine spécifique.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Une liste de tuples contenant les informations sur le domaine spécifique.
        """
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
        """
        Cette méthode retourne tous les domaines de la base de données.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Une liste de tuples contenant les informations sur les domaines.
        """
        try:
            result = cnx.execute(text("SELECT * from DOMAINE;"))
            info_commande = []
            for row in result:
                info_commande.append(row)
            return info_commande
        except Exception as e:
            print("Erreur lors de la récupération des informations sur les commandes :", str(e))
            raise

    def get_id_domaine_from_categorie(cnx, id_categorie) :
        """
        Cette méthode retourne l'identifiant du domaine à partir d'une catégorie spécifique.

        Args:
            cnx (object): Objet de connexion à la base de données.
            id_categorie (int): L'identifiant de la catégorie.

        Returns:
            int: L'identifiant du domaine.
        """
        try:
            result = cnx.execute(text("SELECT idDomaine FROM CATEGORIE WHERE idCategorie = " + str(id_categorie) + ";"))
            for row in result:
                return row[0]
        except:
            print("Erreur lors de la récupération du domaine")
            raise
class Bon_commande:
    """
    Cette classe inclut des méthodes pour récupérer les informations sur les bons de commande,
    vérifier si un bon de commande existe, et obtenir le numéro maximum d'identifiant de bon de commande.
    """

    class Get:
        """
        Cette classe inclut des méthodes pour récupérer les informations sur les bons de commande.
        """

        def afficher_bon_commande(cnx, idut): #get
            """
            Cette méthode permet d'afficher le contenu d'un bon de commande.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): L'identifiant de l'utilisateur dont on veut récupérer les informations sur le bon de commande.

            Returns:
                list: Une liste de tuples contenant les informations sur le bon de commande.
            """
            try:
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
                result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEt Securite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ");"))
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
            """
            Cette méthode permet de récupérer l'identifiant du bon de commande actuel.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): L'identifiant de l'utilisateur.

            Returns:
                int: L'identifiant du bon de commande actuel.
            """
            try:
                result = cnx.execute(text("SELECT idBonCommande FROM BONCOMMANDE WHERE idUtilisateur = " + str(idut) + " AND idEtat = 1;")) #enlever AND idEtat = 1 si on delete le bon de commande validée
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du bon de commande")
                raise

        def get_bon_commande_with_id(cnx, idbc):
            """
            Cette méthode permet de récupérer toutes les informations sur un bon de commande spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idbc (int): L'identifiant du bon de commande.

            Returns:
                list: Une liste de tuples contenant les informations sur le bon de commande spécifique.
            """
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
            """
            Cette méthode permet de récupérer tous les bons de commande en excluant ceux avec l'état 1 (actif) et 4 (supprimé).

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                list: Une liste de tuples contenant les informations sur les bons de commande.
            """
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
            """
            Cette méthode permet de récupérer tous les bons de commande en fonction de leur état.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idetat (int): L'identifiant de l'état du bon de commande.

            Returns:
                list: Une liste de tuples contenant les informations sur les bons de commande.
            """
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
            """
            Cette méthode permet de récupérer tous les bons de commande en fonction de leur état avec fusion des tables COMMANDE et BONCOMMANDE.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idetat (int): L'identifiant de l'état du bon de commande.

            Returns:
                list: Une liste de tuples contenant les informations sur les bons de commande.
            """
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
            """
            Cette méthode permet de récupérer le numéro maximum d'identifiant de bon de commande.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                int: Le numéro maximum d'identifiant de bon de commande.
            """
            try:
                result = cnx.execute(text("SELECT MAX(idBonCommande) FROM BONCOMMANDE;"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du bon de commande")
                raise

    class Update:
        """
        Cette classe inclut des méthodes pour mettre à jour les données des bons de commande.
        """

        def changer_etat_bonCommande(cnx, idut):
            """
            Cette méthode permet de changer l'état d'un bon de commande en cours.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                None
            """
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
            """
            Cette méthode permet de changer l'état d'un bon de commande en utilisant son identifiant.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idbc (int): Identifiant du bon de commande.
                idetat (int): Identifiant de l'état.

            Returns:
                None
            """
            try:
                cnx.execute(text("UPDATE BONCOMMANDE SET idEtat = " + str(idetat) + " WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors du changement d'état du bon de commande")
                raise

    class Delete:
        """
        Cette classe inclut des méthodes pour supprimer les données des bons de commande.
        """

        def delete_bonCommande_with_id(cnx, idbc):
            """
            Cette méthode permet de supprimer un bon de commande en utilisant son identifiant.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idbc (int): Identifiant du bon de commande.

            Returns:
                None
            """
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.execute(text("DELETE FROM BONCOMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du bon de commande")
                raise

    class Insert:
        """
        Cette classe inclut des méthodes pour insérer des données dans les bons de commande.
        """

        def fusion_bon_commande(cnx, liste_bon_commande, idUt):
            """
            Cette méthode permet de fusionner plusieurs bons de commande en un seul.

            Args:
                cnx (object): Objet de connexion à la base de données.
                liste_bon_commande (list): Liste des bons de commande à fusionner.
                idUt (int): Identifiant de l'utilisateur.

            Returns:
                None
            """
            try:
                # partie bon commande
                id_bon = Bon_commande.Get.get_max_id_bon_commande(cnx) + 1
                cnx.execute(text("INSERT INTO BONCOMMANDE (idBonCommande, idEtat, idUtilisateur) VALUES ("+str(id_bon)+", 2, "+str(idUt)+");"))
                cnx.commit()
                # partie commande
                for commande in liste_bon_commande:
                    if cnx.execute(text("SELECT * FROM COMMANDE WHERE idBonCommande = "+str(id_bon)+" AND idMateriel = "+str(commande[3])+";")).first() is None:
                        cnx.execute(text("INSERT INTO COMMANDE (idBonCommande, idMateriel, quantite) VALUES ("+str(id_bon)+", "+str(commande[3])+", "+str(commande[4])+");"))
                    else:
                        cnx.execute(text("UPDATE COMMANDE SET quantite = quantite + "+str(commande[4])+" WHERE idBonCommande = "+str(id_bon)+" AND idMateriel = "+str(commande[3])+";"))
                    Bon_commande.Delete.delete_bonCommande_with_id(cnx, commande[0])
                    cnx.commit()  
            except:
                print("Erreur lors de l'ajout du bon de commande")
                raise

class Suggestion_materiel:
    """
    Cette classe inclut des méthodes pour récupérer les informations sur les suggestions de matériel.
    """

    def get_all_information_to_Materiel_suggestions(cnx):
        """
        Cette méthode permet de récupérer toutes les informations sur les suggestions de matériel.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Une liste de tuples contenant les informations sur les suggestions de matériel.
        """
        try:
            list = []
            result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,pictogramme,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock from MATERIEL natural left join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL JOIN RISQUES NATURAL JOIN RISQUE ;"))
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
    """
    Cette classe inclut des méthodes pour récupérer des informations sur les matériels.
    """

    def get_MATERIEL(cnx):
        """
        Cette méthode permet d'afficher les matériels disponibles.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            None
        """
        result = cnx.execute(text("select * from RECHERCHEMATERIELS;"))
        for row in result:
            print(row[0])

    def get_info_rechercheMateriel(cnx):
        """
        Cette méthode permet de récupérer les informations sur les matériels disponibles.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste des identifiants des matériels disponibles.
        """
        try:
            result = cnx.execute(text("select * from RECHERCHEMATERIELS;"))
            list = []
            for row in result:
                list.append(row[0])
            return list
        except Exception as e:
            print("Erreur lors de la récupération des informations sur les commandes :", str(e))
            raise

class Rangement:
    """
    Cette classe inclut des méthodes pour récupérer des informations sur les rangements.
    """

    class Get:
        """
        Cette classe inclut des méthodes pour récupérer des informations sur les rangements.
        """

        def get_id_endroit_from_id_rangement(cnx, idRangement) :
            """
            Cette méthode permet de récupérer l'identifiant de l'endroit associé à un rangement spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idRangement (int): Identifiant du rangement.

            Returns:
                int: Identifiant de l'endroit associé au rangement spécifié.
            """
            try:
                result = cnx.execute(text("SELECT idEndroit FROM RANGEMENT WHERE idRangement = " + str(idRangement) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de l'endroit")
                raise

class Commande :
    """
    Cette classe inclut des méthodes pour récupérer des informations sur les commandes.
    """

    class Get:
        """
        Cette classe inclut des méthodes pour récupérer des informations sur les commandes.
        """

        def get_statut_from_commande_with_id_boncommande(cnx, id_boncommande):
            """
            Cette méthode permet de récupérer le statut d'une commande spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id_boncommande (int): Identifiant du bon de commande.

            Returns:
                list: Liste des identifiants des états associés à la commande spécifiée.
            """
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
            """
            Cette méthode permet de récupérer le statut d'une commande spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id_etat (int): Identifiant de l'état.

            Returns:
                list: Liste des identifiants des états associés à la commande spécifiée.
            """
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
            """
            Cette méthode permet de récupérer les informations sur les statuts des commandes disponibles.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                list: Liste des identifiants des états associés aux commandes disponibles.
            """
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
    """
    Cette classe inclut des méthodes pour récupérer des informations sur les stocks laboratoires.
    """

    class Get:
        """
        Cette classe inclut des méthodes pour récupérer des informations sur les stocks laboratoires.
        """

        def get_quantite_with_idMateriel(cnx, idMateriel):
            """
            Cette méthode permet de récupérer la quantité d'un matériel spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMateriel (int): Identifiant du matériel.

            Returns:
                int: Quantité du matériel spécifié.
            """
            try:
                result = cnx.execute(text("SELECT quantiteLaboratoire FROM STOCKLABORATOIRE natural join MATERIEL WHERE idMateriel = " + str(idMateriel) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de la quantité")
                raise

# def get_all_information_to_Materiel(cnx, nomcat=None):
#     my_list = []
#     if nomcat is None:
#         result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire  from MATERIEL natural left join MATERIELUNIQUE natural left join 
# natural left join DOMAINE natural left join CATEGORIE natural join FDS;"))
#         for row in result:
#             print(row[1],row[2],row[6])
#             my_list.append((row[1],row[2],row[6]))
#     else:
#         result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire  from MATERIEL natural left join STOCKLABORATOIRE  natural left join DOMAINE natural left join CATEGORIE natural join FDS where nomCategorie = '" + nomcat + "';"))
#         for row in result:
#             my_list.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
#     return my_list

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

#faire trigger before insert pour que si on ajoute un materiel deja dans la commande, on update la quantite