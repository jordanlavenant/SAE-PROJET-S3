from sqlalchemy import text


class Recherche_materiel:
    
    def get_MATERIEL(cnx):
        """
        Retrieves all the rows from the RECHERCHEMATERIELS table.

        Parameters:
        - cnx: The database connection object.

        Returns:
        None
        """
        result = cnx.execute(text("select * from RECHERCHEMATERIELS;"))
        for row in result:
            print(row[0])
            
    def get_info_rechercheMateriel(cnx):
        """
        Récupère les informations sur les recherches de matériel.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste des informations sur les recherches de matériel.
        """
        try:
            result =  cnx.execute(text("select * from RECHERCHEMATERIELS;"))
            list = []
            for row in result:
                list.append(row[0])
            return list
        except Exception as e:
            print("Erreur lors de la récupération des informations sur les commandes :", str(e))
            raise