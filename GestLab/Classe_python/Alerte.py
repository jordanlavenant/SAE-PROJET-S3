from sqlalchemy import text


class Alert:
    
    def get_nb_alert_id(cnx):
        """
        Récupère le nombre d'alertes en cours avec leurs types.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste des alertes en cours avec leurs types.
        """
        try:
            list = []
            result = cnx.execute(text("SELECT * FROM ALERTESENCOURS natural join TYPESALERTES"))
            for row in result:
                list.append((row))
            print(list)
            return list
        except Exception as e:
            print("Erreur lors de la récupération du nombre d'alertes :", str(e))
            raise
        
    def get_info_materiel_alert(cnx):
        """
        Récupère les informations des matériels en alerte.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            list: Liste des informations des matériels en alerte.
        """
        try:
            list = []
            result = cnx.execute(text("select * from MATERIEL natural join MATERIELUNIQUE natural join ALERTESENCOURS;"))    
            for row in result: 
                list.append((row))
            print(list)
            return list
        except Exception as e:
            print("Erreur lors de la récupération du nombre d'alertes :", str(e))
            raise
        
    def get_nb_alert(cnx):
        """
        Récupère le nombre d'alertes en cours.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            int: Le nombre d'alertes en cours.

        Raises:
            Exception: En cas d'erreur lors de la récupération du nombre d'alertes.
        """
        try:
            cpt = 0
            result = cnx.execute(text("SELECT * FROM ALERTESENCOURS"))
            for _ in result:
                cpt += 1
            return cpt
        except Exception as e:
            print("Erreur lors de la récupération du nombre d'alertes :", str(e))
            raise
        
    def nb_alert_par_materiel_dict(cnx):
        """
        Cette fonction retourne un dictionnaire contenant le nombre d'alertes par matériel.

        Args:
            cnx (object): L'objet de connexion à la base de données.

        Returns:
            dict: Un dictionnaire contenant le nombre d'alertes par matériel.
        """
        try:
            dict = {}
            result = cnx.execute(text("select idMateriel,idMaterielUnique from ALERTESENCOURS natural join MATERIELUNIQUE;"))
            for row in result:
                if row[0] in dict:
                    dict[row[0]] += 1
                else:
                    dict[row[0]] = 1

            print(dict)
            return dict
        except: 
            raise

    def nb_alert_par_materielUnique_dict(cnx):
        """
        Cette fonction retourne un dictionnaire contenant le nombre d'alertes par matériel unique.

        Args:
            cnx (object): L'objet de connexion à la base de données.

        Returns:
            dict: Un dictionnaire contenant le nombre d'alertes par matériel unique.
        """
        try:
            dict = {}
            result = cnx.execute(text("select idMaterielUnique,idMaterielUnique from ALERTESENCOURS natural join MATERIELUNIQUE;"))
            for row in result:
                if row[0] in dict:
                    dict[row[0]] += 1
                else:
                    dict[row[0]] = 1

            print(dict)
            return dict
        except: 
            raise
