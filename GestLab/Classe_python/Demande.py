from sqlalchemy import text
import GestLab.Classe_python.BonCommande as Bon_commande

from GestLab.Classe_python.Materiel import Materiel
from GestLab.Classe_python.MaterielUnique import MaterielUnique


class Demande : 
    
    class Get:

        def get_id_demande_actuel(cnx, idut):
            """
            Récupère l'identifiant de la demande actuelle pour un utilisateur donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                int: Identifiant de la demande actuelle.

            Raises:
                Exception: Erreur lors de la récupération de l'identifiant de la demande.
            """
            try:
                result = cnx.execute(text("SELECT idDemande FROM DEMANDE WHERE idUtilisateur = " + str(idut) + " AND idEtatD = 1;"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de la demande")
                raise
        
        def get_nb_demande(cnx):
            """
            Récupère le nombre de demandes ayant l'étatD égal à 2.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                int: Le nombre de demandes ayant l'étatD égal à 2.

            Raises:
                Exception: En cas d'erreur lors de la récupération du nombre de demandes.
            """
            try:
                result = cnx.execute(text("SELECT COUNT(DEMANDE.idDemande) FROM DEMANDE WHERE DEMANDE.idEtatD = 2;"))
                for row in result:
                    return row[0]
            except Exception as e:
                print("Erreur lors de la récupération du nombre de demandes :", str(e))
                raise
            
        def get_info_demande(cnx):
            """
            Récupère les informations des demandes en attente de validation.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                list: Liste contenant les informations des demandes en attente de validation.
                
            Raises:
                Exception: En cas d'erreur lors de la récupération des informations sur les demandes.
            """
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
            """
            Récupère les informations d'une demande spécifique à partir de son identifiant.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idDemande (int): Identifiant de la demande.

            Returns:
                list: Liste contenant les informations de la demande sous forme de tuples.
                    Chaque tuple contient les éléments suivants :
                    - nom (str) : Nom de l'utilisateur associé à la demande.
                    - prenom (str) : Prénom de l'utilisateur associé à la demande.
                    - quantite (int) : Quantité demandée.
                    - nomMateriel (str) : Nom du matériel demandé.
                    - idMateriel (int) : Identifiant du matériel demandé.
                    - referenceMateriel (str) : Référence du matériel demandé.
                    - cpt (int) : Nombre de matériel unique associé au matériel demandé.

            Raises:
                Exception: En cas d'erreur lors de la récupération des informations sur les commandes.
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

        def get_demande_with_statut(cnx, idetat):
            """
            Récupère les demandes avec un statut donné.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idetat (int): L'identifiant du statut.

            Returns:
                list: Une liste contenant les demandes correspondantes.
            """
            try:
                list = []
                result = cnx.execute(text("SELECT * FROM DEMANDE WHERE idEtatD = " + str(idetat) + ";"))
                for row in result:
                    list.append(row)
                return list
            except:
                print("Erreur lors de la récupération des commandes")
                raise

        def afficher_demande(cnx, idut):
            """
            Affiche les demandes de matériel pour un utilisateur donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                list: Liste des demandes de matériel, contenant les informations suivantes pour chaque demande:
                    - idMateriel (int): Identifiant du matériel.
                    - nomMateriel (str): Nom du matériel.
                    - caracteristiquesComplementaires (str): Caractéristiques complémentaires du matériel.
                    - referenceMateriel (str): Référence du matériel.
                    - quantite (int): Quantité demandée.
                    - informationsComplementairesEtSecurite (str): Informations complémentaires et de sécurité du matériel.
                    - idDomaine (int): Identifiant du domaine du matériel.
            """
            try:
                idD = Demande.Get.get_id_demande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idD) + ";"))
                result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idD) + ");"))
                liste = []
                for row in result:
                    idDomaine = Bon_commande.Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                for row in result2:
                    idDomaine = Bon_commande.Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                return liste
            except:
                print("Erreur lors de l'affichage de la table")
                raise

        def afficher_demande_pagination(cnx, idut, start, limite):
            """
            Affiche les demandes de matériel pour un utilisateur donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                list: Liste des demandes de matériel, contenant les informations suivantes pour chaque demande:
                    - idMateriel (int): Identifiant du matériel.
                    - nomMateriel (str): Nom du matériel.
                    - caracteristiquesComplementaires (str): Caractéristiques complémentaires du matériel.
                    - referenceMateriel (str): Référence du matériel.
                    - quantite (int): Quantité demandée.
                    - informationsComplementairesEtSecurite (str): Informations complémentaires et de sécurité du matériel.
                    - idDomaine (int): Identifiant du domaine du matériel.
            """
            try:
                idD = Demande.Get.get_id_demande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idD) + " LIMIT " + str(limite) + " OFFSET " + str(start) + ";"))
                result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idD) + ")" + " LIMIT " + str(limite) + " OFFSET " + str(start) + ";"))
                liste = []

                for row in result:
                    idDomaine = Bon_commande.Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                for row in result2:
                    idDomaine = Bon_commande.Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
                return liste
            except:
                print("Erreur lors de l'affichage de la table")
                raise
        def get_nb_sugestions(cnx, idD):
            try:
                nb = cnx.execute(text("SELECT COUNT(*) FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idD) + ";"))
                for row in nb:
                    return row[0]
                return 0
            except:
                print("Erreur lors de la récupération du nombre de suggestions")
                raise
                
    class Update:
        def tout_commander_with_idDemmande_and_idUt(cnx, idDemande, idUt):
            """
            Effectue une commande de tous les matériels d'une demande spécifique pour un utilisateur spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idDemande (int): Identifiant de la demande.
                idUt (int): Identifiant de l'utilisateur.

            Raises:
                Exception: Erreur lors de la mise à jour de la quantité dans la demande.

            """
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
        
        def delete_demande(cnx, idDemande):
            """
            Supprime une demande de la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idDemande (int): Identifiant de la demande à supprimer.

            Raises:
                Exception: Erreur lors de la suppression de la demande.

            Returns:
                None
            """
            try:
                print("test")
                cnx.execute(text("DELETE FROM DEMANDE WHERE idDemande = " + str(idDemande) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression de la demande")
                raise

        def delete_materiel_demande(cnx, idut, idMateriel):
            """
            Supprime un matériel de la demande actuelle d'un utilisateur.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idut (int): L'identifiant de l'utilisateur.
                idMateriel (int): L'identifiant du matériel à supprimer.

            Raises:
                Exception: En cas d'erreur lors de la suppression du matériel dans la demande.

            """
            try:
                idDemande = Demande.Get.get_id_demande_actuel(cnx, idut)
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idMateriel) + ";"))        
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la demande")
                raise

    class Insert:

        def changer_etat_demande(cnx, idut):
            """
            Modifie l'état d'une demande dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Raises:
                Exception: Erreur lors de la modification de l'état de la demande.

            """
            try:
                idDemande = Demande.Get.get_id_demande_actuel(cnx, idut)
                cnx.execute(text("UPDATE DEMANDE SET idEtatD = 2 WHERE idDemande = " + str(idDemande) + ";"))
                cnx.commit()
                Bon_commande.Utilisateur.Utilisateur.Insert.ajout_laborantin_into_demande(cnx, idut)
            except:
                print("Erreur lors de la modification de l'état de la demande")
                raise

        