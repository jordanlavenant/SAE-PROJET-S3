from sqlalchemy import text


class Categories:
    
    def get_categories(cnx):
        """
        Récupère toutes les catégories depuis la base de données.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste des catégories sous forme de tuples (id, nom, description).
        """
        liste = []
        result = cnx.execute(text("select * from CATEGORIE;"))
        for row in result:
            liste.append((row[0],row[2],row[1]))
        return liste
    