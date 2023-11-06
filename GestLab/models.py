#from .app import db
from flask_login import UserMixin
from .app import login_manager
from .requette import *
from .connexionPythonSQL import *
import smtplib
import json
from email.message import EmailMessage

@login_manager.user_loader
def load_user(email):
    cnx = get_cnx()
    return get_nom_whith_email(cnx, email)

def envoyer_mail(mailreceveur, login, mdp):
    json_file = open('Gestlab/static/data/configEmail.json')
    gmail_config = json.load(json_file)

    msg = EmailMessage()
    msg['Subject'] = 'Test email'

    #email de l'envoyeur
    msg['From'] = gmail_config["email"]

    #email du receveur
    msg['To'] = mailreceveur
    msg.set_content('Voici le login: ' + login  + ' \nVoici le mots de passe temporaire: ' + mdp)
 
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