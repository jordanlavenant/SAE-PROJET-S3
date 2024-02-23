from sqlalchemy import text
import sqlalchemy
import GestLab.Classe_python.Materiel as Materiel 
import GestLab.Classe_python.MaterielUnique as MaterielUnique
import csv



class ExportCSV:
            
    class Get:
        def exporter_csv(cnx, list_table_a_exporter):
            for table in list_table_a_exporter:

                print("Exportation de la table:" + table + ":en cours...")
                with open("table/tout.csv", 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([f"-{table}"])  # Écrire la ligne commençant par "-"
                    attribut = cnx.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'"+ table +"'  AND TABLE_SCHEMA = 'blandeau_gestlab19';"))
                    for att in attribut:
                        writer.writerow([f"*{att[0]}"])  # Écrire les lignes commençant par "*"
                    for row in cnx.execute(text("SELECT * FROM "+ table)):
                        writer.writerow(row)
                    writer.writerow(" ")  # Écrire une ligne vide pour séparer les tables
            print("Exportation terminée")
        
            
     


