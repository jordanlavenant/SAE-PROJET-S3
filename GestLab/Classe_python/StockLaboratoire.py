from sqlalchemy import text


class STOCKLABORATOIRE:
    class Get:
        def get_quantite_with_idMateriel(cnx, idMateriel):
            """
            Récupère la quantité en stock d'un matériel spécifié par son identifiant.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMateriel (int): Identifiant du matériel.

            Returns:
                int: La quantité en stock du matériel.

            Raises:
                Exception: En cas d'erreur lors de la récupération de la quantité.
            """
            try:
                result = cnx.execute(text("SELECT quantiteLaboratoire FROM STOCKLABORATOIRE natural join MATERIEL WHERE idMateriel = " + str(idMateriel) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de la quantité")
                raise

        def materiel_dans_stock(cnx, idMateriel):
            """
            Vérifie si un matériel est présent dans le stock du laboratoire.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMateriel (int): Identifiant du matériel.

            Returns:
                int: Le nombre de fois que le matériel est présent dans le stock.

            Raises:
                Exception: En cas d'erreur lors de l'insertion du matériel dans le stock.
            """
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
            """
            Insère un matériel dans le stock du laboratoire.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMateriel (int): Identifiant du matériel à insérer.

            Raises:
                Exception: Erreur lors de l'insertion du matériel dans le stock.

            """
            try:
                cnx.execute(text("INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (" + str(idMateriel) + ", 0);"))
                cnx.commit()
            except:
                print("Erreur lors de l'insertion du matériel dans le stock")
                raise