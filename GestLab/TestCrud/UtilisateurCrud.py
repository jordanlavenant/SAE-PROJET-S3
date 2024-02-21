from sqlalchemy import text
import sqlalchemy

import  GestLab.Classe_python.Utilisateurs as Utilisateur
from GestLab.initialisation import get_cnx


cnx = get_cnx()

class UtilisateurCrud:

    class Ajout:
        def ajout_utilisateur():
            nom = input("Entrez le nom de l'utilisateur à ajouter: ")
            prenom = input("Entrez le prénom de l'utilisateur à ajouter: ")
            email = input("Entrez l'email de l'utilisateur à ajouter: ")
            choisirRole = input("Entrez le rôle de l'utilisateur à ajouter:\n 1- Administrateur\n 2- Professeur\n 3- Laborantin\n 4- Gestionnaire\n\n Votre choix: ")
            
            def switch(choix, nom, prenom, email):
                if choix == 1 or choix == "Administrateur":
                    Utilisateur.Utilisateur.Insert.ajout_administrateur(cnx,nom,prenom,email)
                elif choix == 2 or choix == "Professeur":
                    Utilisateur.Utilisateur.Insert.ajout_professeur(cnx,nom,prenom,email)
                elif choix == 3 or choix == "Laborantin":
                    Utilisateur.Utilisateur.Insert.ajout_laborantin(cnx,nom,prenom,email)
                elif choix == 4 or choix == "Gestionnaire":
                    Utilisateur.Utilisateur.Insert.ajout_gestionnaire(cnx,nom,prenom,email)
                else:
                    print("Choix invalide")
                    return

            switch(choisirRole, nom, prenom, email)


UtilisateurCrud.Ajout.ajout_utilisateur()
        
    