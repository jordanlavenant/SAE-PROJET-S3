from sqlalchemy import text
import sqlalchemy
import GestLab.Classe_python.Materiel as Materiel 
import GestLab.Classe_python.MaterielUnique as MaterielUnique
import csv



class ImportCSV:
            
    class Insert:
                
        def importer_csv(cnx, data) :
            with open(data, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)
            print(data)

        import csv

        def exporter_csv(cnx):
            AllTable = []
            for table in cnx.execute(text("SHOW TABLES;")):
                AllTable.append(table[0])     

            print("Exportation en cours")
            AllTable = ImportCSV.Insert.arrangeTable(AllTable)
            print(AllTable)
            with open("table/tout.csv", 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for table in AllTable:
                    writer.writerow([f"-{table}"])  # Écrire la ligne commençant par "-"
                    attribut = cnx.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'"+ table +"'  AND TABLE_SCHEMA = 'blandeau_gestlab19';"))
                    for att in attribut:
                        writer.writerow([f"*{att[0]}"])  # Écrire les lignes commençant par "*"
                    for row in cnx.execute(text("SELECT * FROM "+ table)):
                        writer.writerow(row)
                    writer.writerow(" ")  # Écrire une ligne vide pour séparer les tables
            print("Exportation terminée")

        def arrangeTable(listTables):
            res = []
            
            if "DOMAINE" in listTables:
                res.append("DOMAINE")
                listTables.remove("DOMAINE")
            if "CATEGORIE" in listTables:
                res.append("CATEGORIE")
                listTables.remove("CATEGORIE")
            if "STATUT" in listTables:
                res.append("STATUT")
                listTables.remove("STATUT")
            if "UTILISATEUR" in listTables:
                res.append("UTILISATEUR")
                listTables.remove("UTILISATEUR")
            if "RISQUE" in listTables:
                res.append("RISQUE")
                listTables.remove("RISQUE")
            if "FDS" in listTables:
                res.append("FDS")
                listTables.remove("FDS")
            if "RISQUES" in listTables:
                res.append("RISQUES")
                listTables.remove("RISQUES")
            if "ENDROIT" in listTables:
                res.append("ENDROIT")
                listTables.remove("ENDROIT")
            if "RANGEMENT" in listTables:
                res.append("RANGEMENT")
                listTables.remove("RANGEMENT")
            if "MATERIEL" in listTables:
                res.append("MATERIEL")
                listTables.remove("MATERIEL")
            if "MATERIELUNIQUE" in listTables:
                res.append("MATERIELUNIQUE")
                listTables.remove("MATERIELUNIQUE")
            if "STOCKLABORATOIRE" in listTables:
                res.append("STOCKLABORATOIRE")
                listTables.remove("STOCKLABORATOIRE")
            if "FOURNISSEUR" in listTables:
                res.append("FOURNISSEUR")
                listTables.remove("FOURNISSEUR")
            if "ETATDEMANDE" in listTables:
                res.append("ETATDEMANDE")
                listTables.remove("ETATDEMANDE")
            if "DEMANDE" in listTables:
                res.append("DEMANDE")
                listTables.remove("DEMANDE")
            if "ETATCOMMANDE" in listTables:
                res.append("ETATCOMMANDE")
                listTables.remove("ETATCOMMANDE")
            if "BONCOMMANDE" in listTables:
                res.append("BONCOMMANDE")
                listTables.remove("BONCOMMANDE")
            if "SUIVICOMMANDE" in listTables:
                res.append("SUIVICOMMANDE")
                listTables.remove("SUIVICOMMANDE")
            if "TYPESALERTES" in listTables:
                res.append("TYPESALERTES")
                listTables.remove("TYPESALERTES")
            if "RECHERCHEMATERIELS" in listTables:
                res.append("RECHERCHEMATERIELS")
                listTables.remove("RECHERCHEMATERIELS")
            return res


        def get_AllTable(cnx):
            AllTable = cnx.execute(text("SHOW TABLES;"))
            res = []
            for table in AllTable:
                res.append(table[0])
            return res
        

                    

            
     


