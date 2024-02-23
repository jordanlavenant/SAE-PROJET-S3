from sqlalchemy import text


class Table:
    
    class Get:
        
        def afficher_table(cnx, table):
            """
            Affiche le contenu d'une table dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                table (str): Nom de la table à afficher.

            Returns:
                list: Liste contenant les lignes de la table.

            Raises:
                Exception: En cas d'erreur lors de l'affichage de la table.
            """
            try:
                list = []
                result = cnx.execute(text("SELECT * FROM " + table + ";"))
                for row in result:
                    list.append(row)
                return list
            except:
                print("Erreur lors de l'affichage de la table")
                raise
        
        def get_AllTable(cnx):
            """
            Récupère une liste de toutes les tables dans la base de données.

            Paramètres:
                - cnx: L'objet de connexion à la base de données.
            Returns:
                - res: A list of table names.
            """
            
            AllTable = cnx.execute(text("SHOW TABLES;"))
            res = []
            for table in AllTable:
                res.append(table[0])
            return res