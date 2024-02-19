from sqlalchemy import text
import sqlalchemy
import GestLab.Classe_python.Materiel as Materiel 
import GestLab.Classe_python.MaterielUnique as MaterielUnique
import GestLab.Classe_python.FDS as FDS
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
                    formatted_data.append("'" + item + "'") 
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(formatted_data)});"
            print(query)
            cnx.execute(text(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(formatted_data)});"))
            cnx.commit()

        def importer_csv(cnx, data):
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
                                ImportCSV.Insert.insertBD(cnx, table, columns, line)
        
                    
     


