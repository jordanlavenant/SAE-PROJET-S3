

import datetime
from sqlalchemy import text


class DATE:
    class Get:
        def get_date(cnx):
            """
            Récupère la date actuelle à partir de la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                date: La date actuelle extraite de la base de données, ou la date actuelle du système si la requête échoue.
            """
            date_result = cnx.execute(text("SELECT CURDATE();")).fetchone()
            
            # Extraire la date du résultat
            date_res = date_result[0] if date_result else datetime.now().date()
            return date_res

        def materiel_dans_stock(cnx, idMateriel):
            """
            Vérifie si un matériel est présent dans le stock du laboratoire.

            Args:
                cnx (connection): La connexion à la base de données.
                idMateriel (int): L'identifiant du matériel à vérifier.

            Returns:
                int: Le nombre de fois que le matériel est présent dans le stock.

            Raises:
                Exception: En cas d'erreur lors de l'insertion du matériel dans le stock.
            """
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
            """
            Insère un matériel dans le stock du laboratoire.

            :param cnx: La connexion à la base de données.
            :type cnx: object
            :param idMateriel: L'identifiant du matériel à insérer.
            :type idMateriel: int
            """
            try:
                cnx.execute(text("INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (" + str(idMateriel) + ", 0);"))
                cnx.commit()
            except:
                print("Erreur lors de l'insertion du matériel dans le stock")
                raise