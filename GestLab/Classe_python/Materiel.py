from sqlalchemy import text
import sqlalchemy

import GestLab.Classe_python.Demande as Demande


class Materiel:
    
    class Get :

        def get_idMateriel_with_nomMateriel(cnx, nomMateriel):
            """
            Récupère l'identifiant du matériel en fonction de son nom.

            Args:
                cnx (object): Objet de connexion à la base de données.
                nomMateriel (str): Nom du matériel.

            Returns:
                int: Identifiant du matériel.

            Raises:
                Exception: Erreur lors de la récupération de l'identifiant du matériel.
            """
            try:
                result = cnx.execute(text("SELECT idMateriel FROM MATERIEL WHERE nomMateriel = '" + nomMateriel + "';"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id du matériel")
                raise

        def get_all_information_to_Materiel_cat_com(cnx):
            """
            Récupère toutes les informations sur le matériel, y compris la catégorie et le domaine associés.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                list: Liste contenant les informations de chaque matériel.
            """
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
            """
            Retrieves all information related to a specific Materiel with the given id.

            Parameters:
            cnx (connection): The database connection.
            id (int): The id of the Materiel.

            Returns:
            tuple: A tuple containing the information of the Materiel.
            """
            try:
                result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL LEFT JOIN CATEGORIE NATURAL LEFT JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL LEFT JOIN RISQUES NATURAL LEFT JOIN RISQUE WHERE idMateriel = " + str(id) + ";"))
                for row in result:
                    return row
            except:
                print("erreur de l'id")
                raise

        def get_all_information_to_Materiel(cnx):
            """
            Récupère toutes les informations sur le matériel disponible dans le laboratoire.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                tuple: Un tuple contenant une liste des informations sur le matériel et le nombre d'éléments dans la liste.
            """
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
            """
            Récupère la liste des matériels existants dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                list: Liste des matériels existants, chaque élément étant un tuple contenant l'id et le nom du matériel.

            Raises:
                Exception: En cas d'erreur lors de la récupération des matériels existants.
            """
            try:
                result = cnx.execute(text("SELECT idMateriel, nomMateriel FROM MATERIEL;"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération des matériels existants")
                raise


        def get_materiel_commande(cnx, idbc):
            """
            Récupère les informations du matériel dans une commande spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idbc (int): Identifiant de la commande.

            Returns:
                list: Liste des informations du matériel dans la commande.

            Raises:
                Exception: Erreur lors de la récupération du matériel dans la commande.
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

        def get_materiel_demande(cnx, idDemande):
            """
            Récupère les informations du matériel demandé dans une demande spécifique.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idDemande (int): L'identifiant de la demande.

            Returns:
                list: Une liste contenant les informations du matériel demandé.
            """
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
            """
            Récupère l'identifiant du matériel à partir de l'identifiant unique du matériel.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id_materiel_unique (int): Identifiant unique du matériel.

            Returns:
                int: Identifiant du matériel.

            Raises:
                Exception: Erreur lors de la récupération de l'identifiant du matériel.
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
            Récupère les informations d'un matériel à partir de son identifiant.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMateriel (int): Identifiant du matériel à récupérer.

            Returns:
                list: Liste contenant les informations du matériel.

            Raises:
                Exception: En cas d'erreur lors de la récupération du matériel.
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
            Récupère tous les matériels pour générer un PDF dans une commande spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                list: Liste des matériels avec leurs informations (nomMateriel, referenceMateriel, nomDomaine, nomCategorie, quantite).

            Raises:
                Exception: Erreur lors de la récupération du matériel dans la commande.
            """
            try:
                idbc = Demande.Bon_commande.Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT nomMateriel, referenceMateriel, nomDomaine,nomCategorie, quantite from COMMANDE NATURAL JOIN MATERIEL NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE WHERE idBonCommande = " + str(idbc) + ";"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise

        def get_all_materiel_for_pdf_in_bon_commande_after(cnx, idbc):
            """
            Récupère les informations sur le matériel pour générer un PDF dans une commande après un certain ID de bon de commande.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idbc (int): ID du bon de commande.

            Returns:
                list: Liste des informations sur le matériel (nomMateriel, referenceMateriel, nomDomaine, nomCategorie, quantite).

            Raises:
                Exception: Erreur lors de la récupération du matériel dans la commande.
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
            
        def get_materiel_in_bonDeCommande(cnx, idut):
            """
            Récupère les informations sur le matériel dans le bon de commande actuel d'un utilisateur.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Returns:
                list: Liste des informations sur le matériel dans le bon de commande.
            
            Raises:
                Exception: Erreur lors de la récupération du matériel dans la commande.
            """
            try:
                idbc = Demande.Bon_commande.Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                result = cnx.execute(text("SELECT idMateriel, nomMateriel,referenceMateriel, quantite FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ";"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du matériel dans la commande")
                raise
            
        def get_nom_dom_cat_materiel_with_id(cnx, id):
            """
            Récupère le nom du domaine et de la catégorie d'un matériel en fonction de son identifiant.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id (int): Identifiant du matériel.

            Returns:
                tuple: Un tuple contenant le nom du domaine et le nom de la catégorie du matériel.

            Raises:
                Exception: En cas d'erreur lors de l'exécution de la requête.
            """
            try:
                result = cnx.execute(text("select nomDomaine,nomCategorie from MATERIEL natural join DOMAINE natural join CATEGORIE where idMateriel = " + str(id) + ";"))
                result = result.first()
                return result
            except:
                print("erreur de l'id")
                raise

    class Delete:

        def delete_materiel_in_BonCommande_whith_id(cnx, idMateriel, idbc):
            """
            Supprime un matériel dans une commande spécifique en utilisant l'identifiant du matériel et l'identifiant de la commande.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMateriel (int): Identifiant du matériel à supprimer.
                idbc (int): Identifiant de la commande dans laquelle supprimer le matériel.

            Raises:
                Exception: Erreur lors de la suppression du matériel dans la commande.

            Returns:
                None
            """
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idMateriel = " + str(idMateriel) + " AND idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_materiel_in_AjouterMateriel_whith_id(cnx, idMateriel, idDemande):
            """
            Supprime un matériel de la table AJOUTERMATERIEL en fonction de son identifiant (idMateriel) et de l'identifiant de la demande (idDemande).

            Args:
                cnx (connection): La connexion à la base de données.
                idMateriel (int): L'identifiant du matériel à supprimer.
                idDemande (int): L'identifiant de la demande associée.

            Returns:
                bool: True si le matériel et la demande ont été supprimés, False sinon.

            Raises:
                Exception: En cas d'erreur lors de la suppression du matériel dans la commande.
            """
            try:
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idMateriel = " + str(idMateriel) + " AND idDemande = " + str(idDemande) + ";"))
                result = cnx.execute(text("SELECT COUNT(*) FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) +  ";"))
                for row in result:
                    nbmat_in_demande = row[0]
                if nbmat_in_demande == 0:
                    Demande.Demande.Delete.delete_demande(cnx,idDemande)
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
            """
            Supprime un matériel de la base de données.

            Args:
                cnx (connection): La connexion à la base de données.
                idMateriel (int): L'identifiant du matériel à supprimer.

            Raises:
                Exception: En cas d'erreur lors de la suppression du matériel.

            """
            try:
                Materiel.Delete.delete_all_materiel_in_Stocklaboratoire_with_idMat(cnx, idMateriel)
                Materiel.Delete.delete_all_materiel_in_Commande_with_idMat(cnx, idMateriel)
                Materiel.Delete.delete_all_materiel_in_AjouterMateriel_with_idMat(cnx, idMateriel)
                Demande.MaterielUnique.Delete.delete_all_materiel_unique_with_idMateriel(cnx, idMateriel)
                cnx.execute(text("DELETE FROM MATERIEL WHERE idMateriel = " + str(idMateriel) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel")
                raise

        def delete_all_materiel_in_commande(cnx, idut):
            """
            Supprime tous les matériels d'une commande spécifique.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Raises:
                Exception: Erreur lors de la suppression du matériel dans la commande.
            """
            try:
                idbc = Demande.Bon_commande.Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
                cnx.execute(text("DELETE FROM COMMANDE WHERE idBonCommande = " + str(idbc) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_all_materiel_in_AjouterMateriel(cnx, idut):
            """
            Supprime tous les matériels dans la table AJOUTERMATERIEL pour une demande donnée.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idut (int): Identifiant de l'utilisateur.

            Raises:
                Exception: Erreur lors de la suppression du matériel dans la commande.

            """
            try:
                idDemande = Demande.Demande.Get.get_id_demande_actuel(cnx, idut)
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_all_materiel_in_AjouterMateriel_with_idMat(cnx, idMat):
            """
            Supprime tous les matériels dans la table AJOUTERMATERIEL avec l'identifiant idMat.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMat (int): Identifiant du matériel à supprimer.

            Raises:
                Exception: Erreur lors de la suppression du matériel dans la commande.
            """
            try:
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idMateriel = " + str(idMat) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise
        
        def delete_all_materiel_in_Commande_with_idMat(cnx, idMat):
            """
            Supprime tous les enregistrements de matériel dans la table COMMANDE
            correspondant à l'identifiant de matériel spécifié.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMat (int): Identifiant du matériel à supprimer.

            Raises:
                Exception: Erreur lors de la suppression du matériel dans la commande.

            """
            try:
                cnx.execute(text("DELETE FROM COMMANDE WHERE idMateriel = " + str(idMat) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans la commande")
                raise

        def delete_all_materiel_in_Stocklaboratoire_with_idMat(cnx, idMat):
            """
            Supprime tous les matériels dans le stock du laboratoire avec l'identifiant idMat.

            Args:
                cnx (connection): La connexion à la base de données.
                idMat (int): L'identifiant du matériel à supprimer.

            Raises:
                Exception: En cas d'erreur lors de la suppression du matériel dans le stock.

            """
            try:
                cnx.execute(text("DELETE FROM STOCKLABORATOIRE WHERE idMateriel = " + str(idMat) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du matériel dans le stock")
                raise
            

    class Update:

        def modifie_materiel(cnx, idMateriel, categorie, nom, reference, caracteristiques, infossup, seuilalerte):
            """
            Modifie les informations d'un matériel dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMateriel (int): L'identifiant du matériel à modifier.
                categorie (int): L'identifiant de la catégorie du matériel.
                nom (str): Le nom du matériel.
                reference (str): La référence du matériel.
                caracteristiques (str): Les caractéristiques complémentaires du matériel.
                infossup (str): Les informations complémentaires et de sécurité du matériel.
                seuilalerte (str): Le seuil d'alerte du matériel.

            Returns:
                bool: True si la modification a réussi, False sinon.

            Raises:
                Exception: En cas d'erreur lors de la modification du matériel.
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


        def set_all_quantite_from_ajouterMat_to_boncommande(cnx, idDemande, idut, boolajouterMat=False):
            """
            Met à jour la quantité dans la demande en transférant les matériels ajoutés vers la commande.

            :param cnx: La connexion à la base de données.
            :param idDemande: L'identifiant de la demande.
            :param idut: L'identifiant de l'utilisateur.
            :param boolajouterMat: Indique si les matériels sont ajoutés ou non. Par défaut, False.
            """
            try:
                result = cnx.execute(text("SELECT idMateriel,quantite from AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + ";"))
                for row in result:
                    Materiel.Insert.ajout_materiel_in_commande(cnx, row[0], idut, row[1], boolajouterMat)
                    Demande.MaterielUnique.Delete.delete_materiel_unique_in_demande(cnx, idDemande, row[0])
            except:
                print("Erreur lors de la mise à jour de la quantité dans la demande")
                raise
            



    class Insert: 

        def insere_materiel(
            cnx, idCategorie, nomMateriel, referenceMateriel,
            caracteristiquesComplementaires, informationsComplementairesEtSecurite, seuilAlerte
        ):
            """
            Insère un nouveau matériel dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idCategorie (int): L'identifiant de la catégorie du matériel.
                nomMateriel (str): Le nom du matériel.
                referenceMateriel (str): La référence du matériel.
                caracteristiquesComplementaires (str): Les caractéristiques complémentaires du matériel.
                informationsComplementairesEtSecurite (str): Les informations complémentaires et de sécurité du matériel.
                seuilAlerte (str): Le seuil d'alerte du matériel.

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
            Ajoute ou met à jour un matériel dans une commande.

            Args:
                cnx (connection): La connexion à la base de données.
                idmat (int): L'identifiant du matériel.
                idut (int): L'identifiant de l'utilisateur.
                quantite (int): La quantité du matériel.
                boolajouterMat (bool): Indique si le matériel doit être ajouté ou mis à jour.

            Raises:
                Exception: En cas d'erreur lors de l'ajout du matériel dans la commande.

            """
            try:
                idbc = Demande.Bon_commande.Bon_commande.Get.get_id_bonCommande_actuel(cnx, idut)
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
            """
            Ajoute ou met à jour la quantité de matériel dans la demande d'ajout de matériel.

            Args:
                cnx (connection): La connexion à la base de données.
                idmat (int): L'identifiant du matériel.
                idut (int): L'identifiant de l'utilisateur.
                quantite (int): La quantité de matériel à ajouter ou mettre à jour.
                boolajouterMat (bool): Indique si le matériel doit être ajouté ou mis à jour.

            Raises:
                Exception: En cas d'erreur lors de l'ajout du matériel dans la commande.

            """
            try:
                idDemande = Demande.Demande.Get.get_id_demande_actuel(cnx, idut)
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
    