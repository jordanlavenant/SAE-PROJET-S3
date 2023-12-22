import pyotp
import qrcode
from sqlalchemy import text

from GestLab.Classe_python.Utilisateurs import Utilisateur
from GestLab.models import envoyer_mail
from GestLab.initialisation import get_cnx


class Authentification:
    
    def random_key():
        """
        Generate a random base32 key using pyotp library.

        Returns:
            str: A random base32 key.
        """
        return pyotp.random_base32()

    def add_two_authenticator_in_bd(cnx,key, email, id):
        """
        Ajoute un nouvel enregistrement dans la base de données pour l'authentification à deux facteurs.

        Args:
            cnx (object): L'objet de connexion à la base de données.
            key (str): La clé d'authentification à deux facteurs.
            email (str): L'adresse e-mail de l'utilisateur.
            id (int): L'identifiant de l'utilisateur.

        Raises:
            Exception: En cas d'erreur lors de l'ajout de l'enregistrement.

        Returns:
            None
        """
        try:
            if id != None:
                cnx.execute(text("insert into 2FA (email,uri,idUtilisateur) values ('" + email + "', '" + key + "', '" + str(id) + "');"))
                cnx.commit()
                print("uri ajouté")
            else:
                print("id non trouvé")
        except:
            print("erreur d'ajout de l'uri")
            raise

    def create_uri(key,email):
        """
        Crée une URI de provisionnement pour l'authentification à deux facteurs.

        Args:
            key (str): La clé secrète utilisée pour générer les codes d'authentification.
            email (str): L'adresse e-mail de l'utilisateur.

        Returns:
            str: L'URI de provisionnement pour l'authentification à deux facteurs.
        """
        cnx = get_cnx()
        Authentification.add_two_authenticator_in_bd(cnx,key ,email,Utilisateur.Get.get_id_with_email(cnx, email) )
        return pyotp.totp.TOTP(key).provisioning_uri(name= email, issuer_name= "GestLab")

    def create_qr_code_utilisateur_deja_existant(cnx, email):
        """
        Crée un code QR pour un utilisateur existant.

        Args:
            cnx (object): L'objet de connexion à la base de données.
            email (str): L'adresse e-mail de l'utilisateur.

        Returns:
            None
        """
        uri = Utilisateur.Get.get_uri_with_email(cnx, email)
        qrcode.make(uri).save("qrcode.png")
    def create_qr_code_utilisateur_deja_existant(cnx,email):
        uri = Utilisateur.Get.get_uri_with_email(cnx,email)
        qrcode.make(uri).save("qrcode.png")

    def create_qr_code_nouvel_utlisateur(email, mdp):
        """
        Crée un code QR pour un nouvel utilisateur.

        Args:
            email (str): L'adresse e-mail de l'utilisateur.
            mdp (str): Le mot de passe de l'utilisateur.

        Returns:
            None
        """
        key = Authentification.random_key()
        uri = Authentification.create_uri(key,email)
        qrcode.make(uri).save("qrcode.png")
        envoyer_mail(email,mdp, key)

    def verify(key, code):
        """
        Verify the given code against the provided key.

        Parameters:
        key (str): The secret key used for generating the OTP.
        code (str): The code to be verified.

        Returns:
        bool: True if the code is valid, False otherwise.
        """
        return pyotp.TOTP(key).verify(code)
