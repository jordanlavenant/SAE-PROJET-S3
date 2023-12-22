from sqlalchemy import text
from GestLab.Classe_python.FDS import FDS


class Risques:
    
    class Get:
        def get_risque_with_idMateriel(cnx, idMat):
            """
            Récupère les informations sur le risque associé à un matériel donné.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMat (int): Identifiant du matériel.

            Returns:
                tuple: Un tuple contenant les informations suivantes:
                    - referenceMateriel (str): La référence du matériel.
                    - nomMateriel (str): Le nom du matériel.
                    - listBoolean[0] (bool): Indicateur de la présence du risque "Toxicité aiguë".
                    - listBoolean[1] (bool): Indicateur de la présence du risque "Danger incendie".
                    - listBoolean[2] (bool): Indicateur de la présence du risque "Explosif".
                    - listBoolean[3] (bool): Indicateur de la présence du risque "Gaz sous pression".
                    - listBoolean[4] (bool): Indicateur de la présence du risque "Effets graves sur la santé".
                    - listBoolean[5] (bool): Indicateur de la présence du risque "Toxicité aquatique".
                    - listBoolean[6] (bool): Indicateur de la présence du risque "Altération de la santé humaine".
                    - listBoolean[7] (bool): Indicateur de la présence du risque "Comburant".
                    - listBoolean[8] (bool): Indicateur de la présence du risque "Corrosion".

            Raises:
                None: Si une erreur se produit lors de la récupération du risque.
            """
            try:
                referenceMateriel = ""
                nomMateriel = ""
                listBooleanTrue = []
                result = cnx.execute(text("SELECT nomRisque, referenceMateriel, nomMateriel FROM MATERIEL natural  join FDS natural left join  RISQUES Natural left join RISQUE WHERE idFDS = " + str(idMat) + ";"))
                
                for row in result:
                    listBooleanTrue.append(row[0])
                    nomMateriel = row[2]
                    referenceMateriel = row[1]
                    
                listBoolean = []
                if "Toxicité aiguë" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                
                if "Danger incendie" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Explosif" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Gaz sous pression" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                
                if "Effets graves sur la santé" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Toxicité aquatique" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                
                if "Altération de la santé humaine" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Comburant" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                if "Corrosion" in listBooleanTrue:
                    listBoolean.append(True)
                else :
                    listBoolean.append(False)
                    
                return referenceMateriel, nomMateriel, listBoolean[0], listBoolean[1], listBoolean[2], listBoolean[3], listBoolean[4], listBoolean[5], listBoolean[6], listBoolean[7], listBoolean[8]
            except:
                print("Erreur lors de la récupération du risque")
                return None
    class Update:
        def update_risque_with_idMateriel(cnx, idMat, estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif):
            """
            Met à jour les risques associés à un matériel donné dans la base de données.

            Args:
                cnx (object): Objet de connexion à la base de données.
                idMat (int): Identifiant du matériel.
                estToxique (bool): Indique si le matériel est toxique.
                estInflamable (bool): Indique si le matériel est inflammable.
                estExplosif (bool): Indique si le matériel est explosif.
                est_gaz_sous_pression (bool): Indique si le matériel est un gaz sous pression.
                est_CMR (bool): Indique si le matériel a des effets graves sur la santé.
                est_chimique_environement (bool): Indique si le matériel est toxique pour l'environnement.
                est_dangereux (bool): Indique si le matériel altère la santé humaine.
                est_comburant (bool): Indique si le matériel est comburant.
                est_corrosif (bool): Indique si le matériel est corrosif.

            Raises:
                Exception: Erreur lors de la modification du risque.

            """
            try:
                idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, idMat)
                listidRisque = []
                listRisqueAMateriel = []
                
                if estToxique:
                    listRisqueAMateriel.append("Toxicité aiguë")
                if estInflamable:
                    listRisqueAMateriel.append("Danger incendie")
                if estExplosif:
                    listRisqueAMateriel.append("Explosif")
                if est_gaz_sous_pression:
                    listRisqueAMateriel.append("Gaz sous pression")
                if est_chimique_environement:
                    listRisqueAMateriel.append("Toxicité aquatique")
                if est_CMR:
                    listRisqueAMateriel.append("Effets graves sur la senté")           
                if est_dangereux:
                    listRisqueAMateriel.append("Altération de la santé humaine")          
                if est_comburant:
                    listRisqueAMateriel.append("Comburant")
                if est_corrosif:
                    listRisqueAMateriel.append("Corrosion")
                    
                resultRisque = cnx.execute(text("SELECT idRisque, nomRisque FROM RISQUE;"))
                
                for row in resultRisque:
                    if row[1] in listRisqueAMateriel:
                        listidRisque.append(row[0])
                
                cnx.execute(text("DELETE FROM RISQUES WHERE idFDS = " + str(idFDS) + ";"))
                cnx.commit()
                
                for idRisque in listidRisque:
                    Risques.Insert.ajout_risques_with_idFDS_and_idrisque(cnx, idRisque, idFDS)
            except:
                print("Erreur lors de la modification du risque")
                raise
        
    class Insert:
        def ajout_risques_with_idFDS_and_idrisque(cnx, idRisque, idFDS):
            """
            Ajoute un risque avec un identifiant de FDS et un identifiant de risque donnés.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idRisque (int): L'identifiant du risque à ajouter.
                idFDS (int): L'identifiant de la FDS associée au risque.

            Raises:
                Exception: En cas d'erreur lors de l'ajout du risque.

            """
            try:
                cnx.execute(text("INSERT INTO RISQUES (idFDS, idRisque) VALUES (" + str(idFDS) + ", " + str(idRisque) + ");"))
                cnx.commit()
            except:
                print("Erreur lors de l'ajout du risque")
                raise
            
        
        def ajout_risque_with_idMateriel(cnx, idMat, estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif):
            """
            Ajoute les risques associés à un matériel spécifié.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMat (int): L'identifiant du matériel.
                estToxique (bool): Indique si le matériel est toxique.
                estInflamable (bool): Indique si le matériel est inflammable.
                estExplosif (bool): Indique si le matériel est explosif.
                est_gaz_sous_pression (bool): Indique si le matériel est un gaz sous pression.
                est_CMR (bool): Indique si le matériel est toxique pour l'environnement.
                est_chimique_environement (bool): Indique si le matériel a des effets graves sur l'environnement.
                est_dangereux (bool): Indique si le matériel altère la santé humaine.
                est_comburant (bool): Indique si le matériel est comburant.
                est_corrosif (bool): Indique si le matériel est corrosif.

            Raises:
                Exception: Erreur lors de l'ajout du risque.

            """
            try:
                idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, idMat)
                listidRisque = []
                listRisqueAMateriel = []
                
                if estToxique:
                    listRisqueAMateriel.append("Toxicité aiguë")
                if estInflamable:
                    listRisqueAMateriel.append("Danger incendie")
                if estExplosif:
                    listRisqueAMateriel.append("Explosif")
                if est_gaz_sous_pression:
                    listRisqueAMateriel.append("Gaz sous pression")
                if est_CMR:
                    listRisqueAMateriel.append("Toxicité aquatique")
                if est_chimique_environement:
                    listRisqueAMateriel.append("Effets graves sur l'environement")           
                if est_dangereux:
                    listRisqueAMateriel.append("Altération de la santé humaine")          
                if est_comburant:
                    listRisqueAMateriel.append("Comburant")
                if est_corrosif:
                    listRisqueAMateriel.append("Corrosion")
                    
                resultRisque = cnx.execute(text("SELECT idRisque, nomRisque FROM RISQUE;"))
                
                for row in resultRisque:
                    if row[1] in listRisqueAMateriel:
                        listidRisque.append(row[0])
                
                for idRisque in listidRisque:
                    Risques.Insert.ajout_risques_with_idFDS_and_idrisque(cnx, idRisque, idFDS)
            except:
                print("Erreur lors de l'ajout du risque")
                raise
    class Delete:
        def delete_risque_with_idMateriel(cnx, idMat):
            """
            Supprime un risque associé à un matériel spécifié.

            Args:
                cnx (object): L'objet de connexion à la base de données.
                idMat (int): L'identifiant du matériel.

            Raises:
                Exception: En cas d'erreur lors de la suppression du risque.

            Returns:
                None
            """
            try:
                idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, idMat)
                cnx.execute(text("DELETE FROM RISQUES WHERE idFDS = " + str(idFDS) + ";"))
                cnx.commit()
            except:
                print("Erreur lors de la suppression du risque")
                raise

