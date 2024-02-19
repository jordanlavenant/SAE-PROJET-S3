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
            AllTable = cnx.execute(text("SHOW TABLES;"))
            for table in AllTable:
                print(table[0])
                with open("table/tout.csv", 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([f"-{table[0]}"])  # Écrire la ligne commençant par "-"
                    attribut = cnx.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'"+ table[0] +"'  AND TABLE_SCHEMA = 'blandeau_gestlab19';"))
                    for att in attribut:
                        writer.writerow([f"*{att[0]}"])  # Écrire les lignes commençant par "*"
                    for row in cnx.execute(text("SELECT * FROM "+ table[0])):
                        writer.writerow(row)
                    writer.writerow(" ")  # Écrire une ligne vide pour séparer les tables
            print("Exportation terminée")


                    

            
     


