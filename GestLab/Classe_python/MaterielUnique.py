from sqlalchemy import text
import sqlalchemy
import GestLab.Classe_python.Materiel as Materiel 



class MaterielUnique:
    
    class Get:
        
        def get_materiel_unique(cnx, idMaterielUnique) :
            """
            Récupère les informations d'un matériel unique à partir de son identifiant.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMaterielUnique (int): Identifiant du matériel unique.

            Returns:
                list: Liste contenant les informations du matériel unique.

            Raises:
                Exception: En cas d'erreur lors de la récupération du matériel unique.
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
            Récupère le nombre de matériel unique dans une demande spécifiée.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idDemande (int): L'identifiant de la demande.

            Returns:
                int: Le nombre de matériel unique dans la demande.

            Raises:
                Exception: En cas d'erreur lors de la récupération du nombre de matériel unique dans la demande.
            """
            try:
                result = cnx.execute(text("SELECT COUNT(*) FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) +  ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération du nombre de matériel unique dans la demande")
                raise
            
        def get_all_information_to_MaterielUnique_with_id(cnx, id):
            """
            Récupère toutes les informations d'un matériel unique avec un identifiant donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id (int): Identifiant du matériel unique.

            Returns:
                tuple: Tuple contenant une liste des informations du matériel unique et la taille de la liste.
            """
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
            """
            Renvoie le nombre de matériels uniques associés à un identifiant donné.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id (int): L'identifiant du matériel.

            Returns:
                int: Le nombre de matériels uniques associés à l'identifiant donné.
            """
            try:
                result = cnx.execute(text("select count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
                for row in result:
                    return row[0]
            except:
                print("erreur de l'id")
            raise

        def get_last_id(cnx):
            """
            Récupère le dernier identifiant de matériel unique dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                int: Dernier identifiant de matériel unique.
            """
            try:
                result = cnx.execute(text("SELECT idMaterielUnique FROM MATERIELUNIQUE ORDER BY idMaterielUnique DESC LIMIT 1 ;"))
                for row in result:
                    return row[0]
            except:
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
            """
            Supprime un matériel unique d'une demande spécifique.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idDemande (int): L'identifiant de la demande.
                idMateriel (int): L'identifiant du matériel unique.

            Raises:
                Exception: En cas d'erreur lors de la suppression du matériel unique dans la demande.

            """
            try:
                cnx.execute(text("DELETE FROM AJOUTERMATERIEL WHERE idDemande = " + str(idDemande) + " AND idMateriel = " + str(idMateriel) + ";"))
                cnx.commit()
                nbmat_in_demande = MaterielUnique.Get.get_nb_materiel_unique_in_demande(cnx, idDemande)
                if nbmat_in_demande == 0:
                    Materiel.Demande.Demande.Delete.delete_demande(cnx,idDemande)
            except:
                print("Erreur lors de la suppression du matériel unique dans la demande")
                raise
            
        def supprimer_materiel_unique_bdd(cnx, id_materiel_unique) :
            """
            Supprime un matériel unique de la base de données.

            Args:
                cnx (connection): La connexion à la base de données.
                id_materiel_unique (int): L'identifiant du matériel unique à supprimer.

            Raises:
                Exception: En cas d'erreur lors de la suppression du matériel unique.

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
        def modifie_materiel_unique(cnx, idMaterielUnique, idRangement, dateReception, datePeremption, commentaireMateriel, quantiteApproximative) :
            """
            Modifie les informations d'un matériel unique dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMaterielUnique (int): Identifiant du matériel unique à modifier.
                idRangement (int): Identifiant du rangement du matériel unique.
                dateReception (str): Date de réception du matériel unique.
                datePeremption (str): Date de péremption du matériel unique.
                commentaireMateriel (str): Commentaire sur le matériel unique.
                quantiteApproximative (int): Quantité approximative du matériel unique.

            Raises:
                Exception: Erreur lors de la modification du matériel unique.

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
                
        def insere_materiel_unique(cnx, id_materiel, position, date_reception, date_peremption, commentaire, quantite_approximative):
            """
            Insère un nouveau matériel unique dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id_materiel (int): L'identifiant du matériel.
                position (str): La position du matériel dans le rangement.
                date_reception (str): La date de réception du matériel.
                date_peremption (str): La date de péremption du matériel.
                commentaire (str): Le commentaire sur le matériel.
                quantite_approximative (int): La quantité approximative du matériel.

            Returns:
                int: L'identifiant du nouveau matériel unique inséré, ou -1 en cas d'erreur.
            """
            try:
                if date_peremption is None or date_peremption == 'None' or date_peremption == "":
                    date_peremption = "NULL"
                else:
                    date_peremption = f"'{str(date_peremption)}'"

                nouvel_id = 0
                dernier_id = MaterielUnique.Get.get_last_id(cnx) 
                if dernier_id is None:
                    dernier_id = 1
                else:
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

                cnx.execute(sqlalchemy.text(query))
                cnx.commit()
                return nouvel_id
            except sqlalchemy.exc.OperationalError as e:
                print(f"SQL OperationalError: {e}")
                return -1
            except sqlalchemy.exc.IntegrityError as e:
                print(f"SQL IntegrityError: {e}")
                return -1
            
     


