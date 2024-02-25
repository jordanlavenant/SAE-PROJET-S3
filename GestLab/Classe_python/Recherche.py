from sqlalchemy import text

from GestLab.Classe_python.Domaine import Domaine


class Recherche:
    
    def recherche_materiel_commander_search(cnx, search):
        """
        Recherche les matériels commandés en fonction d'un critère de recherche.

        Args:
            cnx (object): Objet de connexion à la base de données.
            search (str): Critère de recherche.

        Returns:
            list: Liste des matériels commandés correspondant au critère de recherche.

        Raises:
            Exception: En cas d'erreur lors de la recherche.
        """
        try:
            list = []
            result = cnx.execute(text("select idMateriel,nomMateriel,referenceMateriel,idFDS,idFDS,seuilAlerte,caracteristiquesComplementaires,caracteristiquesComplementaires from MATERIEL where nomMateriel like '%" + search + "%' ;"))
            result1 = cnx.execute(text("select idMateriel,nomMateriel,referenceMateriel,idFDS,idFDS,seuilAlerte,caracteristiquesComplementaires,caracteristiquesComplementaires from MATERIEL where referenceMateriel like '%" + search + "%' ;"))
            for row in result:
                print(row)
                list.append(row)
            for row in result1:
                print(row)
                list.append(row)
            return list
        except:
            print("erreur de recherche")
            raise

    def recherche_all_in_utilisateur_with_search(cnx, search):
        """
        Recherche tous les utilisateurs dont le nom ou le prénom correspond à la recherche donnée.

        Args:
            cnx (object): L'objet de connexion à la base de données.
            search (str): La chaîne de recherche.

        Returns:
            tuple: Un tuple contenant une liste des utilisateurs correspondants à la recherche et le nombre total de résultats.
        """
        try:
            list = []
            result = cnx.execute(text("select * from UTILISATEUR where idStatut != 1 and nom like '%" + search + "%'" or " prenom like '%" + search + "%' ;"))
            for row in result:
                print(row)
                list.append(row)
            return (list, len(list))
        except:
            print("erreur de recherche")
            raise

    def recherche_all_in_utilisateur_with_search_statut(cnx, search, idStatut=None):
        """
        Recherche tous les utilisateurs dont le nom ou le prénom correspond à la recherche donnée.

        Args:
            cnx (object): L'objet de connexion à la base de données.
            search (str): La chaîne de recherche.

        Returns:
            tuple: Un tuple contenant une liste des utilisateurs correspondants à la recherche et le nombre total de résultats.
        """
        try:
            list = []
            print(idStatut)
            if idStatut is not None:
                result = cnx.execute(text("select * from UTILISATEUR where idStatut = '" + str(idStatut) + "' and (nom like '%" + search + "%' or prenom like '%" + search + "%') ;"))
            for row in result:
                print(row)
                list.append(row)
            return (list, len(list))
        except:
            print("erreur de recherche")
            raise

    
    def recherche_all_in_materiel_with_search(cnx, idbc, search):
        """
        Recherche les matériels correspondant à un critère de recherche dans une commande spécifique.

        Args:
            cnx (object): Objet de connexion à la base de données.
            idbc (int): Identifiant de la commande.
            search (str): Critère de recherche.

        Returns:
            list: Liste des matériels correspondant au critère de recherche dans la commande spécifique.
        """
        try:
            liste = []
            result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + " and nomMateriel like '%" + search + "%';"))
            result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM COMMANDE NATURAL JOIN MATERIEL WHERE idBonCommande = " + str(idbc) + ") and nomMateriel like '%" + search + "%';"))
            for row in result:
                idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            for row in result2:
                idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            return liste
        except:
            print("erreur de recherche")
            raise

    def recherche_all_in_materiel_demande_with_search(cnx, idDemande, search):
        """
        Recherche tous les matériels demandés avec une recherche spécifique.

        Args:
            cnx (object): L'objet de connexion à la base de données.
            idDemande (int): L'identifiant de la demande.
            search (str): La chaîne de recherche pour filtrer les résultats.

        Returns:
            list: Une liste contenant les informations des matériels trouvés.
                Chaque élément de la liste est un tuple contenant les informations suivantes:
                - idMateriel (int): L'identifiant du matériel.
                - nomMateriel (str): Le nom du matériel.
                - caracteristiquesComplementaires (str): Les caractéristiques complémentaires du matériel.
                - referenceMateriel (str): La référence du matériel.
                - quantite (int): La quantité du matériel.
                - informationsComplementairesEtSecurite (str): Les informations complémentaires et de sécurité du matériel.
                - idDomaine (int): L'identifiant du domaine du matériel.
        
        Raises:
            Exception: En cas d'erreur lors de la recherche.
        """
        try:
            liste = []
            result = cnx.execute(text("SELECT idMateriel, nomMateriel, caracteristiquesComplementaires, referenceMateriel, quantite, informationsComplementairesEtSecurite, idCategorie FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idDemande) + " and nomMateriel like '%" + search + "%';"))
            result2 = cnx.execute(text("SELECT idMateriel, nomMateriel,caracteristiquesComplementaires, referenceMateriel, 0, informationsComplementairesEtSecurite, idCategorie FROM MATERIEL WHERE idMateriel NOT IN (SELECT idMateriel FROM AJOUTERMATERIEL NATURAL JOIN MATERIEL WHERE idDemande = " + str(idDemande) + ") and nomMateriel like '%" + search + "%';"))
            for row in result:
                    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                    liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            for row in result2:
                idDomaine = Domaine.get_id_domaine_from_categorie(cnx, row[6])
                liste.append((row[0], row[1], row[2], row[3], row[4], row[5], idDomaine))
            return liste
        except:
            print("erreur de recherche")
            raise

    def recherche_all_in_inventaire(cnx):
        """
        Recherche tous les éléments dans l'inventaire.

        Args:
            cnx (object): Objet de connexion à la base de données.

        Returns:
            tuple: Une liste contenant les résultats de la requête et le nombre d'éléments trouvés.
        """
        try:
            list = []
            result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE;"))
            for row in result:
                id = row[0]
                result_count = cnx.execute(text("select idMateriel, count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
                for row_count in result_count:
                    print((row_count[1]))
                    list.append((row,row_count[1]))
            return list, len(list)
        except:
            print("erreur de l'id")
            raise

    def recherche_all_in_inventaire_with_search(cnx, search):
        """
        Recherche les éléments dans l'inventaire en fonction d'une recherche donnée.

        Args:
            cnx (object): L'objet de connexion à la base de données.
            search (str): La chaîne de recherche.

        Returns:
            tuple: Un tuple contenant une liste des résultats de recherche et le nombre total de résultats.
        """
        try:
            list = []
            result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE where nomMateriel like '%" + search + "%' ;"))
            for row in result:
                id = row[0]
                result_count = cnx.execute(text("select idMateriel, count(*) from MATERIELUNIQUE natural join MATERIEL natural join CATEGORIE NATURAL join DOMAINE where idMateriel =" + str(id) + ";"))
                for row_count in result_count:
                    print((row_count[1]))
                    list.append((row,row_count[1]))
            return list, len(list)
        except:
            print("erreur de l'id")
            raise
