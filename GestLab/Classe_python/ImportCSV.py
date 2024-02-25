from sqlalchemy import text
import sqlalchemy
import GestLab.Classe_python.Materiel as Materiel 
import GestLab.Classe_python.MaterielUnique as MaterielUnique
import GestLab.Classe_python.FDS as FDS
import GestLab.Classe_python.FonctionsGlobales as FonctionsGlobales
import csv
import re


class ImportCSV:
            
    class Insert:

        def insertBD(cnx, table, columns, data): 
            data = data.split(',')
            formatted_data = []
            for item in data:
                if item.isdigit():
                    formatted_data.append(item)
                else:
                    formatted_data.append('"' + item + '"') 
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(formatted_data)});"
            cnx.execute(text(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(formatted_data)});"))
            cnx.commit()

        def importer_csv_bd_plein(cnx, data):
            try:
            #importation des données
                columns = []
                table = None  
                with open(data, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        line = ','.join(row)
                        if line != []:
                            if line.startswith('-'):
                                columns = []
                                table = line[1:]
                            if line.startswith('*'):
                                columns.append(line[1:])
                            elif not line.startswith('*') and not line.startswith('-'):
                                if table is not None and line is not None and line != ' ' and line != '' and line !=[]:  # Check if table has been assigned a value
                                    try:
                                        ImportCSV.Insert.insertBD(cnx, table, columns, line)
                                    except:
                                        print("Erreur lors de l'insertion")
            except sqlalchemy.exc.IntegrityError:
                cnx.rollback()
                print("Erreur d'intégrité, rollback")
            except Exception as e:
                print(e)      
            
        
        def importer_csv_bd_vide(cnx, data):
            try :
                def delete_all(cnx):
                    """ Delete tout sauf le contenu des tables UTILISATEUR, STATUT et 2FA; 
                    Ne supprime pas vraiment STOCKLABORATOIRE : SET toutes les quantités à 0"""
                    statements = [
                        "DELETE FROM RISQUES",
                        "DELETE FROM RESERVELABORATOIRE",
                        "DELETE FROM STOCKLABORATOIRE",
                        "DELETE FROM ENVOIFOURNISSEUR",
                        "DELETE FROM SUIVICOMMANDE",
                        "DELETE FROM AJOUTERMATERIEL",
                        "DELETE FROM RECHERCHEMATERIELS",
                        "DELETE FROM ALERTESENCOURS",
                        "DELETE FROM MATERIELUNIQUE",
                        "DELETE FROM COMMANDE",
                        "DELETE FROM MATERIEL",
                        "DELETE FROM ARCHIVECOMMANDE",
                        "DELETE FROM ARCHIVEBONCOMMANDE",
                        "DELETE FROM ARCHIVECOMMANDEANCIEN",
                        "DELETE FROM FOURNISSEUR",
                        "DELETE FROM RANGEMENT",
                        "DELETE FROM ENDROIT",
                        "DELETE FROM CATEGORIE",
                        "DELETE FROM DOMAINE",
                        "DELETE FROM RISQUE",
                        "DELETE FROM FDS",
                        "DELETE FROM BONCOMMANDE",
                        "DELETE FROM DEMANDE",
                        "DELETE FROM ETATCOMMANDE",
                        "DELETE FROM TYPESALERTES",
                        "DELETE FROM ETATDEMANDE"

                    ]
                    for statement in statements:
                        cnx.execute(text(statement + ";"))
                        cnx.commit()

                
                delete_all(cnx)

                #importation des données
                columns = []
                table = None  
                with open(data, 'r', encoding="UTF-8") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        line = ','.join(row)
                        if line != []:
                            if line.startswith('-'):
                                columns = []
                                table = line[1:]
                            if line.startswith('*'):
                                columns.append(line[1:])
                            elif not line.startswith('*') and not line.startswith('-'):
                                if table is not None and line is not None and line != ' ' and line != '' and line !=[]:  # Check if table has been assigned a value
                                    try:
                                        ImportCSV.Insert.insertBD(cnx, table, columns, line)
                                    except:
                                        print("Erreur lors de l'insertion")
            except sqlalchemy.exc.IntegrityError:
                cnx.rollback()
                print("Erreur d'intégrité, rollback")
            except Exception as e:
                print(e)               
        
                       
     


