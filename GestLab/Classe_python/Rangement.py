from sqlalchemy import text


class Rangement:
    
    class Get:
        
        def get_id_endroit_from_id_rangement(cnx, idRangement) :
            """
            Récupère l'identifiant de l'endroit à partir de l'identifiant du rangement.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idRangement (int): Identifiant du rangement.

            Returns:
                int: Identifiant de l'endroit.

            Raises:
                Exception: Erreur lors de la récupération de l'identifiant de l'endroit.
            """
            try:
                result = cnx.execute(text("SELECT idEndroit FROM RANGEMENT WHERE idRangement = " + str(idRangement) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de l'endroit")
                raise

    class Insert :
        def insere_rangement(cnx, id_endroit, position) :
            """
            Insère un nouvel enregistrement dans la table RANGEMENT.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                id_endroit (int): L'identifiant de l'endroit où le rangement est situé.
                position (str): La position du rangement.

            Returns:
                bool: True si l'insertion a réussi, False sinon.
            """
            try :
                print(text("INSERT INTO RANGEMENT (idEndroit, position) VALUES (" + str(id_endroit) + ", '" + str(position) + "');"))
                cnx.execute(text("INSERT INTO RANGEMENT (idEndroit, position) VALUES (" + str(id_endroit) + ", '" + str(position) + "');"))
                cnx.commit()
                return True
            except :
                print("Erreur lors de l'insertion de l'endroit")
                return False

