from sqlalchemy import text

from  GestLab.Classe_python.Date import DATE
from  GestLab.Classe_python.MotDePasse import Mots_de_passe
import  GestLab.Classe_python.Authentification as Authentification
import  GestLab.Classe_python.Demande as Demande


class Utilisateur:
    
    class Get :

        def get_nom_whith_email(cnx, email):
            """
            Récupère le nom de l'utilisateur correspondant à l'adresse e-mail donnée.

            Args:
                cnx (object): Objet de connexion à la base de données.
                email (str): Adresse e-mail de l'utilisateur.

            Returns:
                str: Nom de l'utilisateur correspondant à l'adresse e-mail donnée.
            """
            result = cnx.execute(text("select nom from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                print(row[0])
            return row[0]

        def get_id_utilisateur_from_email(cnx, email) :
            """
            Récupère l'identifiant de l'utilisateur à partir de son adresse e-mail.

            Args:
                cnx (object): Objet de connexion à la base de données.
                email (str): Adresse e-mail de l'utilisateur.

            Returns:
                int: L'identifiant de l'utilisateur.

            Raises:
                Exception: Erreur lors de la récupération de l'id de l'utilisateur.
            """
            try:
                result = cnx.execute(text("SELECT idUtilisateur FROM UTILISATEUR WHERE email = '" + email + "';"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de l'utilisateur")
                raise

        def get_password_with_email(cnx, email):
            """
            Retrieve the password associated with the given email from the UTILISATEUR table.

            Parameters:
            - cnx: The database connection object.
            - email: The email address of the user.

            Returns:
            - The password associated with the given email.
            """
            result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                return row[0]
            
        def get_nom_and_statut_and_email(cnx, email):
            """
            Récupère le nom, le statut et l'email d'un utilisateur à partir de son adresse email.

            Args:
                cnx (object): Objet de connexion à la base de données.
                email (str): Adresse email de l'utilisateur.

            Returns:
                tuple: Un tuple contenant le nom, le statut, l'email et le prénom de l'utilisateur.
            """
            result = cnx.execute(text("select nom, idStatut, prenom from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                print(row[0], row[1], row[2], email)
                return (row[0], row[1], email, row[2])

 
        def get_user_with_statut(cnx, nomStatut):
            """
            Récupère les utilisateurs ayant un statut donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                nomStatut (str): Nom du statut recherché.

            Returns:
                list: Liste des utilisateurs ayant le statut donné.
            """
            liste = []
            result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where nomStatut = '" + str(nomStatut) + "';"))
            for row in result:
                liste.append((row[4]))
            return liste

         
        def get_all_user(cnx, idStatut=None):
            """
            Récupère tous les utilisateurs de la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idStatut (int, optional): Identifiant du statut des utilisateurs à filtrer. Par défaut, tous les statuts sont inclus.

            Returns:
                tuple: Un tuple contenant une liste des utilisateurs et le nombre total d'utilisateurs.
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
            Récupère l'URI associée à l'email donné à partir de la table 2FA.

            Paramètres:
                cnx (object): L'objet de connexion à la base de données.
                email (str): L'email pour lequel récupérer l'URI.

            Retour:
                str: L'URI associée à l'email donné.
            """
            result = cnx.execute(text("select uri from 2FA where email = '" + email + "';"))
            for row in result:
                print(row[0])
                return row[0]
            
        def get_id_with_email(cnx, email):
            """
            Récupère l'identifiant de l'utilisateur correspondant à l'adresse e-mail donnée.

            Args:
                cnx (object): Objet de connexion à la base de données.
                email (str): Adresse e-mail de l'utilisateur.

            Returns:
                int: Identifiant de l'utilisateur correspondant à l'adresse e-mail donnée.
            """
            result = cnx.execute(text("select idUtilisateur from UTILISATEUR where email = '" + email + "';"))
            for row in result:
                return row[0]
            
        def get_all_information_utilisateur_with_id(cnx, id):
            """
            Récupère toutes les informations d'un utilisateur avec l'ID spécifié.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id (int): ID de l'utilisateur.

            Returns:
                tuple: Un tuple contenant les informations de l'utilisateur (nom, prénom, email, nomStatut).

            Raises:
                Exception: Si une erreur se produit lors de l'exécution de la requête.
            """
            try:
                result = cnx.execute(text("select nom,prenom,email,nomStatut from UTILISATEUR natural join STATUT where idUtilisateur = " + str(id) + ";"))
                for row in result:
                    return row
            except:
                print("erreur de l'id")
                raise

        def get_statut_with_idDemande(cnx, idDemande):
            """
            Récupère le statut de l'utilisateur qui a fait la demande.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idDemande (int): Identifiant de la demande.

            Returns:
                str: Le statut de l'utilisateur qui a fait la demande.
            """
            result = cnx.execute(text("select idStatut from UTILISATEUR natural join STATUT natural join DEMANDE where idDemande = " + str(idDemande) + ";"))
            for row in result:
                return int(row[0])
           
    class Update:
        
        def update_email_utilisateur(cnx,new_email,nom,mdp, old_email):
            """
            Met à jour l'email d'un utilisateur dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                new_email (str): Le nouvel email de l'utilisateur.
                nom (str): Le nom de l'utilisateur.
                mdp (str): Le mot de passe de l'utilisateur.
                old_email (str): L'ancien email de l'utilisateur.

            Returns:
                bool: True si la mise à jour a réussi, False sinon.
            """
            try:
                Utilisateur.Update.update_email_utilisateur_in_ut(cnx, new_email, nom, mdp)
                Utilisateur.Update.update_email_utilisateur_in_2fa(cnx, old_email,new_email)
                print("email mis a jour")
                return True
            except:
                print("erreur de mise a jour de l'email")
                return False


        def update_email_utilisateur_in_ut(cnx, new_email, nom, mdp):
            """
            Met à jour l'email d'un utilisateur dans la table UTILISATEUR.

            Args:
                cnx (object): Objet de connexion à la base de données.
                new_email (str): Nouvelle adresse email de l'utilisateur.
                nom (str): Nom de l'utilisateur.
                mdp (str): Mot de passe de l'utilisateur.

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
            try:
                cnx.execute(text("update 2FA set email = '" + new_email + "' where email = '" + old_email + "';"))
                cnx.commit()
                print("email mis a jour")
                return True
            except:
                print("erreur de mise a jour de l'email")
                return False
         
        def modification_droit_utilisateur(cnx, idut, idSt):
            """
            Modifie les droits d'un utilisateur dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idut (int): L'identifiant de l'utilisateur.
                idSt (int): L'identifiant du statut à attribuer à l'utilisateur.

            Raises:
                Exception: En cas d'erreur lors de la mise à jour des droits.

            Returns:
                None
            """
            try:
                bonCommande = cnx.execute(text("select idBonCommande from BONCOMMANDE where idUtilisateur = '" + str(idut) + "' and idEtat = 1;"))
                for row in bonCommande:
                    cnx.execute(text("delete from COMMANDE where idBonCommande = '" + str(row[0]) + "';"))
                    Demande.Bon_commande.Bon_commande.Delete.delete_bonCommande_with_id(cnx,row[0])
                    print("bon de commande supprimé")

                demande = cnx.execute(text("select idDemande from DEMANDE where idUtilisateur = '" + str(idut) + "' and idEtatD = 1;"))
                for row in demande:
                    cnx.execute(text("delete from AJOUTERMATERIEL where idDemande = '" + str(row[0]) + "';"))
                    Demande.Demande.Delete.delete_demande(cnx,row[0])
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

        def update_mdp_utilisateur(cnx, email, mdp, new_mdp):
            """
            Met à jour le mot de passe d'un utilisateur dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                email (str): L'adresse e-mail de l'utilisateur.
                mdp (str): Le mot de passe actuel de l'utilisateur.
                new_mdp (str): Le nouveau mot de passe de l'utilisateur.

            Returns:
                bool: True si la mise à jour du mot de passe a réussi, False si le mot de passe actuel est incorrect, None en cas d'erreur.
            """
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
            """
            Met à jour le nom d'un utilisateur dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                email (str): L'email de l'utilisateur.
                new_nom (str): Le nouveau nom de l'utilisateur.

            Raises:
                Exception: En cas d'erreur lors de la mise à jour du nom.

            Returns:
                None
            """
            try:
                cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "';"))
                cnx.commit()
                print("nom mis a jour")
            except:
                print("erreur de mise a jour du nom")
                raise

         
        def update_prenom_utilisateur(cnx, email, new_prenom):
            """
            Met à jour le prénom d'un utilisateur dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                email (str): Adresse email de l'utilisateur.
                new_prenom (str): Nouveau prénom de l'utilisateur.

            Raises:
                Exception: En cas d'erreur lors de la mise à jour du prénom.

            Returns:
                None
            """
            try:
                cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "';"))
                cnx.commit()
                print("prenom mis a jour")
            except:
                print("erreur de mise a jour du prenom")
                raise

        def update_all_information_utillisateur_with_id(cnx, id, idStatut, nom, prenom, email):
            """
            Met à jour toutes les informations d'un utilisateur avec un identifiant donné.

            :param cnx: La connexion à la base de données.
            :type cnx: object
            :param id: L'identifiant de l'utilisateur.
            :type id: int
            :param idStatut: L'identifiant du statut de l'utilisateur.
            :type idStatut: int
            :param nom: Le nouveau nom de l'utilisateur.
            :type nom: str
            :param prenom: Le nouveau prénom de l'utilisateur.
            :type prenom: str
            :param email: Le nouvel email de l'utilisateur.
            :type email: str
            :return: True si la mise à jour a réussi, False sinon.
            :rtype: bool
            """
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

        def ajout_fournisseur(cnx, nom, adresse, mail, tel):
            """
            Ajoute un fournisseur à la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                nom (str): Le nom du fournisseur.
                adresse (str): L'adresse du fournisseur.
                mail (str): L'adresse e-mail du fournisseur.
                tel (str): Le numéro de téléphone du fournisseur.

            Raises:
                Exception: En cas d'erreur lors de l'ajout du fournisseur.

            Returns:
                None
            """
            try:
                cnx.execute(text("insert into FOURNISSEUR (nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values ('" + nom + "', '" + adresse + "', '" + mail + "', '" + tel + "');"))
                cnx.commit()
                print("fournisseur ajouté")
            except:
                print("erreur d'ajout du fournisseur")
                raise

        
        def ajout_gest_into_boncommande(cnx, id):
            """
            Ajoute un bon de commande dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id (int): Identifiant de l'utilisateur.

            Raises:
                Exception: En cas d'erreur lors de l'ajout du bon de commande.

            Returns:
                None
            """
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
            """
            Ajoute un laborantin dans la table DEMANDE.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idut (int): L'identifiant de l'utilisateur.

            Raises:
                Exception: En cas d'erreur lors de l'ajout de la demande.

            Returns:
                None
            """
            try:
                etat = 1
                cnx.execute(text("INSERT INTO DEMANDE (idUtilisateur, idEtatD) VALUES (" + str(idut) + ", " + str(etat) + ");")) 
                cnx.commit()
                print("Demande ajoutée")
            except:
                print("erreur d'ajout de la demande")
                raise
            
        def ajout_professeur(cnx, nom, prenom, email):
            """
            Ajoute un professeur à la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                nom (str): Le nom du professeur.
                prenom (str): Le prénom du professeur.
                email (str): L'email du professeur.

            Returns:
                bool: True si l'ajout a réussi, False sinon.
            """
            try:
                idStatut = 2
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
                cnx.commit()
                Authentification.Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False

        def ajout_gestionnaire(cnx, nom, prenom, email):
            """
            Ajoute un gestionnaire dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                nom (str): Nom du gestionnaire.
                prenom (str): Prénom du gestionnaire.
                email (str): Adresse email du gestionnaire.

            Returns:
                bool: True si l'ajout a réussi, False sinon.
            """
            try:
                idStatut = 4
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
                cnx.commit()
                id = Utilisateur.Get.get_id_with_email(cnx, email)
                Utilisateur.Insert.ajout_gest_into_boncommande(cnx,id)
                Authentification.Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False
        
        def ajout_administrateur(cnx, nom, prenom, email):
            """
            Ajoute un nouvel administrateur dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                nom (str): Le nom de l'administrateur.
                prenom (str): Le prénom de l'administrateur.
                email (str): L'email de l'administrateur.

            Returns:
                bool: True si l'administrateur a été ajouté avec succès, False sinon.
            """
            try:
                idStatut = 1
                mdpRandom = Mots_de_passe.generer_mot_de_passe()
                # envoyer mail avec mdpRandom
                print(mdpRandom)
                mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
                cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "');"))
                cnx.commit()
                Authentification.Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False


        def ajout_laborantin(cnx, nom, prenom, email):
            """
            Ajoute un laborantin dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                nom (str): Le nom du laborantin.
                prenom (str): Le prénom du laborantin.
                email (str): L'email du laborantin.

            Returns:
                bool: True si l'ajout a réussi, False sinon.
            """
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
                Authentification.Authentification.create_qr_code_nouvel_utlisateur(email, mdpRandom)
                print("utilisateur ajouté")
                return True
            except:
                print("erreur d'ajout de l'utilisateur")
                return False
                
    class Delete:
            
            def delete_utilisateur(cnx, idut):
                """
                Supprime un utilisateur de la base de données.

                Args:
                    cnx (object): Objet de connexion à la base de données.
                    idut (int): Identifiant de l'utilisateur à supprimer.

                Raises:
                    Exception: En cas d'erreur lors de la suppression de l'utilisateur.

                Returns:
                    None
                """
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
                """
                Supprime un utilisateur de la base de données en utilisant son adresse e-mail.

                Args:
                    cnx (object): L'objet de connexion à la base de données.
                    email (str): L'adresse e-mail de l'utilisateur à supprimer.

                Raises:
                    Exception: En cas d'erreur lors de la suppression de l'utilisateur.

                Returns:
                    None
                """
                try:
                    cnx.execute(text("delete from UTILISATEUR where email = '" + email + "';"))
                    cnx.commit()
                    print("utilisateur supprimé")
                except:
                    print("erreur de suppression de l'utilisateur")
                    raise
    
    class TestCrud:
        class Insert:

            def test_insert(cnx):
                """
                Teste l'ajout d'un utilisateur dans la base de données.

                Args:
                    cnx (object): Objet de connexion à la base de données.

                Returns:
                    bool: True si le test a réussi, False sinon.
                """
                input_nom = input("Entrez le nom de l'utilisateur à ajouter : ")
                input_prenom = input("Entrez le prénom de l'utilisateur à ajouter : ")
                input_email = input("Entrez l'adresse e-mail de l'utilisateur à ajouter : ")
                input_statut = input("Entrez le statut de l'utilisateur à ajouter. \n1 : Administrateur\n2 : Professeur\n3 : Laborantin\n4 : Gestionnaire\n\n Votre choix : ")  

                def switch(input_statut, input_nom, input_prenom, input_email):
                    switcher = {
                        1: Utilisateur.Insert.ajout_administrateur(cnx, input_nom, input_prenom, input_email),
                        2: Utilisateur.Insert.ajout_professeur(cnx, input_nom, input_prenom, input_email),
                        3: Utilisateur.Insert.ajout_laborantin(cnx, input_nom, input_prenom, input_email),
                        4: Utilisateur.Insert.ajout_gestionnaire(cnx, input_nom, input_prenom, input_email)
                    }
                    return switcher.get(input_statut, "Statut invalide")
                
                switch(input_statut, input_nom, input_prenom, input_email)

                if Utilisateur.Get.get_id_utilisateur_from_email(cnx, input_email) is not None:
                    print("Utilisateur ajouté avec succès")
                    print("Test réussi")
                    return True
                else:
                    print("Erreur lors de l'ajout de l'utilisateur")
                    print("Test échoué")
                    return False
                
        class Delete:

            def test_delete(cnx):
                """
                Teste la suppression d'un utilisateur de la base de données.

                Args:
                    cnx (object): Objet de connexion à la base de données.

                Returns:
                    bool: True si le test a réussi, False sinon.
                """
                input_email = input("Entrez l'adresse e-mail de l'utilisateur à supprimer : ")
                Utilisateur.Delete.delete_utilisateur_with_email(cnx, input_email)

                if Utilisateur.Get.get_id_utilisateur_from_email(cnx, input_email) is None:
                    print("Utilisateur supprimé avec succès")
                    print("Test réussi")
                    return True
                else:
                    print("Erreur lors de la suppression de l'utilisateur")
                    print("Test échoué")
                    return False
                
        class Update:

            def test_update(cnx):
                """
                Teste la mise à jour des informations d'un utilisateur dans la base de données.

                Args:
                    cnx (object): Objet de connexion à la base de données.

                Returns:
                    bool: True si le test a réussi, False sinon.
                """
                input_email = input("Entrez l'adresse e-mail de l'utilisateur à mettre à jour : ")
                input_nom = input("Entrez le nouveau nom de l'utilisateur : ")
                input_prenom = input("Entrez le nouveau prénom de l'utilisateur : ")
                input_mdp = input("Entrez le mot de passe actuel de l'utilisateur : ")
                input_new_mdp = input("Entrez le nouveau mot de passe de l'utilisateur : ")
                input_new_email = input("Entrez la nouvelle adresse e-mail de l'utilisateur : ")

                if Utilisateur.Update.update_email_utilisateur(cnx, input_new_email, input_nom, input_mdp, input_email) and Utilisateur.Update.update_mdp_utilisateur(cnx, input_email, input_mdp, input_new_mdp) and Utilisateur.Update.update_nom_utilisateur(cnx, input_email, input_nom) and Utilisateur.Update.update_prenom_utilisateur(cnx, input_email, input_prenom):
                    print("Utilisateur mis à jour avec succès")
                    print("Test réussi")
                    return True
                else:
                    print("Erreur lors de la mise à jour de l'utilisateur")
                    print("Test échoué")
                    return False
                
                
                
                