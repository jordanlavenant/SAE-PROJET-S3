from sqlalchemy import text
import sqlalchemy
import GestLab.Classe_python.Materiel as Materiel 
import GestLab.Classe_python.MaterielUnique as MaterielUnique



class ImportCSV:
            
    class Insert:
                
        def importer_csv(cnx, data) :
            with open(data, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)
            print("heee heee")
            
     


