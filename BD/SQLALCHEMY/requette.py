from sqlalchemy import text
import connexionPythonSQL
cnx= connexionPythonSQL.ouvrir_connexion()

#. Ecrire une fonction pour obtenir le plus grand num´ero utilis´e pour identifier un article
def maxNumArticle(cnx):
    """
    paramètre:
        cnx (Connection) la connexion à la base de données
    résultat: le plus grand numéro d'article
    """
    #. Ecrire une requête SQL qui permet d'obtenir le plus grand numéro d'article
    requete = text("select max(reference) from Article;")
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.first()[0]
    #. Renvoyer le résultat
    return res


    
#. Ecrire une fonction qui prend en param`etre un num´ero et retourne l’article de la base de donn´ees qui a ce num´ero.
def getArticle(cnx,num):
    """
    paramètres:
    cnx (Connection) la connexion à la base de données
    num (int) le numéro de l'article
    résultat: l'article de la base de données qui a ce numéro
    """
    #. Ecrire une requête SQL qui permet d'obtenir l'article qui a le numéro num
    requete = text("SELECT * FROM article WHERE reference = "+str(num))
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.first()[1]
    #. Renvoyer le résultat
    return res
    
#. Ecrire une fonction pour obtenir l’article qui a le plus grand identifiant.
def maxArticle(cnx):
    """
    paramètre:
       cnx (Connection) la connexion à la base de données
    résultat: l'article qui a le plus grand identifiant
    """
    #. Ecrire une requête SQL qui permet d'obtenir l'article qui a le plus grand identifiant
    requete = text("SELECT * FROM article WHERE reference = (SELECT MAX(reference) FROM article);")
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.fetchone()
    #. Renvoyer le résultat
    return res

#Ecrire une fonction qui retourne la liste des articles.
def listeArticle(cnx):
    """
    paramètre:
       cnx (Connection) la connexion à la base de données
    résultat: la liste des articles
    """
    #. Ecrire une requête SQL qui permet d'obtenir la liste des articles
    requete = text("SELECT * FROM article;")
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.fetchall()
    #. Renvoyer le résultat
    return res

#Ecrire une proc´edure pour afficher tous les entrepˆots tri´es par d´epartement avec pour chaque d´epartement, le nombre d’entrepˆots qu’a le d´epartement.
def entrepotParDepartement(cnx):
    """
    paramètre:
       cnx (Connection) la connexion à la base de données
    résultat: la liste des entrepôts triés par département avec pour chaque département, le nombre d'entrepôts qu'a le département
    """
    #. Ecrire une requête SQL qui permet d'obtenir la liste des entrepôts triés par département avec pour chaque département, le nombre d'entrepôts qu'a le département
    requete = text("SELECT departement, count(*) FROM entrepot GROUP BY departement ORDER BY departement;")
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.fetchall()
    #. Renvoyer le 
    
    # for (ville,nb) in res:
    #     print("Il y a ",nb," Entrepot(s) dans la ville " ,ville)
    return res

#Ecrire une proc´edure qui pour un num´ero d’article, affiche la liste des entrepˆots disposant de cet article avec leur quantit´e disponible
def entrepotArticle(cnx,num):
    """
    paramètres:
       cnx (Connection) la connexion à la base de données
       num (int) le numéro de l'article
    résultat: la liste des entrepôts disposant de cet article avec leur quantité disponible
    """
    #. Ecrire une requête SQL qui permet d'obtenir la liste des entrepôts disposant de cet article avec leur quantité disponible
    requete = text("SELECT * FROM Entrepot natural join Stocker WHERE reference = "+str(num))
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.fetchall()
    #. Renvoyer le résultat
    return res

#Ecrire une proc´edure qui pour un num´ero d’entrepˆot, affiche la liste des articles (avec leur quantit´e) disponibles dans l’entrepˆot.
def articleEntrepot(cnx,num):
    """
    paramètres:
       cnx (Connection) la connexion à la base de données
       num (int) le numéro de l'entrepôt
    résultat: la liste des articles (avec leur quantité) disponibles dans l'entrepôt
    """
    #. Ecrire une requête SQL qui permet d'obtenir la liste des articles (avec leur quantité) disponibles dans l'entrepôt
    requete = text("SELECT libelle, quantite FROM Article natural join Stocker WHERE code = "+str(num))
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.fetchall()
    #. Renvoyer le résultat
    return res

#Ecrire une fonction qui retourne la valeur contenue dans un entrepˆot donn´e.

def valeurEntrepot(cnx, num):
    """
    paramètres:
       cnx (Connection) la connexion à la base de données
       num (int) le numéro de l'entrepôt
    résultat: la valeur contenue dans l'entrepôt
    """
    #. Ecrire une requête SQL qui permet d'obtenir la valeur contenue dans l'entrepôt
    requete = text("select nom, (quantite*prix) as valeur from Entrepot natural join Stocker natural join Article where code =" + str(num))
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res =res.fetchall()
    #. Renvoyer le résultat
    return res 

# Ecrire une fonction qui permet de stocker un nouvel article dans la table article ou
# de modifier le prix d’un article d´ej`a existant. Par exemple si l’article est a=(123,
# "tuile17x27", 3.55) alors majArticle(a) modifiera le prix de l’article 123 s’il
# existe et qu’il correspond `a ’tuile 17x27’, si ne nom n’est pas ’tuile17x27’ afficher
# un message d’erreur, si l’article 123 n’est pas dans la base ajouter un nouvel article
# en prenant comme r´ef´erence la plus grande des r´ef´erences pr´esentes dans la base plus
# 1 `a la place de 123. La fonction retournera la r´ef´erence de l’article cr´e´e ou modifi´e (-1
# si erreur).

def majArticle(cnx, article):
    """
    paramètres:
       cnx (Connection) la connexion à la base de données
       article (tuple) le tuple qui contient les informations de l'article
    résultat: la référence de l'article créé ou modifié (-1 si erreur)
    """
    #. Ecrire une requête SQL qui permet de modifier le prix d'un article déjà existant
    requete = text("UPDATE Article SET prix = "+str(article[2])+" WHERE reference = "+str(article[0])+" AND libelle = '"+str(article[1])+"';")
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.fetchall()
    #. Renvoyer le résultat
    return res

# Ecrire une fonction qui ajoute un entrepˆot dans la base de donn´ees. La fonction
# retournera l’identifiant de l’entrepˆot ajout´e, -1 si erreur. Attention aux contrainte :
# on ne veut pas avoir plusieurs entrepˆots avec le mˆeme nom dans le mˆeme d´epartement,
# et on ne veut pas plus de trois entrepˆots dans un mˆeme d´epartement.

def ajouterEntrepot(cnx, entrepot):
    """
    paramètres:
       cnx (Connection) la connexion à la base de données
       entrepot (tuple) le tuple qui contient les informations de l'entrepôt
    résultat: l'identifiant de l'entrepôt ajouté, -1 si erreur
    """
    #. Ecrire une requête SQL qui permet d'ajouter un entrepôt dans la base de données
    requete = text("INSERT INTO Entrepot (nom, departement) VALUES ('"+str(entrepot[0])+"', "+str(entrepot[1])+");")
    #. Exécuter la requête
    res = cnx.execute(requete)
    #. Récupérer le résultat de la requête
    res = res.fetchall()
    #. Renvoyer le résultat
    return res

# Ecrire une fonction entrerStock(refA int, codeE int, qte int) qui augmente
# le stock de l’article refA dans l’entrepˆot codeE de qte. Retourne la nouvelle quantit´e
# de l’article (-1) quand l’article ou l’entrepˆot n’existe pas.

def entrerStock(cnx, refA, codeE, qte):
    requeteView = text("create or replace view viewQuentite as select reference, code, quantite from Article natural join Stocker natural join Entrepot")
    cnx.execute(requeteView)
    requete = text("UPDATE NJ SET quantite = quantite+"+str(qte)+" WHERE reference = "+str(refA)+" AND code = " + str(codeE))
    res = cnx.execute(requete)
    res = res.update()

    # verif
    # requeteVerif = text("select * from Article natural join Stocker natural join Entrepot where  reference = "+ str(refA) +" AND code = " + str(codeE))
    # resVerif = cnx.execute(requeteVerif)
    # resVerif = resVerif.fetchall()
    # return resVerif
# Ecrire une fonction sortirStock(refA int, codeE int, qte int) qui diminue le
# stock de l’article refA dans l’entrepˆot codeE de qte. La quantit´e `a sortir est limit´ee
# `a la quantit´e pr´esente. Retourne la quantit´e r´eellement sortie.
