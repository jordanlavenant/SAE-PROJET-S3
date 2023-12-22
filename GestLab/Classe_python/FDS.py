from sqlalchemy import text


class FDS:
    class Get:
        def get_FDS_with_idMateriel(cnx, idMat):
            """
            Récupère l'identifiant de la FDS associée à un matériel donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMat (int): Identifiant du matériel.

            Returns:
                int: Identifiant de la FDS associée au matériel.

            Raises:
                Exception: Erreur lors de la récupération de l'identifiant de la FDS.
            """
            try:
                result = cnx.execute(text("SELECT idFDS FROM MATERIEL natural join FDS WHERE idMateriel = " + str(idMat) + ";"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de la FDS")
                raise

        def get_idFDS_with_nomFDS(cnx, nomFDS):
            """
            Récupère l'identifiant de la FDS correspondant au nom donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                nomFDS (str): Nom de la FDS.

            Returns:
                int: Identifiant de la FDS.

            Raises:
                Exception: Erreur lors de la récupération de l'identifiant de la FDS.
            """
            try:
                result = cnx.execute(text("SELECT idFDS FROM FDS WHERE nomFDS = '" + nomFDS + "';"))
                for row in result:
                    return row[0]
            except:
                print("Erreur lors de la récupération de l'id de la FDS")
                raise
    
    class Insert:
        def ajout_FDS(cnx, nomFDS):
            """
            Ajoute une nouvelle FDS à la base de données.

            Args:
                cnx (connection): La connexion à la base de données.
                nomFDS (str): Le nom de la FDS à ajouter.

            Returns:
                None
            """
            cnx.execute(text("INSERT INTO FDS (nomFDS) VALUES ('" + nomFDS + "');"))
            cnx.commit()
        
    class Update:
        def update_FDS(cnx, idFDS, idMateriel):
            """
            Met à jour le champ idFDS du matériel spécifié avec l'identifiant de la FDS spécifiée.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idFDS (int): L'identifiant de la FDS à associer au matériel.
                idMateriel (int): L'identifiant du matériel à mettre à jour.

            Returns:
                None
            """
            cnx.execute(text("UPDATE MATERIEL SET idFDS = '" + str(idFDS) + "' WHERE idMateriel = " + str(idMateriel) + ";"))
            cnx.commit()

        