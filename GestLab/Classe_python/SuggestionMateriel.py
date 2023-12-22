from sqlalchemy import text


class Suggestion_materiel:
    
    def get_all_information_to_Materiel_suggestions(cnx):
        """
        Récupère toutes les informations pour les suggestions de matériel.

        Args:
            cnx: La connexion à la base de données.

        Returns:
            Une liste contenant les informations de chaque matériel et le nombre total de matériel.

        Raises:
            Exception: En cas d'erreur lors de l'exécution de la requête.
        """
        try:
            list = []
            result = cnx.execute(text("select idMateriel, nomMateriel, idCategorie,nomCategorie, idDomaine,nomDomaine,quantiteLaboratoire,idRisque,nomRisque,idFDS,0,referenceMateriel,seuilAlerte,caracteristiquesComplementaires,informationsComplementairesEtSecurite, idStock  from MATERIEL natural left join STOCKLABORATOIRE NATURAL JOIN CATEGORIE NATURAL JOIN DOMAINE NATURAL LEFT JOIN FDS NATURAL JOIN RISQUES NATURAL JOIN RISQUE ;"))
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
