from sqlalchemy import text


class Commande :

    class Get:
        
        def get_statut_from_commande_with_id_boncommande(cnx, id_boncommande):
            """
            Récupère le statut de la commande à partir de l'identifiant du bon de commande.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id_boncommande (int): Identifiant du bon de commande.

            Returns:
                list: Liste des identifiants d'état de la commande.

            Raises:
                Exception: Erreur lors de la récupération du statut de la commande.
            """
            try:
                result = cnx.execute(text("SELECT idEtat, nomEtat FROM ETATCOMMANDE NATURAL JOIN BONCOMMANDE WHERE idBonCommande = " + str(id_boncommande) + ";"))
                liste = []
                for row in result:
                    liste.append(row[0])
                return liste
            except:
                print("Erreur lors de la récupération du statut de la commande")
                raise

        def get_statut_from_commande_with_id_etat(cnx, id_etat):
            """
            Récupère le statut de la commande à partir de l'identifiant de l'état.

            Args:
                cnx (object): Objet de connexion à la base de données.
                id_etat (int): Identifiant de l'état de la commande.

            Returns:
                list: Liste contenant l'identifiant et le nom de l'état de la commande.

            Raises:
                Exception: Erreur lors de la récupération du statut de la commande.
            """
            try:
                result = cnx.execute(text("SELECT idEtat, nomEtat FROM ETATCOMMANDE WHERE idEtat = " + str(id_etat) + ";"))
                liste = []
                for row in result:
                    liste.append(row[0])
                return liste
            except:
                print("Erreur lors de la récupération du statut de la commande")
                raise

        def get_statut_from_commande(cnx):
            """
            Récupère le statut de la commande à partir de la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.

            Returns:
                list: Liste contenant les résultats de la requête.

            Raises:
                Exception: En cas d'erreur lors de la récupération du statut de la commande.
            """
            try:
                result = cnx.execute(text("SELECT * FROM ETATCOMMANDE;"))
                liste = []
                for row in result:
                    liste.append(row)
                return liste
            except:
                print("Erreur lors de la récupération du statut de la commande")
                raise
