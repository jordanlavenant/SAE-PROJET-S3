from datetime import date, datetime, timedelta
from sqlalchemy import text
import random
import string
from hashlib import sha256



def update_email_utilisateur(cnx, new_email, nom, mdp):
    try:
        mdp_hash = hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("email mis a jour")
    except:
        print("erreur de mise a jour de l'email")
        raise

# update_email_utilisateur(cnx,"leo@", "leo" ,"12oXevnYPs")


def update_droit_utilisateur(cnx, id, idSt):
    try:
        cnx.execute(text( "update UTILISATEUR set idStatut = '" + str(idSt) + "' where idUtilisateur = '" + str(id) + "';"))
        cnx.commit()
        print("droit mis a jour")
    except:
        print("erreur de mise a jour du droit")
        raise

# update_droit_utilisateur(cnx, 5 , 1)


def update_mdp_utilisateur(cnx, email,mdp, new_mdp):
    try:
        init_mdp = hasher_mdp(mdp)
        new_mdp_hash = hasher_mdp(new_mdp)
        mdp_get = get_password_hashed_with_email(cnx, email)
        if mdp_get != init_mdp:
            print("mdp incorrect")
            return False
        else:
            cnx.execute(text(" update UTILISATEUR set motDePasse = '" + new_mdp_hash + "' where email = '" + email + "' and motDePasse = '" + init_mdp + "'"))
            cnx.commit()
            print("mdp mis a jour")
            return True
    except:
        print("erreur de mise a jour du mdp")
        return None

# update_mdp_utilisateur(cnx, "leo@", "leo","leoo")







# normalement on ne les utilise pas #

def update_nom_utilisateur(cnx, email, new_nom, mdp):
    try:
        mdp_hash = hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("nom mis a jour")
    except:
        print("erreur de mise a jour du nom")
        raise

#update_nom_utilisateur(cnx, "leo@kd", "lucidor", "leo")

def update_prenom_utilisateur(cnx, email, new_prenom, mdp):
    try:
        mdp_hash = hasher_mdp(mdp)
        cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "' and motDePasse = '" + mdp_hash + "';"))
        cnx.commit()
        print("prenom mis a jour")
    except:
        print("erreur de mise a jour du prenom")
        raise

# update_prenom_utilisateur(cnx, "newDupont@gmail.com", "newPierre")







# ----------------------------------- GET ----------------------------------#




def afficher_table(cnx, table):

    result = cnx.execute(text("select * from " + table + ";"))
    for row in result:
        print(row[0])


# afficher_table(cnx, "RECHERCHEMATERIELS")


def get_nom_and_statut_and_email(cnx, email):
    result = cnx.execute(text("select nom, idStatut from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0], row[1])
        return (row[0], row[1], email)
    
def get_password_with_email(cnx, email):
    result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]

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

# get_id_ut_with_email(cnx, "alice.johnson@example.com")

def get_password_hashed_with_email(cnx, email):
    result = cnx.execute(text("select motDePasse from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]

# get_password_hashed_with_email(cnx, "alice.johnson@example.com")

def get_statut_with_email(cnx, email):
    result = cnx.execute(text("select nomStatut from UTILISATEUR natural join STATUT where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]
    
# get_statut_with_email(cnx, "alice.johnson@example.com")


def get_nom_and_statut_with_email(cnx, email):
    result = cnx.execute(text("select nom, idStatut from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0], row[1])
        return (row[0], row[1])

# get_nom_and_statut_with_email(cnx, "alice.johnson@example.com")

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




# def get_pictogramme(cnx, idRisque):
#     result = cnx.execute("select pictogramme from RISQUE where idRisque = %s", idRisque)
#     for row in result:
#         extract_data(row[0], "pictograme"+str(idRisque)+".png")

# # get_pictogramme(cnx, 51)






def generer_mot_de_passe():
    caracteres = string.ascii_letters + string.digits
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

    return mot_de_passe

def hasher_mdp(mdp):
    m = sha256()
    m.update(mdp.encode("utf-8"))
    return m.hexdigest()



# Convert images or files data to binary format
def convert_data(file_name):
    with open(file_name, 'rb') as file:
        binary_data = file.read()
    return binary_data



# ----------------------------------- AJOUT ----------------------------------#


def ajout_proffesseur(cnx, nom, prenom, email, mdp, idStatut = 1):
    
    try:
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text( "insert into UTILISATEUR (nom, prenom, email, mdp, idStatut) values ('" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "', '" + str(idStatut) + "');" ))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise


# ajout_proffesseur(cnx, "lucidor", "leo", "leo@", "leo")

def ajout_administrateur(cnx, nom, prenom, email, idStatut = 2):
    
    try:
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR (nom, prenom, email, mdp, idStatut) values ('" + nom + "', '" + prenom + "', '" + email + "', '" + mdphash +  "', '" + str(idStatut) + "');"))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise

# ajout_administrateur(cnx, "admin", "admin", "admin@testhash2")

def ajout_gestionnaire(cnx, nom, prenom, email, idStatut = 3):
        
        try:
            mdpRandom = generer_mot_de_passe()
            # envoyer mail avec mdpRandom
            print(mdpRandom)
            mdphash = hasher_mdp(mdpRandom)
            cnx.execute(text("insert into UTILISATEUR (idStatut, nom, prenom, email, motDePasse) values ('" + str(idStatut) + "', '" +  nom + "', '" + prenom + "', '" + email +  "', '" + mdphash + "');"))
            cnx.commit()
            print("utilisateur ajouté")
        except:
            print("erreur d'ajout de l'utilisateur")
            raise


# ajout_gestionnaire(cnx, "colin", "colin", "colin@")

def add_proffesseur(cnx, nom, prenom, email, mdp, idSt = 1):
    
    try:
        mdpRandom = generer_mot_de_passe()
        # envoyer mail avec mdpRandom
        print(mdpRandom)
        mdphash = hasher_mdp(mdpRandom)
        cnx.execute(text("insert into UTILISATEUR ( nom, prenom, email, mdp, idSt) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idSt) + "');"))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise


def ajout_fournisseur(cnx, nom, adresse,mail, tel):
    try:
        cnx.execute(text("insert into FOURNISSEUR (idFournisseur, nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values (" +  nom + "', '" + adresse + "', '"  + mail + "', '"+ tel + "');"))
        cnx.commit()
        print("fournisseur ajouté")
    except:
        print("erreur d'ajout du fournisseur")
        raise



def ajoute_materiel(cnx, nom, idDom, idCat):
    try:
        cnx.execute(text("insert into MATERIAUX (idDom, idCategorie, idFDS, nomMateriel ) values (" + nom + "', " + str(idDom) + ", " + str(idCat) + ");"))
        cnx.commit()
        print("materiel ajouté")
    except:
        print("erreur d'ajout du materiel")
        raise



def ajout_quantite(cnx, idMat, quantite):
    try:
        cnx.execute(text("insert into STOCK (idMat, quantite) values (" + str(idMat) + ", " + str(quantite) + ");"))
        cnx.commit()
        print("quantite ajouté dans un nouveau stock")
    except:
        print("id deja utiliser")
        try:
            cnx.execute(text("update STOCK set quantite = quantite + " + str(quantite) + " where idMat = " + str(idMat) +";"))
            cnx.commit()
            print("quantite ajouté")
        except:
            print("erreur d'ajout de la quantité")
            raise

# ajout_quantite(cnx, 3, 50)




def delete_utilisateur(cnx, idUt):
    try:
        cnx.execute(text( "delete from UTILISATEUR where idUtilisateur = '" + str(idUt) + " ';"))
        cnx.commit()
        print("utilisateur supprimé")
    except:
        print("erreur de suppression de l'utilisateur")
        raise

# def ajout_blob_in_risques(cnx, idFDS, idRisque, file_path):
#     try:
#         blob = convert_data(file_path)
#         cnx.execute("insert into RISQUE (idRisque, nomRisque, pictogramme) values (%s, %s, %s);", idFDS, idRisque, blob)
#         cnx.commit()
#         print("Blob ajouté")
#     except Exception as e:
#         raise

# ajout_blob_in_risques(cnx, 4, 1, "r.png")
