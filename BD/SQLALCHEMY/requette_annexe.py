from hashlib import sha256
import connexionPythonSQL as conn
from sqlalchemy import text
import random
import string


cnx = conn.get_cnx()





def generer_mot_de_passe():
    caracteres = string.ascii_letters + string.digits
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(10))

    return mot_de_passe

def hasher_mdp(mdp):
    m = sha256()
    m.update(mdp.encode("utf-8"))
    return m.hexdigest()



