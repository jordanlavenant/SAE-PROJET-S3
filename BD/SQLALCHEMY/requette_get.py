from sqlalchemy import text
import connexionPythonSQL as conn
from datetime import date, datetime, timedelta
import requette_annexe as req_annexe

cnx = conn.get_cnx()

def afficher_table(cnx, table):

    result = cnx.execute(text("select * from " + table + ";"))
    for row in result:
        print(row)


# afficher_table(cnx, "RECHERCHEMATERIELS")


def get_nom_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIEL where idMateriel = " + str(id) + ";"))
        result = result.first()
        print(result[4])
        return result[4]
    except:
        print("erreur de l'id")
        raise

# get_nom_materiel_with_id(cnx, 3)

def get_nom_dom_cat_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIEL natural join DOMAINE natural join CATEGORIE where idMateriel = " + str(id) + ";"))
        result = result.first()
        print("domaine : " + result[4], " | categorie : ",result[5])
        return (result[4], result[5])
    except:
        print("erreur de l'id")
        raise

# get_nom_dom_cat_materiel_with_id(cnx, 1)

def get_nom_whith_email(cnx, email):
    result = cnx.execute(text("select nom from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]
    
# get_nom_whith_email(cnx, "alice.johnson@example.com")

def get_materiel(cnx):
    result = cnx.execute(text("select * from RECHERCHEMATERIELS;"))
    for row in result:
        print(row[0])

# get_materiel(cnx)

def get_id_ut_with_email(cnx, email):
    result = cnx.execute(text("select idUtilisateur from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]

# get_id_ut_with_email(cnx, "leo@")

def get_password_hashed_with_email(cnx, email):
    result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]

# get_password_hashed_with_email(cnx, "leo@")

def get_statut_with_email(cnx, email):
    result = cnx.execute(text("select nomStatut from UTILISATEUR natural join STATUT where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]
    
# get_statut_with_email(cnx, "admin@testhash2")


def get_nom_and_statut_with_email(cnx, email):
    result = cnx.execute(text("select nom, idStatut from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0], row[1])
        return (row[0], row[1])

# get_nom_and_statut_with_email(cnx, "leo@")

def get_utilisateur_is_in_db_with_email_passwrd(cnx, email,mot_de_passe):
    result = cnx.execute(text("select * from UTILISATEUR where email = '" + email + "' and mdp = '" + mot_de_passe + "';"))
    for _ in result:
        return True
    return False

def get_blob_with_ifd_and_idrisque(cnx, idF, idR):
    result = cnx.execute(text("select pictogramme from RISQUES where idFDS = '" + str(idF) + "' and idRisque = '" + str(idR) + "';"))
    for row in result:
        print(row[0])
        return row[0]
# print(get_utilisateur_is_in_db_with_email_passwrd(cnx, "DUPONT@gmail.com", "azerty"))

def get_user_with_statut(cnx, nomStatut):
    list = []
    result = cnx.execute(text("select * from UTILISATEUR natural join STATUT where nomStatut = '" + str(nomStatut) + "';"))
    for row in result:
        print(row[0],row[2],row[3])
        list.append((row[0],row[2],row[3]))
    return list
        

# get_user_with_statut(cnx, "Administrateur")

def get_nb_alert(cnx):
    try:
        # Calculer la date qui est 1 mois à partir de maintenant
        one_month_ago = datetime.now() - timedelta(days=30)
        one_month_ago_str = one_month_ago.strftime('%Y-%m-%d')
        # Exécuter la requête SQL
        result = cnx.execute(text("SELECT COUNT(*) FROM MATERIEL NATURAL JOIN DATEPEREMPTION WHERE datePeremption < '" + one_month_ago_str + "';"))
        count = result.first()[0]
        print(count)
        return count
    except Exception as e:
        print("Erreur lors de la récupération du nombre d'alertes :", str(e))
        raise

# get_nb_alert(cnx)


def nb_jour_ecart(date_string):
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    today = datetime.now()
    difference = ( date_obj - today).days
    print(difference)
    return difference


# nb_jour_ecart("2021-12-01")


def get_nb_demande(cnx):
    try:
        result = cnx.execute(text("SELECT count(*) FROM DEMANDE NATURAL JOIN BONCOMMANDE NATURAL JOIN ETATCOMMANDE WHERE nomEtat = 'En attente';"))
        count = result.first()[0]
        print(count)
        return count
    except Exception as e:
        print("Erreur lors de la récupération du nombre de demandes :", str(e))
        raise

# get_nb_demande(cnx)

def get_pictogramme(cnx, idRisque):
    result = cnx.execute("select pictogramme from RISQUE where idRisque = %s", idRisque)
    for row in result:
        req_annexe.extract_data(row[0], "pictograme"+str(idRisque)+".png")

# get_pictogramme(cnx, 51)