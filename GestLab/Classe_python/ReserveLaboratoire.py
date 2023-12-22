from sqlalchemy import text

class ReserveLaboratoire :
    class Get:
        def get_last_id_reserve(cnx):
            """
            Récupère le dernier identifiant de réservation dans la table RESERVELABORATOIRE.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                int: Le dernier identifiant de réservation, ou 0 si la table est vide.

            Raises:
                Exception: En cas d'erreur lors de la récupération du dernier identifiant.
            """
            try:
                res = None
                result = cnx.execute(text("SELECT idReserve FROM RESERVELABORATOIRE ORDER BY idReserve DESC LIMIT 1 ;"))

                for row in result:
                    res = row[0]
                if res == None:
                    return 0
                else:
                    return res
            except:
                print("Erreur lors de la récupération du dernier id")
                raise
        
    class Insert:
        def insere_materiel_unique_reserve(cnx, idMaterielUnique):
            """
            Insère un matériel unique dans la table RESERVELABORATOIRE.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMaterielUnique (int): L'identifiant du matériel unique à insérer.

            Returns:
                bool: True si l'insertion a réussi, False sinon.
            """
            last_id_reserve = ReserveLaboratoire.Get.get_last_id_reserve(cnx)+1
            cnx.execute(text("INSERT INTO RESERVELABORATOIRE (idReserve,idMaterielUnique) VALUES (" + str(last_id_reserve) + "," + str(idMaterielUnique) + ");"))
            cnx.commit()
            return True