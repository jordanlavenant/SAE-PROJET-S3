import random
import string

def generer_mot_de_passe(longueur):
    caracteres = string.ascii_letters + string.digits
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mot_de_passe

longueur_mot_de_passe = 10

mot_de_passe_generé = generer_mot_de_passe(longueur_mot_de_passe)
print("Mot de passe généré :", mot_de_passe_generé)
