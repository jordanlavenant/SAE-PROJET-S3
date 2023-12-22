from hashlib import sha256
import random
import string
from sqlalchemy import text

from GestLab.models import envoyer_mail_mdp_oublie


class Mots_de_passe:
    
    def generer_mot_de_passe():
        """
        Génère un mot de passe aléatoire composé de lettres majuscules, lettres minuscules et chiffres.
        
        Returns:
            str: Le mot de passe généré.
        """
        caracteres = string.ascii_letters + string.digits
        mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

        return mot_de_passe

    
    def hasher_mdp(mdp):
        """
        Hashes the given password using SHA-256 algorithm.

        Args:
            mdp (str): The password to be hashed.

        Returns:
            str: The hashed password in hexadecimal format.
        """
        m = sha256()
        m.update(mdp.encode("utf-8"))
        return m.hexdigest()
    
    def recuperation_de_mot_de_passe(cnx, email):
        """
        Cette fonction permet de récupérer le mot de passe d'un utilisateur à partir de son adresse email.
        
        Args:
            cnx (object): L'objet de connexion à la base de données.
            email (str): L'adresse email de l'utilisateur.
        
        Returns:
            bool: True si le mot de passe a été mis à jour et envoyé avec succès, False sinon.
        """
        try:
            mdpRandom = Mots_de_passe.generer_mot_de_passe()
            print(mdpRandom)
            mdphash = Mots_de_passe.hasher_mdp(mdpRandom)
            cnx.execute(text("update UTILISATEUR set motDePasse = '" + mdphash + "' where email = '" + email + "';"))
            cnx.commit()
            envoyer_mail_mdp_oublie(email, mdpRandom)
            print("mdp mis a jour")
            return True
        except:
            print("erreur de mise a jour du mdp")
            return False
