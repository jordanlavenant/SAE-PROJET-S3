#from .app import db
from flask_login import UserMixin
from .app import login_manager
from .connexionPythonSQL import *
import smtplib
import json
from email.message import EmailMessage

@login_manager.user_loader
def load_user(email):
    cnx = get_cnx()
    return get_nom_whith_email(cnx, email)

def envoyer_mail_nouveau_compte(mailreceveur, mdp):
    json_file = open('Gestlab/static/data/configEmail.json')
    gmail_config = json.load(json_file)

    msg = EmailMessage()
    msg['Subject'] = 'Test email'

    #email de l'envoyeur
    msg['From'] = gmail_config["email"]

    #email du receveur
    msg['To'] = mailreceveur
    msg.set_content('Voici le login: ' + mailreceveur  + ' \nVoici le mots de passe temporaire: ' + mdp)
 
    with smtplib.SMTP_SSL('smtp.gmail.com', gmail_config["port"]) as smtp:
        smtp.login(gmail_config["email"], gmail_config["password"])
        smtp.send_message(msg)
        print("Mail envoyé")

def envoyer_mail(mailreceveur, login, mdp, key):
    json_file = open('GestLab/static/data/configEmail.json')
    gmail_config = json.load(json_file)

    msg = EmailMessage()
    msg['Subject'] = '2FA'
    msg['From'] = gmail_config["email"]
    msg['To'] = mailreceveur

    # Texte de l'e-mail avec l'image incorporée
    text = f'Voici le login: {login}\nVoici le mot de passe temporaire: {mdp} et la clé : {key} '
    
    # Utilisation de balises HTML pour incorporer l'image dans le corps du message
    text_with_image = f'<html><body>{text}<br><img src="cid:image1"></body></html>'
    msg.add_alternative(text_with_image, subtype='html')
    
    # Image à ajouter en tant que pièce jointe et incorporée dans le corps
    image_path = './qrcode.png'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        msg.add_attachment(image_data, maintype='image', subtype='jpg', filename='image.jpg', cid='image1')

    with smtplib.SMTP_SSL('smtp.gmail.com', gmail_config["port"]) as smtp:
        smtp.login(gmail_config["email"], gmail_config["password"])
        smtp.send_message(msg)
        print("Mail envoyé")


def envoyer_mail_commentaire(mailreceveur, mailenvoyeur, text):
    json_file = open('GestLab/static/data/configEmail.json')
    gmail_config = json.load(json_file)

    msg = EmailMessage()
    msg['Subject'] = 'Test email'

    #email de l'envoyeur
    msg['From'] = gmail_config["email"]

    #email du receveur
    msg['To'] = mailreceveur
    msg.set_content('Voici le commentaire de la part de '+ mailenvoyeur + ' : \n\n'+text)
 
    with smtplib.SMTP_SSL('smtp.gmail.com', gmail_config["port"]) as smtp:
        smtp.login(gmail_config["email"], gmail_config["password"])
        smtp.send_message(msg)
        print("Mail envoyé")

    