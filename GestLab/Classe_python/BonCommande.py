from sqlalchemy import text

from GestLab.Classe_python.Date import DATE
from GestLab.Classe_python.Domaine import Domaine
import GestLab.Classe_python.Utilisateurs as Utilisateur


class Bon_commande:
    
    class Get:
        
        def afficher_bon_commande(cnx, idut):
            """
            Affiche les informations du bon de commande actuel pour un utilisateur donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                list: Liste des informations du bon de commande actuel.
            """
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

        def get_nb_bon_commande(cnx, idbc):
            try:
                nb = cnx.execute(text("SELECT COUNT(*) FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
                for row in nb:
                    return row[0]
                return 0
            except:
                print("Erreur lors de la récupération du nombre de suggestions")
                raise

            
        def get_id_bonCommande_actuel(cnx, idut):
            """
            Récupère l'identifiant du bon de commande actuel pour un utilisateur donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                int: L'identifiant du bon de commande actuel.

            Raises:
                Exception: En cas d'erreur lors de la récupération de l'identifiant du bon de commande.
            """
            try:
                result = cnx.execute(text("SELECT idBonCommande FROM BONCOMMANDE WHERE idUtilisateur = " + str(idut) + " AND idEtat = 1;")) #enlever  AND idEtat = 1 si on delete le bon de commande validée
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du bon de commande")
                raise
            
        def get_bon_commande_with_id(cnx, idbc):
            """
            Récupère les informations du bon de commande avec l'identifiant spécifié.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idbc (int): Identifiant du bon de commande.

            Returns:
                list: Liste des informations du bon de commande.
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
            Cette fonction permet de consulter les bons de commande qui ne sont pas dans les états 1 et 4.

            Args:
                cnx (object): L'objet de connexion à la base de données.

            Returns:
                list: Une liste contenant les bons de commande récupérés.
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
            Récupère les bons de commande avec un certain statut.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idetat (int): Identifiant du statut des bons de commande à récupérer.

            Returns:
                list: Liste des bons de commande correspondant au statut donné.
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
            Récupère les bons de commande avec un statut de fusion donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idetat (int): Identifiant du statut de fusion.

            Returns:
                list: Liste des bons de commande correspondants.

            Raises:
                Exception: Erreur lors de la récupération des commandes.
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
            Récupère l'ID maximum du bon de commande dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                int: L'ID maximum du bon de commande.
                
            Raises:
                Exception: En cas d'erreur lors de la récupération de l'ID du bon de commande.
            """
            try:
                result = cnx.execute(text("SELECT MAX(idBonCommande) FROM BONCOMMANDE;"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du bon de commande")
                raise
            
    class Update:
        
        def changer_etat_bonCommande(cnx, idut):
            """
            Change l'état du bon de commande dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Raises:
                Exception: Erreur lors du changement d'état du bon de commande.

            """
            try:
                idetat = 2
                idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                cnx.execute(text("UPDATE BONCOMMANDE SET idEtat = " + str(idetat) + " WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
                Utilisateur.Utilisateur.Insert.ajout_gest_into_boncommande(cnx,idut)
            except:
                print("Erreur lors du changement d'état du bon de commande")
                raise

        def changer_etat_bonCommande_with_id(cnx, idbc, idetat):
            """
            Change l'état d'un bon de commande avec l'identifiant spécifié.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idbc (int): L'identifiant du bon de commande.
                idetat (int): L'identifiant de l'état à assigner au bon de commande.

            Raises:
                Exception: En cas d'erreur lors du changement d'état du bon de commande.

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
        
        def delete_bonCommande_with_id(cnx, idbc):
            """
            Supprime un bon de commande avec l'identifiant spécifié.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idbc (int): Identifiant du bon de commande à supprimer.

            Raises:
                Exception: Erreur lors de la suppression du bon de commande.

            """
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.execute(text("DELETE FROM BONCOMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du bon de commande")
                raise

    class Insert:

        def fusion_bon_commande(cnx, liste_bon_commande, idUt):
            """
            Fusionne les bons de commande avec la base de données.

            Args:
                cnx (connection): La connexion à la base de données.
                liste_bon_commande (list): La liste des bons de commande à fusionner.
                idUt (int): L'identifiant de l'utilisateur.

            Raises:
                Exception: En cas d'erreur lors de l'ajout du bon de commande.

            """
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