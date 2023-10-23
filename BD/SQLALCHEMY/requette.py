from sqlalchemy import text
import connexionPythonSQL
cnx= connexionPythonSQL.ouvrir_connexion()

def afficher_table(cnx, table):

    result = cnx.execute(text("select * from " + table + " natural join MATERIAUX;"))
    for row in result:
        print(row)


# afficher_table(cnx, "STOCK")

def get_last_id(cnx , table, id):
    try:
        result = cnx.execute(text("select max("+ id +") from " + table + ";"))
        result = result.first()[0]
        print(result)
        return result
    except:
        print("erreur du nom de l'id ou du nom de la table")
        raise

# get_last_id(cnx, "STOCK", "idMat")

def get_nom_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIAUX where idMat = " + str(id) + ";"))
        result = result.first()
        print(result[1])
    except:
        print("erreur de l'id")
        raise

# get_nom_materiel_with_id(cnx, 3)

def get_nom_dom_cat_materiel_with_id(cnx, id):
    try:
        result = cnx.execute(text("select * from MATERIAUX natural join DOMAINE natural join CATEGORIE where idMat = " + str(id) + ";"))
        result = result.first()
        print("domaine : " + result[4], " | categorie : ",result[5])
    except:
        print("erreur de l'id")
        raise

# get_nom_dom_cat_materiel_with_id(cnx, 1)


def ajoute_materiel(cnx, nom, idDom, idCat):
    try:
        last_id = int(get_last_id(cnx, "MATERIAUX", "idMat")) + 1
        cnx.execute(text("insert into MATERIAUX (idMat,nomMat, idDom, idCat) values (" + str(last_id) + ", '" + nom + "', " + str(idDom) + ", " + str(idCat) + ");"))
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


def ajout_fournisseur(cnx, nom, adresse,mail, tel):
    try:
        last_id = int(get_last_id(cnx, "FOURNISSEUR", "idFournisseur")) + 1
        cnx.execute(text("insert into FOURNISSEUR (idFournisseur, nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) values (" + str(last_id) + ", '" + nom + "', '" + adresse + "', '"  + mail + "', '"+ tel + "');"))
        cnx.commit()
        print("fournisseur ajouté")
    except:
        print("erreur d'ajout du fournisseur")
        raise

def connexion_utilisateur(cnx, email,mot_de_passe):
    result = cnx.execute(text("select * from UTILISATEUR where email = '" + email + "' and mdp = '" + mot_de_passe + "';"))
    for _ in result:
        return True
    return False

# print(connexion_utilisateur(cnx, "DUPONT@gmail.com", "azerty"))


def get_nom_whith_email(cnx, email):
    result = cnx.execute(text("select nom from UTILISATEUR where email = '" + email + "';"))
    for row in result:
        print(row[0])
        return row[0]
    
#get_nom_whith_email(cnx, "DUPONT@gmail.com")

def get_materiaux(cnx):
    result = cnx.execute(text("select * from MATERIAUX_RECHERCHE;"))
    for row in result:
        print(row[0])

# get_materiaux(cnx)

def ajout_proffesseur(cnx, nom, prenom, email, mdp, idSt = 1):
    
    try:
        last_id = int(get_last_id(cnx, "UTILISATEUR", "idUt")) + 1
        cnx.execute(text("insert into UTILISATEUR (idUt, nom, prenom, email, mdp, idSt) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idSt) + "');"))
        cnx.commit()
        print("utilisateur ajouté")
    except:
        print("erreur d'ajout de l'utilisateur")
        raise

# ajout_proffesseur(cnx, "blandeau", "erwan", "test@gmail.com", "erwanB")


def ajout_gestionnaire(cnx, nom, prenom, email, mdp, idSt = 3):
        
        try:
            last_id = int(get_last_id(cnx, "UTILISATEUR", "idUt")) + 1
            cnx.execute(text("insert into UTILISATEUR (idUt, nom, prenom, email, mdp, idSt) values ('" + str(last_id) + "', '" + nom + "', '" + prenom + "', '" + email + "', '" + mdp +  "', '" + str(idSt) + "');"))
            cnx.commit()
            print("utilisateur ajouté")
        except:
            print("erreur d'ajout de l'utilisateur")
            raise

# ajout_gestionnaire(cnx, "blandeauG", "erwang", "testG", "erwanBG")


def update_email_utilisateur(cnx, new_email, nom, mdp):
    try:
        cnx.execute(text("update UTILISATEUR set email = '" + new_email + "' where nom = '" + nom + "' and mdp = '" + mdp + "';"))
        cnx.commit()
        print("email mis a jour")
    except:
        print("erreur de mise a jour de l'email")
        raise

# update_email_utilisateur(cnx,"newErwan@gmail.com", "blandeau" ,"erwanB")


def modification_droit_utilisateur(cnx, id, idSt):
    try:
        cnx.execute(text("update UTILISATEUR set idSt = '" + str(idSt) + "' where idUt = '" + id + "';"))
        cnx.commit()
        print("droit mis a jour")
    except:
        print("erreur de mise a jour du droit")
        raise

# modification_droit_utilisateur(cnx, "testG", 2)


def update_mdp_utilisateur(cnx, email, new_mdp):
    try:
        cnx.execute(text("update UTILISATEUR set mdp = '" + new_mdp + "' where email = '" + email + "';"))
        cnx.commit()
        print("mdp mis a jour")
    except:
        print("erreur de mise a jour du mdp")
        raise

# update_mdp_utilisateur(cnx, "newDupont@gmail.com", "newMdp")

def update_nom_utilisateur(cnx, email, new_nom):
    try:
        cnx.execute(text("update UTILISATEUR set nom = '" + new_nom + "' where email = '" + email + "';"))
        cnx.commit()
        print("nom mis a jour")
    except:
        print("erreur de mise a jour du nom")
        raise

# update_nom_utilisateur(cnx, "newDupont@gmail.com", "newDupont")

def update_prenom_utilisateur(cnx, email, new_prenom):
    try:
        cnx.execute(text("update UTILISATEUR set prenom = '" + new_prenom + "' where email = '" + email + "';"))
        cnx.commit()
        print("prenom mis a jour")
    except:
        print("erreur de mise a jour du prenom")
        raise

# update_prenom_utilisateur(cnx, "newDupont@gmail.com", "newPierre")



# def ajouterEntrepot(cnx, entrepot):
#     """
#     paramètres:
#        cnx (Connection) la connexion à la base de données
#        entrepot (tuple) le tuple qui contient les informations de l'entrepôt
#     résultat: l'identifiant de l'entrepôt ajouté, -1 si erreur
#     """
#     #. Ecrire une requête SQL qui permet d'ajouter un entrepôt dans la base de données
#     requete = text("INSERT INTO Entrepot (nom, departement) VALUES ('"+str(entrepot[0])+"', "+str(entrepot[1])+");")
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchall()
#     #. Renvoyer le résultat
#     return res


# def ajout_fournisseur(cnx, )


# # cration d'une table
# def creerTable(cnx):
#     cnx.execute("CREATE TABLE IF NOT EXISTS Article (reference int, libelle varchar(30), prix float, primary key(reference));")

    
# #. Ecrire une fonction qui prend en param`etre un num´ero et retourne l’article de la base de donn´ees qui a ce num´ero.
# def getArticle(cnx,num):
#     """
#     paramètres:
#     cnx (Connection) la connexion à la base de données
#     num (int) le numéro de l'article
#     résultat: l'article de la base de données qui a ce numéro
#     """
#     #. Ecrire une requête SQL qui permet d'obtenir l'article qui a le numéro num
#     requete = text("SELECT * FROM article WHERE reference = "+str(num))
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.first()[1]
#     #. Renvoyer le résultat
#     return res
    
# #. Ecrire une fonction pour obtenir l’article qui a le plus grand identifiant.
# def maxArticle(cnx):
#     """
#     paramètre:
#        cnx (Connection) la connexion à la base de données
#     résultat: l'article qui a le plus grand identifiant
#     """
#     #. Ecrire une requête SQL qui permet d'obtenir l'article qui a le plus grand identifiant
#     requete = text("SELECT * FROM article WHERE reference = (SELECT MAX(reference) FROM article);")
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchone()
#     #. Renvoyer le résultat
#     return res

# #Ecrire une fonction qui retourne la liste des articles.
# def listeArticle(cnx):
#     """
#     paramètre:
#        cnx (Connection) la connexion à la base de données
#     résultat: la liste des articles
#     """
#     #. Ecrire une requête SQL qui permet d'obtenir la liste des articles
#     requete = text("SELECT * FROM article;")
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchall()
#     #. Renvoyer le résultat
#     return res

# #Ecrire une proc´edure pour afficher tous les entrepˆots tri´es par d´epartement avec pour chaque d´epartement, le nombre d’entrepˆots qu’a le d´epartement.
# def entrepotParDepartement(cnx):
#     """
#     paramètre:
#        cnx (Connection) la connexion à la base de données
#     résultat: la liste des entrepôts triés par département avec pour chaque département, le nombre d'entrepôts qu'a le département
#     """
#     #. Ecrire une requête SQL qui permet d'obtenir la liste des entrepôts triés par département avec pour chaque département, le nombre d'entrepôts qu'a le département
#     requete = text("SELECT departement, count(*) FROM entrepot GROUP BY departement ORDER BY departement;")
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchall()
#     #. Renvoyer le 
    
#     # for (ville,nb) in res:
#     #     print("Il y a ",nb," Entrepot(s) dans la ville " ,ville)
#     return res

# #Ecrire une proc´edure qui pour un num´ero d’article, affiche la liste des entrepˆots disposant de cet article avec leur quantit´e disponible
# def entrepotArticle(cnx,num):
#     """
#     paramètres:
#        cnx (Connection) la connexion à la base de données
#        num (int) le numéro de l'article
#     résultat: la liste des entrepôts disposant de cet article avec leur quantité disponible
#     """
#     #. Ecrire une requête SQL qui permet d'obtenir la liste des entrepôts disposant de cet article avec leur quantité disponible
#     requete = text("SELECT * FROM Entrepot natural join Stocker WHERE reference = "+str(num))
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchall()
#     #. Renvoyer le résultat
#     return res

# #Ecrire une proc´edure qui pour un num´ero d’entrepˆot, affiche la liste des articles (avec leur quantit´e) disponibles dans l’entrepˆot.
# def articleEntrepot(cnx,num):
#     """
#     paramètres:
#        cnx (Connection) la connexion à la base de données
#        num (int) le numéro de l'entrepôt
#     résultat: la liste des articles (avec leur quantité) disponibles dans l'entrepôt
#     """
#     #. Ecrire une requête SQL qui permet d'obtenir la liste des articles (avec leur quantité) disponibles dans l'entrepôt
#     requete = text("SELECT libelle, quantite FROM Article natural join Stocker WHERE code = "+str(num))
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchall()
#     #. Renvoyer le résultat
#     return res

# #Ecrire une fonction qui retourne la valeur contenue dans un entrepˆot donn´e.

# def valeurEntrepot(cnx, num):
#     """
#     paramètres:
#        cnx (Connection) la connexion à la base de données
#        num (int) le numéro de l'entrepôt
#     résultat: la valeur contenue dans l'entrepôt
#     """
#     #. Ecrire une requête SQL qui permet d'obtenir la valeur contenue dans l'entrepôt
#     requete = text("select nom, (quantite*prix) as valeur from Entrepot natural join Stocker natural join Article where code =" + str(num))
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res =res.fetchall()
#     #. Renvoyer le résultat
#     return res 

# # Ecrire une fonction qui permet de stocker un nouvel article dans la table article ou
# # de modifier le prix d’un article d´ej`a existant. Par exemple si l’article est a=(123,
# # "tuile17x27", 3.55) alors majArticle(a) modifiera le prix de l’article 123 s’il
# # existe et qu’il correspond `a ’tuile 17x27’, si ne nom n’est pas ’tuile17x27’ afficher
# # un message d’erreur, si l’article 123 n’est pas dans la base ajouter un nouvel article
# # en prenant comme r´ef´erence la plus grande des r´ef´erences pr´esentes dans la base plus
# # 1 `a la place de 123. La fonction retournera la r´ef´erence de l’article cr´e´e ou modifi´e (-1
# # si erreur).

# def majArticle(cnx, article):
#     """
#     paramètres:
#        cnx (Connection) la connexion à la base de données
#        article (tuple) le tuple qui contient les informations de l'article
#     résultat: la référence de l'article créé ou modifié (-1 si erreur)
#     """
#     #. Ecrire une requête SQL qui permet de modifier le prix d'un article déjà existant
#     requete = text("UPDATE Article SET prix = "+str(article[2])+" WHERE reference = "+str(article[0])+" AND libelle = '"+str(article[1])+"';")
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchall()
#     #. Renvoyer le résultat
#     return res

# # Ecrire une fonction qui ajoute un entrepˆot dans la base de donn´ees. La fonction
# # retournera l’identifiant de l’entrepˆot ajout´e, -1 si erreur. Attention aux contrainte :
# # on ne veut pas avoir plusieurs entrepˆots avec le mˆeme nom dans le mˆeme d´epartement,
# # et on ne veut pas plus de trois entrepˆots dans un mˆeme d´epartement.

# def ajouterEntrepot(cnx, entrepot):
#     """
#     paramètres:
#        cnx (Connection) la connexion à la base de données
#        entrepot (tuple) le tuple qui contient les informations de l'entrepôt
#     résultat: l'identifiant de l'entrepôt ajouté, -1 si erreur
#     """
#     #. Ecrire une requête SQL qui permet d'ajouter un entrepôt dans la base de données
#     requete = text("INSERT INTO Entrepot (nom, departement) VALUES ('"+str(entrepot[0])+"', "+str(entrepot[1])+");")
#     #. Exécuter la requête
#     res = cnx.execute(requete)
#     #. Récupérer le résultat de la requête
#     res = res.fetchall()
#     #. Renvoyer le résultat
#     return res

# # Ecrire une fonction entrerStock(refA int, codeE int, qte int) qui augmente
# # le stock de l’article refA dans l’entrepˆot codeE de qte. Retourne la nouvelle quantit´e
# # de l’article (-1) quand l’article ou l’entrepˆot n’existe pas.

# def entrerStock(cnx, refA, codeE, qte):
#     requeteView = text("create or replace view viewQuentite as select reference, code, quantite from Article natural join Stocker natural join Entrepot")
#     cnx.execute(requeteView)
#     requete = text("UPDATE NJ SET quantite = quantite+"+str(qte)+" WHERE reference = "+str(refA)+" AND code = " + str(codeE))
#     res = cnx.execute(requete)
#     res = res.update()

#     # verif
#     # requeteVerif = text("select * from Article natural join Stocker natural join Entrepot where  reference = "+ str(refA) +" AND code = " + str(codeE))
#     # resVerif = cnx.execute(requeteVerif)
#     # resVerif = resVerif.fetchall()
#     # return resVerif
# # Ecrire une fonction sortirStock(refA int, codeE int, qte int) qui diminue le
# # stock de l’article refA dans l’entrepˆot codeE de qte. La quantit´e `a sortir est limit´ee
# # `a la quantit´e pr´esente. Retourne la quantit´e r´eellement sortie.
