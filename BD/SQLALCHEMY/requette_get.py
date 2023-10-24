from sqlalchemy import text
import connexionPythonSQL as conn
import requette_annexe as req_annexe

cnx = conn.get_cnx()

def afficher_table(cnx, table):

    result = cnx.execute(text("select * from " + table + ";"))
    for row in result:
        print(row)


afficher_table(cnx, "RECHERCHEMATERIELS")


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

# print(get_utilisateur_is_in_db_with_email_passwrd(cnx, "DUPONT@gmail.com", "azerty"))