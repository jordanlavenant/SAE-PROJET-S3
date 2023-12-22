from sqlalchemy import text


class Domaine: 
    
    def get_all_info_from_domaine(cnx):
        """
        Récupère toutes les informations du domaine à partir de la connexion à la base de données.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste contenant toutes les informations du domaine.
        """
        try:
            list = []
            result = cnx.execute(text("select * from DOMAINE ;"))
            for row in result:
                print(row)
                list.append(row)
            return list
        except:
            print("erreur de l'id")
            raise
        
    def get_domaine(cnx):
        """
        Récupère les informations sur les domaines depuis la base de données.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste contenant les informations sur les domaines.
            
        Raises:
            Exception: En cas d'erreur lors de la récupération des informations.
        """
        try:
            result = cnx.execute(text("SELECT * from DOMAINE;"))
            info_commande = []
            for row in result:
                info_commande.append(row)
            return info_commande
        except Exception as e:
            print("Erreur lors de la récupération des informations sur les commandes :", str(e))
            raise
        
        
    def get_id_domaine_from_categorie(cnx, id_categorie) :
        """
        Récupère l'identifiant du domaine à partir de l'identifiant de la catégorie.

        Args:
            cnx (object): Objet de connexion à la base de données.
            id_categorie (int): Identifiant de la catégorie.

        Returns:
            int: Identifiant du domaine.

        Raises:
            Exception: Erreur lors de la récupération du domaine.
        """
        try:
            result = cnx.execute(text("SELECT idDomaine FROM CATEGORIE WHERE idCategorie = " + str(id_categorie) + ";"))
            for row in result:
                return row[0]
        except:
            print("Erreur lors de la récupération du domaine")
            raise