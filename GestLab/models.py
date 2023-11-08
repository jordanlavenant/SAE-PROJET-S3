#from .app import db
from flask_login import UserMixin
from .app import login_manager
from .connexionPythonSQL import *
import smtplib
import json
from email.message import EmailMessage
import smtplib
import json
from email.message import EmailMessage

@login_manager.user_loader
def load_user(email):
    cnx = get_cnx()
    return get_nom_whith_email(cnx, email)

def envoyer_mail_reset_2FA(mailreceveur,key):
    json_file = open('GestLab/static/data/configEmail.json')
    gmail_config = json.load(json_file)
    msg = EmailMessage()
    msg['Subject'] = 'Rénitialisation de la A2F'
    msg['From'] = gmail_config["email"]
    msg['To'] = mailreceveur
    
    # Utilisation de balises HTML pour incorporer l'image dans le corps du message
    text_with_image = f'''
    <html>
    <head>
        <style>
            a{{
                text-decoration: none;
            }}

            p,li {{
                font-size: 20px;
            }}

            .alert {{
                font-size: 25px;
                color: red;
            }}

            img {{
                width: 300px;
                height: 300px;
            }}
        </style>
    </head>
    <body>
        <p>Vous avez oublié votre clé A2F.</p>
        <p class='alert'>Pour des raisons de sécurité veillez à ne pas partager ces informations !</p>
        <p>Voici la nouvelle clé d'authentification: {key}</p>
        <p>Voici le nouveau QR code pour le mettre dans une application externe d'authentification :  </p>
        <img src="cid:image1">
        <p> Voici quleques applications d'authentification : </p>
        <ul>
            <li><a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&pcampaignid=web_share">Google Authenticator</li>
            <li><a href="https://play.google.com/store/apps/details?id=com.twofasapp&pcampaignid=web_share">2FA Authenticator (2FAS)</li>
            <li><a href="https://play.google.com/store/apps/details?id=com.azure.authenticator&pcampaignid=web_share">Microsoft Authenticator</li>
            <li><a href="https://play.google.com/store/apps/details?id=org.fedorahosted.freeotp&pcampaignid=web_share">FreeOTP Authenticator</li>
        </ul>
    </body>
    </html>
    '''
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


def envoyer_mail(mailreceveur, mdp, key):
    json_file = open('GestLab/static/data/configEmail.json')
    gmail_config = json.load(json_file)

    msg = EmailMessage()
    msg['Subject'] = 'A2F - Création de compte GestLab - Email automatique ne pas répondre !'
    msg['From'] = gmail_config["email"]
    msg['To'] = mailreceveur

    # Utilisation de balises HTML pour incorporer l'image dans le corps du message
    text_with_image = f'''
    <html>
    <head>
        <style>
            a{{
                text-decoration: none;
            }}

            p,li {{
                font-size: 20px;
            }}

            .alert {{
                font-size: 25px;
                color: red;
            }}

            img {{
                width: 300px;
                height: 300px;
            }}

            .logo {{
                width: 100px;
                height: 100px;
            }}
        </style>
    </head>
    <body>
        <p class='alert'>Pour des raisons de sécurité veillez à ne pas partager ces informations !</p>
        <p>Votre compte a été crée avec succès voici les informations correspondants :</p>
        <ul>
            <li>Voici le login: {mailreceveur}</li>
            <li>Voici le mot de passe temporaire: {mdp}</li>
        </ul>
        <p>Voici votre clé d'authentification: {key}</p>
        <p>Voici votre QR code pour le mettre dans une application externe d'authentification :  </p>
        <img src="cid:image1">
        <p> Voici quleques applications d'authentification : </p>
        <ul>
            <li><a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&pcampaignid=web_share">Google Authenticator</li>
            <li><a href="https://play.google.com/store/apps/details?id=com.twofasapp&pcampaignid=web_share">2FA Authenticator (2FAS)</li>
            <li><a href="https://play.google.com/store/apps/details?id=com.azure.authenticator&pcampaignid=web_share">Microsoft Authenticator</li>
            <li><a href="https://play.google.com/store/apps/details?id=org.fedorahosted.freeotp&pcampaignid=web_share">FreeOTP Authenticator</li>
        </ul>
    </body>
    <footer>
        <br>
        <p>Si vous n'avez pas demandé de création de compte veuillez ignorer ce mail.</p>
        <img class="logo" src="https://cdn.discordapp.com/attachments/1171757951124525127/1171757962973429780/logo-GestLab.png?ex=655dd7a4&is=654b62a4&hm=457ba97c61b08dcb5941590e280bf720a72dba79dc96c86680d3005ff6160121&">
    </footer>
    </html>
    '''
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
    msg['Subject'] = "Commentaire"

    #email de l'envoyeur
    msg['From'] = gmail_config["email"]

    #email du receveur
    msg['To'] = mailreceveur
    text_with_image = f'''
    <html>
    <head>
        <style>

            p{{
                font-size: 20px;
            }}

        

            img {{
                width: 300px;
                height: 300px;
            }}

            .logo {{
                width: 100px;
                height: 100px;
            }}
        </style>
    </head>
    <body>
        <p>Voici le commentaire de la part de : {mailenvoyeur}</p>
        <p>{text}</p>
    </body>
    <footer>
        <img class="logo" src="https://cdn.discordapp.com/attachments/1171757951124525127/1171757962973429780/logo-GestLab.png?ex=655dd7a4&is=654b62a4&hm=457ba97c61b08dcb5941590e280bf720a72dba79dc96c86680d3005ff6160121&">
    </footer>
    </html>
    '''
    msg.add_alternative(text_with_image, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', gmail_config["port"]) as smtp:
        smtp.login(gmail_config["email"], gmail_config["password"])
        smtp.send_message(msg)
        print("Mail envoyé")



def envoyer_mail_signalement(mailreceveur, mailenvoyeur, text, objet):
    json_file = open('GestLab/static/data/configEmail.json')
    gmail_config = json.load(json_file)

    msg = EmailMessage()
    msg['Subject'] = "Signalement"

    #email de l'envoyeur
    msg['From'] = gmail_config["email"]

    #email du receveur
    msg['To'] = mailreceveur
    text_with_image = f'''
    <html>
    <head>
        <style>

            p{{
                font-size: 20px;
            }}

            img {{
                width: 300px;
                height: 300px;
            }}

            .logo {{
                width: 100px;
                height: 100px;
            }}
        </style>
    </head>
    <body>
        <p>Votre compte a été crée avec succès voici les informations correspondants :</p>
        <p>Voici le signalement de la part de : {mailenvoyeur}</p>
        <p>Voici l'objet concerné : {objet}</p>
    </body>
    <footer>
        <img class="logo" src="https://cdn.discordapp.com/attachments/1171757951124525127/1171757962973429780/logo-GestLab.png?ex=655dd7a4&is=654b62a4&hm=457ba97c61b08dcb5941590e280bf720a72dba79dc96c86680d3005ff6160121&">
    </footer>
    </html>
    '''
    msg.add_alternative(text_with_image, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', gmail_config["port"]) as smtp:
        smtp.login(gmail_config["email"], gmail_config["password"])
        smtp.send_message(msg)
        print("Mail envoyé")

def envoyer_mail_mdp_oublie(mailreceveur, mdp):
    json_file = open('GestLab/static/data/configEmail.json')
    gmail_config = json.load(json_file)

    msg = EmailMessage()
    msg['Subject'] = 'Récuperation de compte GestLab - Email automatique ne pas répondre !'
    msg['From'] = gmail_config["email"]
    msg['To'] = mailreceveur

    # Utilisation de balises HTML pour incorporer l'image dans le corps du message
    text_with_image = f'''
    <html>
    <head>
        <style>
            a{{
                text-decoration: none;
            }}

            p,li {{
                font-size: 20px;
            }}

            .alert {{
                font-size: 25px;
                color: red;
            }}

            img {{
                width: 300px;
                height: 300px;
            }}

            .logo {{
                width: 100px;
                height: 100px;
            }}
        </style>
    </head>
    <body>
        <p class='alert'>Pour des raisons de sécurité veillez à ne pas partager ces informations !</p>
        <p>Votre compte a été récuperer avec succès voici les informations correspondants :</p>
        <ul>
            <li>Voici le login: {mailreceveur}</li>
            <li>Voici le mot de passe temporaire: {mdp}</li>
        </ul>
    </body>
    <footer>
        <br>
        <p>Si vous n'avez pas demandé de récuperation de compte veuillez contacter un administrateur.</p>
        <img class="logo" src="https://cdn.discordapp.com/attachments/1171757951124525127/1171757962973429780/logo-GestLab.png?ex=655dd7a4&is=654b62a4&hm=457ba97c61b08dcb5941590e280bf720a72dba79dc96c86680d3005ff6160121&">
    </footer>
    </html>
    '''
    msg.add_alternative(text_with_image, subtype='html')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', gmail_config["port"]) as smtp:
        smtp.login(gmail_config["email"], gmail_config["password"])
        smtp.send_message(msg)
        print("Mail envoyé")