from sqlalchemy import text


class Endroit :
    class Insert :
        def insere_endroit(cnx, endroit):
            """
            Insère un nouvel endroit dans la base de données.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                endroit (str): Le nom de l'endroit à insérer.

            Returns:
                bool: True si l'insertion a réussi, False sinon.
            """
            try:
                cnx.execute(text("INSERT INTO ENDROIT (endroit) VALUES ('" + endroit + "');"))
                print(text("INSERT INTO ENDROIT (endroit) VALUES ('" + endroit + "');"))
                cnx.commit()
                return True
            except:
                print("Erreur lors de l'insertion de l'endroit")
                return False