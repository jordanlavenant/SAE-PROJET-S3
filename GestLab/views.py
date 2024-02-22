from sqlalchemy import text

from GestLab.Classe_python.Alerte import Alert
import GestLab.Classe_python.Authentification as Authentification
import GestLab.Classe_python.BonCommande as Bon_commande 
import GestLab.Classe_python.Commande as Commande
import GestLab.Classe_python.Domaine as Domaine
from GestLab.Classe_python.Endroit import Endroit
from GestLab.Classe_python.FDS import FDS
from GestLab.Classe_python.Demande import Demande
from GestLab.Classe_python.Materiel import Materiel
from GestLab.Classe_python.MaterielUnique import MaterielUnique
from GestLab.Classe_python.MotDePasse import Mots_de_passe
from GestLab.Classe_python.Rangement import Rangement
from GestLab.Classe_python.Recherche import Recherche
from GestLab.Classe_python.Reload import RELOAD
from GestLab.Classe_python.ReserveLaboratoire import ReserveLaboratoire
from GestLab.Classe_python.Risque import Risques
from GestLab.Classe_python.StockLaboratoire import STOCKLABORATOIRE
from GestLab.Classe_python.ImportCSV import ImportCSV
from GestLab.Classe_python.ExportCSV import ExportCSV
from GestLab.Classe_python.Table import Table
from GestLab.Classe_python.Utilisateurs import Utilisateur
from GestLab.initialisation import get_cnx

from .app import app, csrf #, db
from flask import render_template, url_for, redirect, request, session, jsonify, send_file
from flask_login import login_user, current_user, logout_user, login_required
#from .models import User
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, HiddenField, FileField, SubmitField, SelectField, TextAreaField, DateField, BooleanField, RadioField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField
from hashlib import sha256
from .connexionPythonSQL import *
from .models import *
from .genererpdf import *

import time
import datetime
import os
from werkzeug.utils import secure_filename


cnx = get_cnx()

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        """
        Récupère l'utilisateur authentifié.

        Cette méthode récupère l'utilisateur authentifié en utilisant l'adresse e-mail fournie.
        Elle vérifie également si le mot de passe fourni correspond au mot de passe enregistré pour cet utilisateur.

        Returns:
            L'utilisateur authentifié si l'adresse e-mail et le mot de passe sont valides, sinon None.
        """
        user = Bon_commande.Utilisateur.Utilisateur.Get.get_nom_and_statut_and_email(cnx, self.email.data)
        print(user)
        mdp = Bon_commande.Utilisateur.Utilisateur.Get.get_password_with_email(cnx, self.email.data)
        if user is None:
            return None
        passwd = Mots_de_passe.hasher_mdp(self.password.data)
        print(str(mdp)+" == "+str(passwd))
        return user if passwd == mdp else None

class ChangerMDPForm(FlaskForm):
    ancienMDP = PasswordField('ancienMDP', validators=[DataRequired()])
    nouveauMDP = PasswordField('nouveauMDP', validators=[DataRequired()])
    confirmerMDP = PasswordField('confirmerMDP', validators=[DataRequired()])
    next = HiddenField()

    def get_full_mdp(self):
        """
        Récupère les valeurs des champs ancienMDP, nouveauMDP et confirmerMDP.

        Returns:
            Tuple[str, str, str]: Un tuple contenant les valeurs des champs ancienMDP, nouveauMDP et confirmerMDP.
        """
        ancienMDP = self.ancienMDP.data
        nouveauMDP = self.nouveauMDP.data
        confirmerMDP = self.confirmerMDP.data
        return (ancienMDP, nouveauMDP, confirmerMDP)

class ChangerMailForm(FlaskForm):
    ancienMail = StringField('ancienMail', validators=[DataRequired()])
    nouveauMail = StringField('nouveauMail', validators=[DataRequired()])
    confirmerMail = StringField('confirmerMail', validators=[DataRequired()])
    mdp = PasswordField('mdp', validators=[DataRequired()])
    next = HiddenField()

    def get_full_mail(self):
        """
        Récupère les informations complètes du formulaire de modification d'email.

        Returns:
            tuple: Un tuple contenant les valeurs des champs ancienMail, nouveauMail, confirmerMail et mdp.
        """
        ancienMail = self.ancienMail.data
        nouveauMail = self.nouveauMail.data
        confirmerMail = self.confirmerMail.data
        mdp = self.mdp.data
        return (ancienMail, nouveauMail, confirmerMail, mdp)
      
class RechercherForm(FlaskForm):
    value = StringField('value')
    submit = SubmitField('rechercher')

    def get_value(self):
        value = self.value.data
        return value
    
class RechercherFormWithAssets(FlaskForm):
    value = StringField('value')
    domaine = SelectField('domaine', choices=[], id="domaine", name="domaine", validators=[])
    categorie = SelectField('categorie', choices=[], id="categorie", name="categorie", validators=[])
    submit = SubmitField('rechercher')

    def get_value(self):
            """
            Renvoie la valeur actuelle de l'attribut 'value'.
            
            Returns:
                La valeur actuelle de l'attribut 'value'.
            """
            value = self.value.data
            return value

    def get_domaine(self):
        """
        Renvoie le domaine associé à l'objet.
        
        Returns:
            str: Le domaine associé à l'objet.
        """
        domaine = self.domaine.data
        return domaine
    
    def get_categorie(self):
        """
        Renvoie la catégorie sélectionnée.

        Returns:
            str: La catégorie sélectionnée.
        """
        categorie = self.categorie.data
        return categorie

class AjouterUtilisateurForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    choices = [('professeur', 'Professeur'), ('gestionnaire', 'Gestionnaire'), ('laborantin', 'Laborantin')]
    statut = SelectField('ComboBox', choices=choices)
    next = HiddenField()

    def get_full_user(self):
            """
            Récupère les informations complètes de l'utilisateur.

            Returns:
                Tuple[str, str, str, str]: Les informations de l'utilisateur sous forme de tuple.
            """
            nom = self.nom.data
            prenom = self.prenom.data
            email = self.email.data
            statut = self.statut.data
            return (nom, prenom, email, statut)

class AjouterSuggestionForm(FlaskForm):
    domaine = SelectField('ComboBox', choices=[], id="domaine", name="domaine", validators=[DataRequired()])
    categorie = SelectField('Categorie', choices=[], id="categorie", name="categorie", validate_choice=False, validators=[DataRequired()])
    nom = StringField('nom', validators=[DataRequired()])
    reference = StringField('reference', validators=[DataRequired()])
    caracteristiques = TextAreaField('caracteristiques')
    infossup = TextAreaField('infossup')
    seuilalerte  = IntegerField('seuilalerte')
    next = HiddenField()

    def get_full_materiel(self):
            """
            Récupère les informations complètes du matériel.

            Returns:
                tuple: Un tuple contenant les informations suivantes:
                    - categorie (str): La catégorie du matériel.
                    - nom (str): Le nom du matériel.
                    - reference (str): La référence du matériel.
                    - caracteristiques (str): Les caractéristiques du matériel.
                    - infossup (str): Les informations supplémentaires du matériel.
                    - seuilalerte (int): Le seuil d'alerte du matériel.
            """
            categorie = self.categorie.data
            nom = self.nom.data
            reference = self.reference.data
            caracteristiques = self.caracteristiques.data
            infossup = self.infossup.data
            seuilalerte = self.seuilalerte.data
            return (categorie, nom, reference, caracteristiques, infossup, seuilalerte)
    
    def get_full_materiel_requestform(self):
        categorie = request.form['categorie']
        nom = request.form['nom']
        reference = request.form['reference']
        caracteristiques = request.form['caracteristiques']
        infossup = request.form['infossup']
        seuilalerte = request.form['seuilalerte']
        return (categorie, nom, reference, caracteristiques, infossup, seuilalerte)

class CommentaireForm(FlaskForm):
    gestionnaires = SelectField('ComboBox', choices=Bon_commande.Utilisateur.Utilisateur.Get.get_user_with_statut(get_cnx(), "Gestionnaire"))
    text = TextAreaField('text', validators=[DataRequired()])
    submit = SubmitField('envoyer le commentaire')

    def get_text(self):
        """
        Récupère le texte et le gestionnaire associé.

        Returns:
            tuple: Un tuple contenant le texte et le gestionnaire.
        """
        gest = self.gestionnaires.data
        text = self.text.data
        return text, gest
    
class MdpOublierForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('recevoir un nouveau mot de passe')

    def get_email(self):
            """
            Récupère l'email stocké dans l'attribut email.

            Returns:
                str: L'adresse email.
            """
            email = self.email.data
            return email

class AjouterMaterielForm(FlaskForm):
    domaine = SelectField('ComboBox', choices=[], id="domaine", name="domaine", validators=[DataRequired()])
    categorie = SelectField('Categorie', choices=[], id="categorie", name="categorie", validate_choice=False, validators=[DataRequired()])
    nom = StringField('nom', validators=[DataRequired()])
    reference = StringField('reference', validators=[DataRequired()])
    caracteristiques = TextAreaField('caracteristiques')
    infossup = TextAreaField('infossup')
    seuilalerte  = StringField('seuilalerte')
    next = HiddenField()

    def get_full_materiel(self):
            """
            Récupère les informations complètes du matériel.

            Returns:
                tuple: Un tuple contenant les informations suivantes:
                    - categorie (str): La catégorie du matériel.
                    - nom (str): Le nom du matériel.
                    - reference (str): La référence du matériel.
                    - caracteristiques (str): Les caractéristiques du matériel.
                    - infossup (str): Les informations supplémentaires du matériel.
                    - seuilalerte (int): Le seuil d'alerte du matériel.
            """
            categorie = self.categorie.data
            nom = self.nom.data
            reference = self.reference.data
            caracteristiques = self.caracteristiques.data
            infossup = self.infossup.data
            seuilalerte = self.seuilalerte.data
            return (categorie, nom, reference, caracteristiques, infossup, seuilalerte)
    
    def get_full_materiel_requestform(self):
        """
        Récupère les informations complètes du formulaire de demande de matériel.

        Returns:
            tuple: Un tuple contenant les informations suivantes :
                - categorie (str): La catégorie du matériel.
                - nom (str): Le nom du matériel.
                - reference (str): La référence du matériel.
                - caracteristiques (str): Les caractéristiques du matériel.
                - infossup (str): Les informations supplémentaires sur le matériel.
                - seuilalerte (str): Le seuil d'alerte du matériel.
        """
        categorie = request.form['categorie']
        nom = request.form['nom']
        reference = request.form['reference']
        caracteristiques = request.form['caracteristiques']
        infossup = request.form['infossup']
        seuilalerte = request.form['seuilalerte']
        return (categorie, nom, reference, caracteristiques, infossup, seuilalerte)
    
class AjouterStockForm(FlaskForm):
    caracteristiques = TextAreaField('caracteristiques')
    infossup = TextAreaField('infossup')
    seuilalerte  = StringField('seuilalerte')
    materiel = SelectField('ComboBox', choices=[], id="materiel", name="materiel", validators=[DataRequired()])
    endroit = SelectField('ComboBox', choices=[], id="endroit", name="endroit", validators=[DataRequired()])
    position = SelectField('Position', choices=[], id="position", name="position", validate_choice=False, validators=[DataRequired()])
    date_reception = DateField('date_reception', validators=[DataRequired()], default =  datetime.datetime.now().date())
    date_peremption = DateField('date_peremption', validators=[Optional()])
    commentaire = TextAreaField('commentaire', validators=[Optional()])
    quantite_approximative = StringField('quantite_approximative', validators=[DataRequired()])
    quantite_recue = StringField('quantite_recue', validators=[DataRequired()])
    submit = SubmitField("AJOUTER AU STOCK")
    next = HiddenField()

    def get_full_materiel(self):
        """
        Renvoie le domaine et la catégorie du matériel.

        Returns:
            tuple: Un tuple contenant le domaine et la catégorie du matériel.
        """
        categorie = self.categorie.data
        domaine = self.domaine.data
        return (domaine, categorie)
    
    def get_full_materiel_requestform(self):
        """
        Récupère les informations complètes du formulaire de demande de matériel.

        Returns:
            Tuple[str, str, str, str, str, str, str]: Un tuple contenant les informations suivantes:
                - materiel: le matériel demandé
                - idRangement: l'endroit où ranger le matériel
                - date_reception: la date de réception du matériel
                - date_peremption: la date de péremption du matériel
                - commentaire: un commentaire sur la demande de matériel
                - quantite_approximative: la quantité approximative demandée
                - quantite_recue: la quantité réellement reçue
        """
        materiel = request.form['materiel']
        idRangement = request.form['endroit']
        date_reception = request.form['date_reception']
        date_peremption = request.form['date_peremption']
        commentaire = request.form['commentaire']
        quantite_approximative = request.form['quantite_approximative']
        quantite_recue = self.quantite_recue.data
        return (materiel, idRangement, date_reception, date_peremption, commentaire, quantite_approximative, quantite_recue)
    
    def get_materiel(self):
        """
        Returns the data of the materiel.
        """
        return self.materiel.data
    
    def get_endroit(self):
        """
        Returns the value of the 'endroit' data attribute.
        """
        return self.endroit.data


class ImporterCsvForm(FlaskForm):
    
    fichier = FileField('fichier', validators=[])
    submit = SubmitField('IMPORTER')
    next = HiddenField()
    bd_option = RadioField('voulez-vous remplacer les données existantes ?', choices=[('oui','oui'),('non','non')], default='non')

    def get_fichier(self):
        """
        Récupère le fichier associé à l'objet.

        Returns:
            Le fichier associé à l'objet.
        """
        fichier = self.fichier.data
        return fichier
    
    def get_bd_option(self):
        """
        Récupère l'option de base de données associée à l'objet.

        Returns:
            L'option de base de données associée à l'objet.
        """
        bd_option = self.bd_option.data
        return bd_option
    

class ExporterCsvForm(FlaskForm):
    liste_tables = Table.Get.get_AllTable(cnx) 

    # Créer des champs de formulaire pour chaque table
    for table in liste_tables:
        locals()[table] = BooleanField(table, default=False)

    submit = SubmitField('EXPORTER')
    next = HiddenField()

    def get_tables(self):
        """
        Récupère les tables sélectionnées.

        Returns:
            list: Une liste contenant les tables sélectionnées.
        """
        tables = []
        for table in self.liste_tables:
            if getattr(self, table).data is True:
                tables.append(table)
        return tables


@app.route("/csv")
def csv():
    return render_template(
        "csv.html",
        title="CSV",
        chemin = [("base", "accueil"), ("csv", "csv")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/exporter-csv/", methods=("GET","POST",))
def exporter_csv():
    """
    Cette fonction gère l'exportation des données de la base de données dans un fichier CSV.
    Elle affiche un formulaire permettant de sélectionner les tables à exporter, valide le formulaire,
    effectue l'exportation des données dans un fichier CSV et renvoie le fichier CSV à l'utilisateur.
    """
    f = ExporterCsvForm()
    if f.validate_on_submit():
        tables = f.get_tables()
        print(tables)
        ExportCSV.Get.exporter_csv(cnx, tables)
        return send_file("../table/tout.csv", as_attachment=True)
    return render_template(
        "exporterCsv.html",
        title="exporter un fichier csv",
        ExporterCsvForm=f,
        liste_tables = f.liste_tables,
        longueurListe = len(f.liste_tables),    
        chemin = [("base", "accueil"), ("csv", "csv"), ("exporter_csv", "exporter un fichier csv")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )        

@app.route("/importer-csv/", methods=("GET","POST",))
@csrf.exempt
def importer_csv():
    def os_choice(filename):
        if os.name == 'posix':  
            filepath = os.path.join('./temp', filename)
        elif os.name == 'nt':  
            filepath = os.path.join('..\\temp', filename)
        else:
            filepath = os.path.join('./temp', filename)
        return filepath
    
    importerForm = ImporterCsvForm()

    try:
        if importerForm.validate_on_submit():
            fichier = importerForm.fichier.data
            bb_vide = importerForm.bd_option.data
            if fichier:
                filename = secure_filename(fichier.filename)
                
                filepath = os_choice(filename)

                fichier.save(filepath)
                if bb_vide == "oui":
                    ImportCSV.Insert.importer_csv_bd_vide(cnx, filepath)
                elif bb_vide == "non":
                    ImportCSV.Insert.importer_csv_bd_plein(cnx, filepath)
                return redirect(url_for('inventaire'))

    except Exception as e:
        print(f"An error occurred: {e}")

    return render_template(
        "importerCsv.html",
        title="importer un fichier csv",
        ImporterCsvForm=importerForm,
        chemin = [("base", "accueil"), ("csv", "csv"), ("importer_csv", "importer un fichier csv")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/manuel-csv")
def manuel_csv():
    return send_file('../data/module_csv.zip', as_attachment=True)

class AjouterMaterielUniqueForm(FlaskForm):
    endroit = SelectField('ComboBox', choices=[], id="endroit", name="endroit", validators=[DataRequired()])
    position = SelectField('Position', choices=[], id="position", name="position", validate_choice=False, validators=[DataRequired()])
    date_reception = DateField('date_reception', validators=[DataRequired()], default =  datetime.datetime.now().date())
    date_peremption = DateField('date_peremption', validators=[Optional()])
    commentaire = TextAreaField('commentaire')
    quantite_approximative = StringField('quantite_approximative', validators=[DataRequired()])
    quantite_recue = StringField('quantite_recue', validators=[DataRequired()])
    submit = SubmitField("AJOUTER MATERIEL")
    next = HiddenField()

    def get_full_materiel_unique(self):
        """
        Renvoie les informations complètes d'un matériel unique.

        Returns:
            tuple: Un tuple contenant les informations suivantes:
                - position (str): La position du matériel.
                - date_reception (str): La date de réception du matériel.
                - date_peremption (str): La date de péremption du matériel.
                - commentaire (str): Le commentaire associé au matériel.
                - quantite_approximative (int): La quantité approximative du matériel.
                - quantite_recue (int): La quantité reçue du matériel.
        """
        position = self.position.data
        date_reception = self.date_reception.data
        date_peremption = self.date_peremption.data
        commentaire = self.commentaire.data
        quantite_approximative = self.quantite_approximative.data
        quantite_recue = self.quantite_recue.data
        return (position, date_reception, date_peremption, commentaire, quantite_approximative, quantite_recue)
    
    def get_full_materiel_unique_requestform(self):
        """
        Récupère les informations du formulaire de demande de matériel unique.

        Returns:
            Tuple: Un tuple contenant les informations suivantes:
                - position (str): La position du matériel.
                - date_reception (str): La date de réception du matériel.
                - date_peremption (str): La date de péremption du matériel.
                - commentaire (str): Le commentaire associé au matériel.
                - quantite_approximative (str): La quantité approximative du matériel.
                - quantite_recue (str): La quantité reçue du matériel.
        """
        position = request.form['position']     
        date_reception = request.form['date_reception'] 
        date_peremption = request.form['date_peremption']
        commentaire = request.form['commentaire']
        quantite_approximative = request.form['quantite_approximative']
        quantite_recue = request.form['quantite_recue']
        return (position, date_reception, date_peremption, commentaire, quantite_approximative, quantite_recue)

class ModifierMaterielUniqueForm(FlaskForm):
    endroit = SelectField('ComboBox', choices=[], id="endroit", name="endroit", validators=[DataRequired()])
    position = SelectField('Position', choices=[], id="position", name="position", validate_choice=False, validators=[DataRequired()])
    date_reception = DateField('date_reception', validators=[DataRequired()], default =  datetime.datetime.now().date())
    date_peremption = DateField('date_peremption', validators=[Optional()])
    commentaire = TextAreaField('commentaire')
    quantite_approximative = StringField('quantite_approximative', validators=[DataRequired()])
    next = HiddenField()

    def get_full_materiel_unique(self):
        """
        Récupère les informations complètes d'un matériel unique.

        Returns:
            Tuple: Un tuple contenant les informations suivantes:
                - position: La position du matériel
                - date_reception: La date de réception du matériel
                - date_peremption: La date de péremption du matériel
                - commentaire: Le commentaire associé au matériel
                - quantite_approximative: La quantité approximative du matériel
        """
        position = self.position.data
        date_reception = self.date_reception.data
        date_peremption = self.date_peremption.data
        commentaire = self.commentaire.data
        quantite_approximative = self.quantite_approximative.data
        return (position, date_reception, date_peremption, commentaire, quantite_approximative)
    
    def get_full_materiel_unique_requestform(self):
        """
        Récupère les informations complètes du formulaire de demande de matériel unique.

        Returns:
            tuple: Un tuple contenant les informations suivantes :
                - position (str): La position du matériel.
                - date_reception (str): La date de réception du matériel.
                - date_peremption (str): La date de péremption du matériel.
                - commentaire (str): Le commentaire associé au matériel.
                - quantite_approximative (str): La quantité approximative du matériel.
        """
        position = request.form['position']     
        date_reception = request.form['date_reception'] 
        date_peremption = request.form['date_peremption']
        commentaire = request.form['commentaire']
        quantite_approximative = request.form['quantite_approximative']
        return (position, date_reception, date_peremption, commentaire, quantite_approximative)

class FDSForm(FlaskForm):
    comburant = BooleanField('comburant')
    inflammable = BooleanField('inflammable')
    explosif = BooleanField('explosif')
    CMR = BooleanField('CMR')
    chimique = BooleanField('chimique')
    gaz = BooleanField('gaz')
    corrosif = BooleanField('corrosif',)
    environnement = BooleanField('environnement')
    toxique = BooleanField('toxique')
   
    def get_full_fds(self):
        """
        Renvoie les informations complètes sur les FDS.

        :return: Un tuple contenant les informations sur les substances toxiques, inflammables, explosives, les gaz, les CMR, l'environnement, les substances chimiques, les comburants et les substances corrosives.
        :rtype: tuple
        """
        comburant = self.comburant.data
        inflammable = self.inflammable.data
        explosif = self.explosif.data
        CMR = self.CMR.data
        chimique = self.chimique.data
        gaz = self.gaz.data
        corrosif = self.corrosif.data
        environnement = self.environnement.data
        toxique = self.toxique.data
        return toxique, inflammable, explosif, gaz, CMR, environnement, chimique, comburant, corrosif

class EndroitForm(FlaskForm):
    endroit = StringField('endroit', validators=[DataRequired()])
    submit = SubmitField('ajouter un endroit')
    next = HiddenField()

    def get_endroit(self):
            """
            Cette méthode renvoie l'endroit associé à l'objet.
            
            Returns:
                L'endroit associé à l'objet.
            """
            endroit = self.endroit.data
            return endroit
    
class RangementForm(FlaskForm):
    endroit = SelectField('ComboBox', choices=[], id="endroit", name="endroit", validators=[DataRequired()])
    rangement = StringField('rangement', validators=[DataRequired()])
    submit = SubmitField('ajouter un rangement')
    next = HiddenField()

    def get_rangement(self):
        """
        Cette méthode renvoie la valeur du rangement.

        Returns:
            rangement: La valeur du rangement.
        """
        rangement = self.rangement.data
        return rangement
    
    def get_full_rangement(self):
        """
        Récupère les informations d'endroit et de rangement à partir du formulaire.

        Returns:
            Tuple[str, str]: Un tuple contenant les informations d'endroit et de rangement.
        """
        endroit = request.form['endroit']
        rangement = request.form['rangement']
        return (endroit, rangement)

def get_domaine_choices():
    """
    Récupère les choix de domaine à partir de la base de données.

    :return: Une liste de tuples contenant les choix de domaine.
    """
    query = text("SELECT nomDomaine, idDomaine FROM DOMAINE;")
    result = cnx.execute(query)
    domaines =  [(str(id_), name) for name, id_ in result]
    domaines.insert(0, ("", "Choisir un domaine"))
    return domaines

@app.route('/get_categorie_choices/', methods=['GET'])
def get_categorie_choices():
    """
    Récupère les choix de catégories en fonction de l'identifiant de domaine sélectionné.

    Returns:
        jsonify: Les catégories sous forme de JSON.
    """
    selected_domain_id = request.args.get('domaine_id')
    result = cnx.execute(text("SELECT nomCategorie, idCategorie FROM CATEGORIE WHERE idDomaine = " + str(selected_domain_id)))
    categories = {str(id_): name for name, id_ in result}
    return jsonify(categories)


def get_categorie_choices_modifier_materiel(idDomaine):
    """
    Récupère les choix de catégorie pour la modification du matériel.

    Args:
        idDomaine (int): L'identifiant du domaine.

    Returns:
        list: Une liste de tuples contenant les noms et les identifiants des catégories.
    """
    query = text("SELECT nomCategorie, idCategorie FROM CATEGORIE WHERE idDomaine =" + str(idDomaine) )
    result = cnx.execute(query)
    categories = [(str(id_), name) for name, id_ in result]
    return categories

@app.route("/ajouter-suggestion/", methods=("GET","POST",))
def ajouter_suggestion():
    """
    Cette fonction gère l'ajout d'une suggestion dans le système.
    Elle affiche un formulaire pour saisir les informations nécessaires,
    valide le formulaire et effectue les opérations d'insertion dans la base de données.
    En cas d'erreur, elle affiche un message d'erreur approprié.
    """
    FDSFormulaire = FDSForm()
    f = AjouterSuggestionForm()
    f.domaine.choices = get_domaine_choices() 
    if f.validate_on_submit() :
        try:
            categorie, nom, reference, caracteristiques, infossup, seuilalerte = f.get_full_materiel()
            res = Materiel.Insert.insere_materiel(cnx, categorie, nom, reference, caracteristiques, infossup, seuilalerte)
            print("FDS : " + str(FDSFormulaire.get_full_fds()))
            toxique, inflammable, explosif, gaz, CMR, environnement, chimique, comburant, corrosif = FDSFormulaire.get_full_fds()
            idMat = Materiel.Get.get_idMateriel_with_nomMateriel(cnx, nom)
            
            FDS.Insert.ajout_FDS(cnx, nom)
            idFDS = FDS.Get.get_idFDS_with_nomFDS(cnx, nom)
            FDS.Update.update_FDS(cnx, idFDS, idMat)
            
            Risques.Insert.ajout_risque_with_idMateriel(cnx, idMat, toxique, inflammable, explosif, gaz, CMR, environnement, chimique, comburant, corrosif)
            if res:
                return redirect(url_for('demander'))
            else:
                print("Erreur lors de l'insertion du matériel")
                return redirect(url_for('ajouter_suggestion'))
        except Exception as e:
            print(e)
            return render_template(
                "ajouterSuggestion.html",
                title="ajouter une suggestion",
                FDSForm=FDSFormulaire,
                AjouterSuggestionForm=f,
                erreur="Le nom du materiel ou la reference est deja existante",
                chemin = [("base", "accueil"), ("ajouter_suggestion", "ajouter une suggestion")],
                alerte_tl = Alert.get_nb_alert(cnx),
                demande_tl = Demande.Get.get_nb_demande(cnx)
            )
    else :
        print("Erreur lors de la validation du formulaire")
        print(f.errors)
    return render_template(
        "ajouterSuggestion.html",
        title="ajouter une suggestion",
        FDSForm=FDSFormulaire,
        AjouterSuggestionForm=f,
        chemin = [("base", "accueil"), ("demander","demander"), ("ajouter_suggestion", "ajouter une suggestion")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/ajouter-endroit", methods=("GET","POST",))
def ajouter_endroit():
    """
    Fonction qui permet d'ajouter un endroit dans le système.

    Returns:
        - Si la validation du formulaire est réussie et l'insertion de l'endroit est effectuée avec succès,
          la fonction redirige vers la page 'inventaire'.
        - Si la validation du formulaire échoue, la fonction rend le template 'ajouterEndroit.html' avec le formulaire,
          le titre et le chemin de navigation.
    """
    f = EndroitForm()
    if f.validate_on_submit() :
        endroit = f.get_endroit()
        res = Endroit.Insert.insere_endroit(get_cnx(), endroit)
        print(endroit)

        if res:
            return redirect(url_for('inventaire'))
        else:
            print("Erreur lors de l'insertion de l'endroit")
            return redirect(url_for('ajouter_endroit'))
    else :
        return render_template(
        "ajouterEndroit.html",
        title="ajouter un endroit",
        AjouterEndroitForm=f,
        chemin = [("base", "accueil"),("inventaire", "inventaire"),("ajouter_endroit", "ajouter un endroit")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/ajouter-rangement", methods=("GET","POST",))
def ajouter_rangement():
    """
    Cette fonction gère l'ajout d'un rangement dans le système.
    Elle affiche un formulaire pour saisir les informations du rangement,
    valide les données saisies, insère le rangement dans la base de données
    et redirige l'utilisateur vers la page d'inventaire en cas de succès.
    En cas d'échec, elle affiche un message d'erreur et redirige l'utilisateur
    vers la page d'ajout de rangement.
    """
    f = RangementForm()
    f.endroit.choices = get_endroit_choices() 

    if f.validate_on_submit():
        endroit, rangement = f.get_full_rangement()
        
        res = Rangement.Insert.insere_rangement(get_cnx(), endroit, rangement)
        
        if res:
            return redirect(url_for('inventaire'))
        else:
            print("Erreur lors de l'insertion du rangement")
            return redirect(url_for('ajouter_rangement'))
    else :
        return render_template(
        "ajouterRangement.html",
        title="ajouter un rangement",
        AjouterRangementForm=f,
        chemin = [("base", "accueil"),("inventaire", "inventaire"),("ajouter_rangement", "ajouter un rangement")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )


@app.route("/supprimer-suggestion/<int:id>", methods=("GET","POST",))
def supprimer_suggestion(id):
    """
    Supprime une suggestion en fonction de son identifiant.

    Args:
        id (int): L'identifiant de la suggestion à supprimer.

    Returns:
        redirect: Une redirection vers la page 'demander'.
    """
    print("id supprimé : ",id)
    Risques.Delete.delete_risque_with_idMateriel(get_cnx(),id)
    Materiel.Delete.delete_materiel(get_cnx(),id)   

    return redirect(url_for('demander'))

def intersection(lst1, lst2): 
    return [item for item in lst1 if item not in lst2]

@app.route("/ajouter-stock/", methods=("GET","POST",))
@csrf.exempt
def ajouter_stock():
    """
    Fonction qui gère l'ajout de matériel au stock.

    Cette fonction affiche un formulaire permettant de rechercher et filtrer les matériels existants,
    puis d'ajouter un matériel au stock en spécifiant différentes informations telles que l'endroit de stockage,
    la date de réception, la date de péremption, le commentaire, la quantité approximative et la quantité reçue.

    Returns:
        - Si le formulaire est valide et l'ajout est effectué avec succès, la fonction redirige vers la vue 'etat' du matériel ajouté.
        - Sinon, la fonction affiche les erreurs de validation du formulaire et rend le template 'ajouterStock.html'.
    """
    rechercherForm = RechercherFormWithAssets()
    rechercherForm.domaine.choices = get_domaine_choices() 

    search = rechercherForm.get_value()
    domaine = rechercherForm.get_domaine()
    categorie = rechercherForm.get_categorie()

    ajouterForm = AjouterStockForm()
    ajouterForm.endroit.choices = get_endroit_choices()

    items = get_materiels_existants() # Valeur par-défaut (tout tout tout les matériels)

    # filtre à la valeur de la recherche    
    if search != None: items = get_materiels_existants_with_search(search)

    # Filtre du domaine
    if domaine != "" and domaine != None:
        domaines_list = list()
        for (idM,name) in items:
            domaine_id = str(Materiel.Get.get_all_information_to_Materiel_with_id(get_cnx(),idM)[4])
            if domaine_id != domaine: domaines_list.append((idM,name))

    # Filtre de la catégorie
    if categorie != None:
        categories_list = list()
        for (idM,name) in items:
            categorie_id = str(Materiel.Get.get_all_information_to_Materiel_with_id(get_cnx(),idM)[2])
            if categorie_id != categorie: categories_list.append((idM,name))

    # Intersection de tous les tris possibles
    if domaine != "" and domaine != None:
        items = intersection(items, domaines_list)
    if categorie != None:
        items = intersection(items, categories_list)

    # Actualisation final des choix de matériels en fonction de tous les inputs
    ajouterForm.materiel.choices = items

    # /!\ L'ajout dans l'inventaire ne se fait pas correctement, code à reprendre en priorité V
    if ajouterForm.validate_on_submit():
        materiel, idRangement, date_reception, date_peremption, commentaire, quantite_approximative, quantite_recue = ajouterForm.get_full_materiel_requestform()
        
        if STOCKLABORATOIRE.Get.materiel_dans_stock(get_cnx(), materiel) <= 0 :
            STOCKLABORATOIRE.Insert.insere_materiel_stock(get_cnx(), materiel)
        
        for _ in range(int(quantite_recue)): # On insère autant de fois que la quantité est exigée
            nouvel_id = MaterielUnique.Insert.insere_materiel_unique(cnx, materiel, idRangement, date_reception, date_peremption, commentaire, quantite_approximative)
            if nouvel_id > 0 :
                    res = ReserveLaboratoire.Insert.insere_materiel_unique_reserve(cnx, nouvel_id)
                    if res == False :
                        print("Erreur lors de l'insertion du matériel unique d'id " + str(nouvel_id))
                        return redirect(url_for('ajouter_materiel'))
            # ^ Probablement incorrect, quand on ajoute, on est effectivement redirigier vers la vue Etat mais elle n'aparaît pas dans l'inventaire
        RELOAD.reload_alert(cnx)
        return redirect(url_for('etat', id=materiel))
    else:
        print("Erreur lors de la validation du formulaire")
        print(ajouterForm.errors)

    return render_template(
        "ajouterStock.html",
        title="ajouter au stock",
        AjouterStockForm=ajouterForm,
        RechercherFormWithAssets=rechercherForm,
        chemin = [("base", "accueil"), ("ajouter_stock", "ajouter au stock")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )


def get_endroit_choices():
    """
    Récupère les choix d'endroits de rangement depuis la base de données.

    Returns:
        list: Une liste de tuples contenant les choix d'endroits de rangement.
              Chaque tuple contient l'identifiant de l'endroit et son nom.
    """
    query = text("SELECT endroit, idEndroit FROM ENDROIT;")
    result = cnx.execute(query)
    endroits =  [(str(id_), name) for name, id_ in result]
    endroits.insert(0, ("", "Choisir un endroit de rangement"))
    return endroits

@app.route('/get_position_choices/', methods=['GET'])
def get_position_choices():
    """
    Retrieves the position choices based on the selected endroit_id.

    Returns:
        A JSON response containing the positions and their corresponding idRangement.
    """
    selected_endroit_id = request.args.get('endroit_id')
    result = cnx.execute(text("SELECT position, idRangement FROM RANGEMENT WHERE idEndroit = " + str(selected_endroit_id)))
    positions = {str(id_): name for name, id_ in result}
    return jsonify(positions)

def get_position_choices_modifier_materiel(idEndroit):
    """
    Récupère les choix de position pour la modification du matériel.

    Args:
        idEndroit (int): L'identifiant de l'endroit.

    Returns:
        list: Une liste de tuples contenant les positions et les identifiants de rangement.
    """
    query = text("SELECT position, idRangement FROM RANGEMENT WHERE idEndroit = " + str(idEndroit))
    result = cnx.execute(query)
    positions = [(str(id_), name) for name, id_ in result]
    return positions

def get_materiels_existants():
    """
    Récupère les matériels existants dans la base de données.

    Returns:
        Une liste de tuples contenant le nom et l'identifiant de chaque matériel.
    """
    query = text("SELECT nomMateriel, idMateriel FROM MATERIEL;")
    result = cnx.execute(query)
    materiels = [(str(id_), name) for name, id_ in result]
    return materiels

def get_materiels_existants_with_search(search):
    """
    Récupère les matériels existants correspondant à une recherche donnée.

    Args:
        search (str): La chaîne de recherche.

    Returns:
        list: Une liste de tuples contenant l'identifiant et le nom des matériels correspondants.
    """
    query = text("SELECT nomMateriel, idMateriel FROM MATERIEL where nomMateriel like'%" + search + "%';")
    result = cnx.execute(query)
    materiels = [(str(id_), name) for name, id_ in result]
    return materiels

@app.route("/ajouter-materiel-unique/<int:id>", methods=("GET","POST",))
def ajouter_materiel_unique(id):
    """
    Ajoute un matériel unique au stock du laboratoire.

    Args:
        id (int): L'identifiant du matériel.

    Returns:
        flask.Response: Redirige vers la page d'état du matériel.

    Raises:
        None
    """
    f = AjouterMaterielUniqueForm()
    f.endroit.choices = get_endroit_choices() 

    if f.validate_on_submit():
        position, date_reception, date_peremption, commentaire, quantite_approximative, quantite_recue = f.get_full_materiel_unique_requestform()
        identifiant = Materiel.Get.get_all_information_to_Materiel_with_id(get_cnx(), id)[0]

        if STOCKLABORATOIRE.Get.materiel_dans_stock(get_cnx(), identifiant) <= 0:
            STOCKLABORATOIRE.Insert.insere_materiel_stock(get_cnx(), identifiant)

        liste_res = []

        for _ in range(int(quantite_recue)): # On insère autant de fois que la quantité est exigée
            print("----------------------------------------")
            new_id = MaterielUnique.Insert.insere_materiel_unique(cnx, identifiant, position, date_reception, date_peremption, commentaire, quantite_approximative)
            print("new_id : ",new_id)
            if new_id > 0 :
                res = ReserveLaboratoire.Insert.insere_materiel_unique_reserve(cnx, new_id) # Erreur ici
                if res == False or res == None:
                    print("Erreur lors de l'insertion du matériel unique d'id " + str(new_id))
                    return redirect(url_for('etat', id=id))
        
        return redirect(url_for('etat', id=id))
        
    else :
        print("Erreur lors de la validation du formulaire")
        print(f.errors)
    return render_template(
        "ajouterMaterielUnique.html",
        title="ajouter un matériel au stock",
        AjouterMaterielUniqueForm=f,
        id = id,
        materiel = Materiel.Get.get_all_information_to_Materiel_with_id(get_cnx(), id)[1],
        chemin = [("base", "accueil"),("inventaire", "inventaire")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

class A2FForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('valider')

    def get_code(self):
        code = self.code.data
        return code

@app.route("/")
def base():
    """
    Fonction qui renvoie le rendu du template "home.html" avec les informations suivantes :
    - Le nombre d'alertes récupéré à partir de la méthode get_nb_alert de la classe Alert
    - Le nombre de demandes récupéré à partir de la méthode get_nb_demande de la classe Demande
    - Le titre de la page est défini comme "GESTLAB"
    """
    nb_alertes = Alert.get_nb_alert(cnx)
    nb_demandes = Demande.Get.get_nb_demande(cnx)
    return render_template(
        "home.html",
        alertes=str(nb_alertes),
        demandes=str(nb_demandes),
        title="GESTLAB",
        chemin = [("base", "accueil")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/motdepasseoublie/", methods=("GET","POST",))
def mot_de_passe_oublier():
    """
    Fonction qui gère la demande de réinitialisation du mot de passe.
    Si le formulaire est valide, l'adresse e-mail est récupérée et la redirection est effectuée vers la page a2f avec l'e-mail et l'ID.
    Sinon, le formulaire est renvoyé à la page de connexion.
    """
    f = MdpOublierForm()
    if f.validate_on_submit():
        email = f.get_email()
        return redirect(url_for('a2f', mail=email, id=1))
    return render_template(
        "login.html",
        MdpOublierForm=f,
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/a2f/<string:mail>/<int:id>", methods=("GET","POST",))
def a2f(mail, id):
    """
    Fonction qui gère l'authentification à deux facteurs (A2F).
    
    Args:
        mail (str): L'adresse e-mail de l'utilisateur.
        id (int): L'identifiant de l'action à effectuer (1: récupération de mot de passe, 2: changement de mot de passe, 3: changement d'adresse e-mail).
    
    Returns:
        render_template: Le template HTML correspondant à la page A2F.
    """
    oldMdp = request.args.get('oldMdp')
    newMdp = request.args.get('newMdp')
    newMail = request.args.get('newMail')
    oldMail = request.args.get('oldMail')
    mdp = request.args.get('mdp')
    print(oldMdp)
    print(newMdp)
    print(newMail)
    print(oldMail)
    print(mdp)
    f = A2FForm()
    if f.validate_on_submit():
        code = f.get_code()
        uri = Bon_commande.Utilisateur.Utilisateur.Get.get_uri_with_email(cnx, mail)
        if Authentification.Authentification.verify(uri, code):
            if id == 1:
                Mots_de_passe.recuperation_de_mot_de_passe(cnx, mail)
                print("code valide")
                return redirect(url_for('login'))
            if id == 2:
                res = Bon_commande.Utilisateur.Utilisateur.Update.update_mdp_utilisateur(cnx, session['utilisateur'][2], oldMdp, newMdp)
                if res:
                    session.pop('utilisateur', None)
                    return redirect(url_for('login'))
                else:
                    print("erreur de changement de mdp")
                    return redirect(url_for('login'))
            if id == 3:
                res = Bon_commande.Utilisateur.Utilisateur.Update.update_email_utilisateur(cnx, newMail, session['utilisateur'][0], mdp, oldMail)
                print(newMail, session['utilisateur'][0], mdp)
                if res:
                    session.pop('utilisateur', None)
                    return redirect(url_for('login'))
                else:
                    print("erreur de changement de mail")
                    return redirect(url_for('login'))
    return render_template(
        "a2f.html",
        title="A2F - "+mail,
        mail=mail,
        id=id,
        oldMdp=oldMdp,
        newMdp=newMdp,
        newMail=newMail,
        oldMail=oldMail,
        mdp=mdp,
        A2FForm=f,
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/reinitialiser-bon-commande/<int:id>", methods=("GET","POST",))
def reinitialiser_bon_commande(id):
    """
    Réinitialise le bon de commande en supprimant tous les matériels associés.

    Args:
        id (int): L'identifiant du bon de commande.

    Returns:
        redirect: Une redirection vers la page 'commander'.
    """
    Materiel.Delete.delete_all_materiel_in_commande(cnx, id)
    return redirect(url_for('commander'))

@app.route("/reinitialiser-demande/<int:id>", methods=("GET","POST",))
def reinitialiser_demande(id):
    """
    Réinitialise la demande en supprimant tous les matériels ajoutés à la demande spécifiée.

    Args:
        id (int): L'identifiant de la demande à réinitialiser.

    Returns:
        redirect: Une redirection vers la page 'demander'.
    """
    Materiel.Delete.delete_all_materiel_in_AjouterMateriel(cnx, id)
    return redirect(url_for('demander'))

@app.route("/commander-materiel-unique/<int:id>", methods=("GET","POST",))
def commander_materiel_unique(id):
    """
    Ajoute un matériel unique à une commande.

    Args:
        id (int): L'identifiant de la commande.

    Returns:
        redirect: Redirige vers la page 'commander'.
    """
    idDemande = request.args.get('idDemande')
    idMat = request.args.get('idMat')
    qte = request.args.get('qte')
    Materiel.Insert.ajout_materiel_in_commande(cnx, idMat, id, qte, False)
    return redirect(url_for('commander'))

@app.route("/commander-demande-materiel-unique/<int:id>", methods=("GET","POST",))
def commander_demande_materiel_unique(id):
    """
    Commande un matériel unique pour une demande spécifique.

    Args:
        id (int): L'identifiant de la demande.

    Returns:
        redirect: Redirige vers la page 'commander'.
    """
    idDemande = request.args.get('idDemande')
    idMat = request.args.get('idMat')
    qte = request.args.get('qte')
    Materiel.Insert.ajout_materiel_in_commande(cnx, idMat, id, qte, True)
    MaterielUnique.Delete.delete_materiel_unique_in_demande(cnx, idDemande, idMat)
    return redirect(url_for('commander'))

@app.route("/tout-commander-materiel-unique/<int:idDemande>", methods=("GET","POST",))
def tout_commander_materiel_unique(idDemande):
    """
    Commande tout le matériel unique pour une demande spécifique.

    Args:
        idDemande (int): L'identifiant de la demande.

    Returns:
        redirect: Redirige vers la page 'commander'.
    """
    idUser = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    Demande.Update.tout_commander_with_idDemmande_and_idUt(cnx, idDemande, idUser)
    return redirect(url_for('commander'))


@app.route("/demander-materiel-unique/<int:id>", methods=("GET","POST",))
def demander_materiel_unique(id):
    """
    Demande un matériel unique pour une demande spécifique.

    Args:
        id (int): L'identifiant de la demande.

    Returns:
        redirect: Redirige vers la page 'demander'.
    """
    idDemande = request.args.get('idDemande')
    idMat = request.args.get('idMat')
    qte = request.args.get('qte')
    Materiel.Insert.ajout_materiel_in_AjouterMateriel(cnx, idMat, id, qte, False)
    return redirect(url_for('demander'))

#Pour le bouton commander tout les materiels 

# @app.route("/commander-all-materiel-unique/<int:id>", methods=("GET","POST",))
# def commander_all_materiel_unique(id):
#     idMat = request.args.get('idMat')
#     qte = request.args.get('qte')
#     ajout_materiel_in_commande(cnx, idMat, id, qte, False)
#     set_all_quantite_from_ajouterMat_to_boncommande(cnx, idemande, id)  #---------------------------------------------------LEO-----AIDE--------------------------------------#  
#     return redirect(url_for('commander'))

@app.route("/commander/")
@csrf.exempt
def commander():
    """
    Fonction qui affiche la page de commande de matériel.

    Returns:
        render_template: Le template HTML de la page commander.html avec les données nécessaires.
    """
    rechercher = RechercherForm()
    nb_alertes = Alert.get_nb_alert(cnx)
    nb_demandes = Demande.Get.get_nb_demande(cnx)
    idUser = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    idbc = Bon_commande.Bon_commande.Get.get_id_bonCommande_actuel(cnx, idUser)
    liste_materiel = Bon_commande.Bon_commande.Get.afficher_bon_commande(cnx, idUser)
    nbMateriel = len(liste_materiel)
    print(liste_materiel)
    return render_template(
        "commander.html",
        title="commander du matériel",
        categories = Domaine.Domaine.get_domaine(get_cnx()),
        alertes=str(nb_alertes),
        demandes=str(nb_demandes),
        idUser = idUser,
        idbc = idbc,
        liste_materiel = liste_materiel,
        nbMateriel = nbMateriel,
        RechercherForm=rechercher,
        chemin = [("base", "accueil"), ("commander", "commander")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/recherche-materiel-demander", methods=("GET","POST",))
@csrf.exempt
def recherche_materiel_demander():
    """
    Fonction qui effectue une recherche de matériel demandé.

    Returns:
        - Si une valeur de recherche est spécifiée, renvoie la page "demander.html" avec les résultats de la recherche.
        - Sinon, redirige vers la page "demander.html".
    """
    rechercher = RechercherForm()
    idUser = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    idDemande = Demande.Get.get_id_demande_actuel(cnx, idUser)
    value = rechercher.get_value()
    print("value : "+value)
    if value != None:
        liste_materiel = Recherche.recherche_all_in_materiel_demande_with_search(get_cnx(), idDemande, value)
        return render_template(
            "demander.html",
            title="demander",
            idUser = idUser,
            idDemande = Demande.Get.get_id_demande_actuel(cnx, Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])),
            categories = Domaine.Domaine.get_domaine(get_cnx()),
            RechercherForm=rechercher,
            liste_materiel = liste_materiel,
            nbMateriel = len(liste_materiel),
            alertes = Alert.get_nb_alert(cnx),
            demandes = Demande.Get.get_nb_demande(cnx),
            chemin = [("base", "accueil"), ("demander", "demander")],
            alerte_tl = Alert.get_nb_alert(cnx),
            demande_tl = Demande.Get.get_nb_demande(cnx)
        )
    return redirect(url_for('demander'))

@app.route("/recherche-materiel", methods=("GET","POST",))
@csrf.exempt
def recherche_materiel():
    """
    Cette fonction gère la recherche de matériel.
    Elle récupère les informations de recherche, effectue la recherche dans la base de données,
    et renvoie les résultats à la page commander.html.
    Si aucune valeur de recherche n'est fournie, la fonction redirige vers la page commander.
    """
    rechercher = RechercherForm()
    idUser = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    idbc = Bon_commande.Bon_commande.Get.get_id_bonCommande_actuel(cnx, idUser)
    value = rechercher.get_value()
    print("value : "+value)
    if value != None:
        liste_materiel = Recherche.recherche_all_in_materiel_with_search(get_cnx(), idbc, value)
        return render_template(
            "commander.html",
            title="commander",
            idUser = idUser,
            idbc = Bon_commande.Bon_commande.Get.get_id_bonCommande_actuel(cnx, Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])),
            categories = Domaine.Domaine.get_domaine(get_cnx()),
            RechercherForm=rechercher,
            liste_materiel = liste_materiel,
            nbMateriel = len(liste_materiel),
            alertes = Alert.get_nb_alert(cnx),
            demandes = Demande.Get.get_nb_demande(cnx),
            chemin = [("base", "accueil"), ("commander", "commander")],
            alerte_tl = Alert.get_nb_alert(cnx),
            demande_tl = Demande.Get.get_nb_demande(cnx)
        )
    return redirect(url_for('commander'))

@app.route("/bon-commande/<int:id>")
def bon_commande(id):
    """
    Affiche le bon de commande avec les détails correspondants.

    Args:
        id (int): L'identifiant du bon de commande.

    Returns:
        render_template: Le template HTML pour afficher le bon de commande.
    """
    idUser = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    liste_materiel = Materiel.Get.get_materiel_commande(cnx, id)
    return render_template(
        "bonDeCommande.html",
        id = id,
        idUser = idUser,
        categories = Domaine.Domaine.get_domaine(get_cnx()),
        title = "bon de commande",
        liste_materiel = liste_materiel,
        longueur = len(liste_materiel),
        chemin = [("base", "accueil"), ("commander", "commander"), ('demandes', 'bon de commande')],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/bon-demande/<int:id>")
def bon_demande(id):
    """
    Affiche le bon de demande avec les détails de la demande.

    Args:
        id (int): L'identifiant de la demande.

    Returns:
        render_template: Le template HTML "bonDemande.html" avec les données nécessaires pour afficher le bon de demande.
    """
    idUser = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    liste_materiel = Materiel.Get.get_materiel_demande(cnx, id)
    return render_template(
        "bonDemande.html",
        id = id,
        idUser = idUser,
        categories = Domaine.Domaine.get_domaine(get_cnx()),
        title = "bon de demande",
        liste_materiel = liste_materiel,
        longueur = len(liste_materiel),
        chemin = [("base", "accueil"), ("demander", "demander"), ("demander","bon de demande")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/consulterBonCommande/")
def consulter_bon_commande():
    """
    Cette fonction permet de consulter les bons de commande.
    Elle récupère les informations des bons de commande depuis la base de données,
    puis les affiche dans un template HTML avec les informations des utilisateurs associés
    et les états des bons de commande.
    """
    info_bon_commande = Bon_commande.Bon_commande.Get.consulter_bon_commande_without_table(cnx)
    print(info_bon_commande)
    liste_info_user = []
    liste_etat_bon_commande = []
    nb_bon_commande_attente = 0
    for info in info_bon_commande:
        if info[1] == 2:
            nb_bon_commande_attente += 1
        liste_etat_bon_commande.append(Commande.Commande.Get.get_statut_from_commande_with_id_etat(cnx, info[1]))
        info_user = Bon_commande.Utilisateur.Utilisateur.Get.get_all_information_utilisateur_with_id(get_cnx(), info[2])
        liste_info_user.append(info_user)
    return render_template(
        "consulterBonCommande.html",
        title="consultation des bon de commande",
        len = len(info_bon_commande),
        nb_bon_commande_attente = nb_bon_commande_attente,
        bonCommande = info_bon_commande,
        infoUser = liste_info_user,
        listeEtat = liste_etat_bon_commande,
        statutsCommande = Commande.Commande.Get.get_statut_from_commande(cnx),
        chemin = [("base", "accueil"), ('consulter_bon_commande', 'consulter bon de commande')],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/changer-statut-bon-commande", methods=("GET","POST",))
def changer_statut_bon_commande():
    """
    Change le statut d'un bon de commande en fonction des paramètres passés dans la requête.
    
    :return: Redirige vers la page de consultation du bon de commande.
    """
    idbc = request.args.get('idbc')
    idStatut = request.args.get('statut')
    Bon_commande.Bon_commande.Update.changer_etat_bonCommande_with_id(cnx, idbc, idStatut)
    return redirect(url_for('consulter_bon_commande'))

@app.route("/delete-materiel/<int:idbc>/<int:idMat>", methods=("GET","POST",))
def delete_materiel(idbc, idMat):
    """
    Supprime un matériel d'une commande en utilisant son identifiant de commande et son identifiant de matériel.

    Args:
        idbc (int): L'identifiant de la commande.
        idMat (int): L'identifiant du matériel.

    Returns:
        redirect: Redirige vers la page de la commande après la suppression du matériel.
    """
    Materiel.Delete.delete_materiel_in_BonCommande_whith_id(cnx, idMat, idbc)
    return redirect(url_for('bon_commande', id=idbc))

@app.route("/delete-materiel-demande/<int:idDemande>/<int:idMat>", methods=("GET","POST",))
def delete_materiel_demande(idDemande, idMat):
    """
    Supprime un matériel d'une demande spécifique.

    Args:
        idDemande (int): L'identifiant de la demande.
        idMat (int): L'identifiant du matériel à supprimer.

    Returns:
        redirect: Redirige vers la page 'bon_demande' avec l'identifiant de la demande.
    """
    Materiel.Delete.delete_materiel_in_AjouterMateriel_whith_id(cnx, idMat, idDemande)
    return redirect(url_for('bon_demande', id=idDemande))

@app.route("/delete-materiel-demandes/<int:idDemande>/<int:idMat>", methods=("GET","POST",))
def delete_materiel_demandes(idDemande, idMat):
    """
    Supprime un matériel d'une demande spécifique.

    Args:
        idDemande (int): L'identifiant de la demande.
        idMat (int): L'identifiant du matériel à supprimer.

    Returns:
        redirect: Redirige vers la page de base si la suppression est réussie, sinon redirige vers la page de la demande spécifique.
    """
    res = Materiel.Delete.delete_materiel_in_AjouterMateriel_whith_id(cnx, idMat, idDemande)
    if res:
        return redirect(url_for('base'))
    return redirect(url_for('demande', idDemande=idDemande))

@app.route("/bon-commande-unique", methods=("GET","POST",))
def bon_commande_unique():
    """
    Affiche les détails d'un bon de commande unique.

    :return: Le template "bonCommandeUnique.html" avec les détails du bon de commande.
    """
    idbc = request.args.get('idbc')
    liste_materiel = Bon_commande.Bon_commande.Get.get_bon_commande_with_id(cnx, idbc)
    return render_template(
        "bonCommandeUnique.html",
        liste_materiel = liste_materiel,
        title="bon de commande n°"+str(idbc),
        idbc = idbc,
        chemin = [("base", "accueil"), ("consulter_bon_commande", "consulter bon de commande"), ("bon_commande_unique", "bon de commande")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/historique-bon-commande")
def historique_bon_commande():
    """
    Cette fonction renvoie l'historique des bons de commande.

    Returns:
        render_template: Le template "historiqueBonCommande.html" avec les données nécessaires.
    """
    info_bon_commande = Bon_commande.Bon_commande.Get.get_bon_commande_with_statut(cnx, 4)
    liste_info_user = []
    liste_etat_bon_commande = []
    for info in info_bon_commande:
        liste_etat_bon_commande.append(Commande.Commande.Get.get_statut_from_commande_with_id_etat(cnx, info[1]))
        info_user = Bon_commande.Utilisateur.Utilisateur.Get.get_all_information_utilisateur_with_id(get_cnx(), info[2])
        liste_info_user.append(info_user)
    return render_template(
        "historiqueBonCommande.html",
        title="historique des bon de commande",
        len = len(info_bon_commande),
        bonCommande = info_bon_commande,
        infoUser = liste_info_user,
        listeetat = liste_etat_bon_commande,
        statutsCommande = Commande.Commande.Get.get_statut_from_commande(cnx),
        # chemin = [("base", "accueil"), ("consulter_bon_commande, consulter bon commande"), ("historique_bon_commande", "historique des bon de commande")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/delete-bon-commande/<int:id>", methods=("GET","POST",))
def delete_bon_commande(id):
    """
    Supprime un bon de commande avec l'ID spécifié.

    Args:
        id (int): L'ID du bon de commande à supprimer.

    Returns:
        redirect: Une redirection vers la page de consultation des bons de commande.
    """
    Bon_commande.Bon_commande.Delete.delete_bonCommande_with_id(cnx, id)
    return redirect(url_for('consulter_bon_commande'))

@app.route("/valider-bon-demande/<int:id>", methods=("GET","POST",))
def valider_bon_demande(id):
    """
    Valide le bon de demande avec l'identifiant spécifié.

    Args:
        id (int): L'identifiant du bon de demande à valider.

    Returns:
        None
    """
    idDemande = request.args.get('idDemande')
    Demande.Insert.changer_etat_demande(cnx, id)
    while True:
        pass
    return redirect(url_for('base'))

@app.route("/update-theme/<int:id>", methods=("GET","POST",))
def update_theme(id):
    try:
        Utilisateur.Update.update_theme_utilisateur(cnx, session['utilisateur'][4], id)
        return redirect(url_for('base'))
    except Exception as e:
        print("An error occurred:", e)
        return redirect(url_for('base'))




@app.route("/valider-bon-commande/<int:id>", methods=("GET","POST",))
def valider_bon_commande(id):
    """
    Valide un bon de commande en changeant son état et génère un PDF du bon de commande.

    Args:
        id (int): L'identifiant du bon de commande à valider.

    Returns:
        None
    """
    idCommande = request.args.get('idCommande')
    liste_materiel = Materiel.Get.get_all_materiel_for_pdf_in_bon_commande(cnx, id)
    print(liste_materiel)
    Bon_commande.Bon_commande.Update.changer_etat_bonCommande(cnx, id)
    PDF_BonCommande.genererpdfBonCommande(session['utilisateur'][0], session['utilisateur'][3], liste_materiel, str(idCommande))
    while True:
        pass  # Cette boucle ne se termine jamais  
    return redirect(url_for('base'))

@app.route("/valider-bon-commande-pdf/<int:id>", methods=("GET","POST",))
def valider_bon_commande_pdf(id):
    """
    Génère un bon de commande au format PDF et renvoie le fichier en tant que téléchargement.

    Args:
        id (int): L'identifiant du bon de commande.

    Returns:
        flask.Response: Le fichier PDF du bon de commande en tant que téléchargement.
    """
    liste_materiel = Materiel.Get.get_all_materiel_for_pdf_in_bon_commande_after(cnx, id)
    PDF_BonCommande.genererpdfBonCommande(session['utilisateur'][0], session['utilisateur'][3], liste_materiel, str(id))
    return send_file("static/data/bonCommande.pdf", as_attachment=True)

@app.route("/fusion-bon-commande")
def fusion_bon_commande():
    """
    Fusionne les bons de commande avec le statut de fusion 2.
    
    Récupère la liste des bons de commande avec le statut de fusion 2.
    Affiche la liste des bons de commande.
    Effectue la fusion des bons de commande.
    Redirige vers la page de consultation des bons de commande.
    """
    liste_bon_commande = Bon_commande.Bon_commande.Get.get_bon_commande_with_statut_fusion(cnx, 2)
    print(liste_bon_commande)
    Bon_commande.Bon_commande.Insert.fusion_bon_commande(cnx, liste_bon_commande, session['utilisateur'][4])
    return redirect(url_for('consulter_bon_commande'))

@app.route("/alertes/")
def alertes():
    """
    Cette fonction renvoie la page des alertes.

    Elle récupère le nombre d'alertes et les informations sur les matériels en alerte,
    puis les transmet à la template "alertes.html" pour affichage.

    :return: Le rendu de la template "alertes.html" avec les données nécessaires.
    """
    nb_alertes = Alert.get_nb_alert(cnx)
    info_materiel = Alert.get_info_materiel_alert(cnx)
    return render_template(
        "alertes.html",
        alertes = str(nb_alertes),
        nb_alerte = nb_alertes,
        info_materiels = info_materiel,
        title="alertes",
        chemin = [("base", "accueil"), ("alertes", "alertes")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/etat/<int:id>")
def etat(id):
    """
    Affiche l'état d'un matériel spécifique en fonction de son identifiant.

    Args:
        id (int): L'identifiant du matériel.

    Returns:
        render_template: Le template "etat.html" avec les informations nécessaires pour afficher l'état du matériel.
    """
    idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, id)
    referenceMateriel, nomMateriel,estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif = Risques.Get.get_risque_with_idMateriel(cnx, idFDS)
    risques = [estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif]
    lenRisques = len(risques)

    return render_template(
        "etat.html",
        id=id,
        title="etat",
        risques = risques,
        lenRisques = len(risques),
        path = ['../static/images/FDS/toxique.png', '../static/images/FDS/inflammable.png', '../static/images/FDS/explosion.png', '../static/images/FDS/gaz.png', '../static/images/FDS/CMR.png', '../static/images/FDS/environnement.png', '../static/images/FDS/chimique.png', '../static/images/FDS/comburant.png', '../static/images/FDS/corrosif.png'],
        item_properties = Materiel.Get.get_all_information_to_Materiel_with_id(cnx, id),
        items_unique = MaterielUnique.Get.get_all_information_to_MaterielUnique_with_id(cnx, id),
        alertes = Alert.nb_alert_par_materielUnique_dict(cnx),
        chemin = [("base", "accueil"), ("inventaire", "inventaire"), ("inventaire", "etat")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/generer-fds/<int:idMat>")
def generer_fds(idMat):
    """
    Génère la fiche de données de sécurité (FDS) pour un matériel donné.

    Args:
        idMat (int): L'identifiant du matériel.

    Returns:
        flask.Response: Le fichier PDF de la FDS en tant que réponse à télécharger.
    """
    idFDS = FDS.Get.get_FDS_with_idMateriel(cnx, idMat)
    referenceMateriel, nomMateriel,estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif = Risques.Get.get_risque_with_idMateriel(cnx, idFDS)
    PDF_BonCommande.genererpdfFDS(session['utilisateur'][0], session['utilisateur'][3], referenceMateriel, nomMateriel,estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif)
    return send_file("static/data/FDS.pdf", as_attachment=True)
    # return redirect(url_for('inventaire'))

@app.route("/ajouter-utilisateur/")
def ajouter_utilisateur():
    """
    Cette fonction affiche le formulaire d'ajout d'un utilisateur et renvoie la page HTML correspondante.

    :return: La page HTML avec le formulaire d'ajout d'un utilisateur.
    """
    f = AjouterUtilisateurForm()
    return render_template(
        "ajouterUtilisateur.html",
        title="ajouter un utilisateur",
        AjouterUtilisateurForm=f,
        chemin=[("base", "accueil"), ("ajouter_utilisateur", "ajouter un Utilisateur")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/consulter-utilisateur/", methods=("GET","POST",))
@csrf.exempt
def consulter_utilisateur():
    """
    Fonction qui permet de consulter les utilisateurs en fonction de la catégorie sélectionnée.

    Returns:
        render_template: Le template "consulterUtilisateur.html" avec les utilisateurs correspondants à la catégorie sélectionnée.
    """
    f = RechercherForm()
    if 'cat' in request.form:
        selected_value = request.form['cat']
        print("Option sélectionnée : "+selected_value)
        if selected_value == "Tous":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx())[0],
                nbUser = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx())[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")],
                alerte_tl = Alert.get_nb_alert(cnx),
                demande_tl = Demande.Get.get_nb_demande(cnx)
            )
        elif selected_value == "Professeur":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 2)[0],
                nbUser = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 2)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")],
                alerte_tl = Alert.get_nb_alert(cnx),
                demande_tl = Demande.Get.get_nb_demande(cnx)
            )
        elif selected_value == "Gestionnaire":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 4)[0],
                nbUser = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 4)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")],
                alerte_tl = Alert.get_nb_alert(cnx),
                demande_tl = Demande.Get.get_nb_demande(cnx)
            )
        elif selected_value == "Laborantin":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 3)[0],
                nbUser = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 3)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")],
                alerte_tl = Alert.get_nb_alert(cnx),
                demande_tl = Demande.Get.get_nb_demande(cnx)
            )

    return render_template(
        "consulterUtilisateur.html",
        professeurs = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 2)[0],
        laborantins = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 3)[0],
        gestionnaires = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx(), 4)[0],
        utilisateurs = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx())[0],
        nbUser = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx())[1],
        categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
        title="consulter les utilisateurs",
        RechercherForm=f,
        chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/recherche-utilisateur/", methods=("GET","POST",))
@csrf.exempt
def recherche_utilisateur():
    """
    Fonction qui gère la recherche d'utilisateurs dans le système.

    Returns:
        template: Le template HTML pour afficher les résultats de la recherche.
    """
    f = RechercherForm()    
    value = f.get_value()
    print("value : "+value)
    if value != None:
        return render_template(
            "consulterUtilisateur.html",
            # utilisateurs = Recherche.recherche_all_in_utilisateur_with_search(get_cnx(), value)[0],
            professeurs = Recherche.recherche_all_in_utilisateur_with_search_statut(get_cnx(), value, 2)[0],
            laborantins = Recherche.recherche_all_in_utilisateur_with_search_statut(get_cnx(), value, 3)[0],
            gestionnaires = Recherche.recherche_all_in_utilisateur_with_search_statut(get_cnx(), value, 4)[0],
            nbUser = Recherche.recherche_all_in_utilisateur_with_search(get_cnx(), value)[1],
            categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
            title="consulter les utilisateurs",
            RechercherForm=f,
            chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")],
            alerte_tl = Alert.get_nb_alert(cnx),
            demande_tl = Demande.Get.get_nb_demande(cnx)
        )

    return render_template(
        "consulterUtilisateur.html",
        utilisateurs = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx())[0],
        nbUser = Bon_commande.Utilisateur.Utilisateur.Get.get_all_user(get_cnx())[1],
        categories = ["Tous", "Professeur", "Gestionnaire"],
        title="consulter les utilisateurs",
        RechercherForm=f,
        chemin = [("base", "accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "consulter les utilisateurs")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/supprimer-utilisateur/<int:id>", methods=("GET","POST",))
def supprimer_utilisateur(id):
    """
    Supprime un utilisateur en utilisant son identifiant.

    Args:
        id (int): L'identifiant de l'utilisateur à supprimer.

    Returns:
        redirect: Une redirection vers la page de consultation des utilisateurs.
    """
    Bon_commande.Utilisateur.Utilisateur.Delete.delete_utilisateur(cnx, id)
    print("supprimer utilisateur : "+str(id))
    return redirect(url_for('consulter_utilisateur'))

@app.route("/modifier-utilisateur/<int:id>/", methods=("GET","POST",))
def modifier_utilisateur(id):
    """
    Modifie un utilisateur en fonction de son identifiant.

    Args:
        id (int): L'identifiant de l'utilisateur à modifier.

    Returns:
        flask.Response: Une réponse de redirection vers la page 'consulter_utilisateur' en cas de succès, sinon une réponse de redirection vers la même page avec un message d'erreur.

    """
    f = AjouterUtilisateurForm()
    if f.validate_on_submit():
        nom, prenom, email, statut = f.get_full_user()
        print(statut)
        if nom != None and prenom != None and email != None and statut != None:
            if statut == "professeur":
                res = Bon_commande.Utilisateur.Utilisateur.Update.update_all_information_utillisateur_with_id(cnx, id, 2, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "gestionnaire":
                res = Bon_commande.Utilisateur.Utilisateur.Update.update_all_information_utillisateur_with_id(cnx, id, 4, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "laborantin":
                res = Bon_commande.Utilisateur.Utilisateur.Update.update_all_information_utillisateur_with_id(cnx, id, 3, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
    prenom, nom, email, statut = Bon_commande.Utilisateur.Utilisateur.Get.get_all_information_utilisateur_with_id(get_cnx(), id)
    return render_template(
        "modifierUtilisateur.html",
        title="modifier un utilisateur",
        AjouterUtilisateurForm=f,
        nom=nom,
        prenom=prenom,
        email=email,
        statut=statut,
        id=id,
        chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs"), ("consulter_utilisateur", "modifier un utilisateur")], 
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/modifier-materiel/<int:id>", methods=("GET","POST",))
def modifier_materiel(id):
    """
    Modifie un matériel dans la base de données en fonction de l'ID fourni.

    Args:
        id (int): L'ID du matériel à modifier.

    Returns:
        redirect: Redirige vers la page d'état du matériel modifié si la modification est réussie.
        redirect: Redirige vers la page d'inventaire si la modification échoue.

    """
    FDSFormulaire = FDSForm()
    materiel = Materiel.Get.get_materiel(cnx, id)
    idMateriel, referenceMateriel, idFDS, nomMateriel, idCategorie, seuilAlerte, caracteristiquesCompelmentaires, informationsComplementairesEtSecurite = materiel[0]

    referenceMateriel, nomMateriel, estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif = Risques.Get.get_risque_with_idMateriel(cnx, idFDS)
    print(estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif)


    idDomaine = Domaine.Domaine.get_id_domaine_from_categorie(cnx, idCategorie)
    f = AjouterMaterielForm()
    f.nom.default = nomMateriel
    f.reference.default = referenceMateriel
    f.caracteristiques.default = caracteristiquesCompelmentaires
    f.infossup.default = informationsComplementairesEtSecurite
    f.seuilalerte.default = str(seuilAlerte)
    f.domaine.choices = get_domaine_choices() 
    f.domaine.default = str(idDomaine)
    f.categorie.choices = get_categorie_choices_modifier_materiel(idDomaine)
    f.categorie.default = str(idCategorie)
    f.process()

    if f.validate_on_submit() :
        categorie, nom, reference, caracteristiques, infossup, seuilalerte = f.get_full_materiel_requestform()
        res = Materiel.Update.modifie_materiel(cnx, idMateriel, categorie, nom, reference, caracteristiques, infossup, seuilalerte)
        
        toxique, inflammable, explosif, gaz, CMR, environnement, chimique, comburant, corrosif = FDSFormulaire.get_full_fds()
        Risques.Update.update_risque_with_idMateriel(cnx, id, toxique, inflammable, explosif, gaz, CMR, chimique, environnement, comburant, corrosif)
        RELOAD.reload_alert(cnx)
        if res:
            return redirect(url_for('etat', id=idMateriel))
        else:
            print("Erreur lors de la modification du matériel")
            return redirect(url_for('inventaire'))
    else :
        print("Erreur lors de la validation du formulaire")
        print(f.errors)
    return render_template(
        "modifierMateriel.html",
        title="modifier un matériel",
        AjouterMaterielForm=f,
        id = idMateriel,
        FDSForm=FDSFormulaire,
        estToxique = estToxique,
        estInflamable = estInflamable,
        estExplosif = estExplosif,
        est_gaz_sous_pression = est_gaz_sous_pression,
        est_CMR = est_CMR,
        est_chimique_environement = est_chimique_environement,
        est_dangereux = est_dangereux,
        est_comburant = est_comburant,
        est_corrosif = est_corrosif,
        chemin = [("base", "accueil"),("inventaire","inventaire"), ("inventaire", "modifier un matériel")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/modifier-materiel-unique/<int:id>", methods=("GET","POST",))
def modifier_materiel_unique(id):
    """
    Modifie les informations d'un matériel unique en stock.

    Args:
        id (int): L'identifiant du matériel unique.

    Returns:
        flask.Response: La réponse de redirection vers la page d'état du matériel.

    """
    materiel = MaterielUnique.Get.get_materiel_unique(cnx, id)
    idMaterielUnique, idMateriel, idRangement, dateReception, commentaireMateriel, quantiteApproximative, datePeremption = materiel[0]
    idEndroit = Rangement.Get.get_id_endroit_from_id_rangement(cnx, idRangement)
    f = ModifierMaterielUniqueForm()
    f.date_reception.default = dateReception
    f.date_peremption.default = datePeremption
    f.commentaire.default = commentaireMateriel
    f.quantite_approximative.default = str(quantiteApproximative)
    f.endroit.choices = get_endroit_choices() 
    f.endroit.default = str(idRangement)
    f.position.choices = get_position_choices_modifier_materiel(idRangement)
    f.position.default = str(idEndroit)
    f.process()

    if f.validate_on_submit() :
        position, date_reception, date_peremption, commentaire, quantite_approximative = f.get_full_materiel_unique_requestform()
        res = MaterielUnique.Update.modifie_materiel_unique(cnx, id, position, date_reception, date_peremption, commentaire, quantite_approximative)
        RELOAD.reload_alert(cnx)
        if res:
            return redirect(url_for('etat', id=idMateriel))
        else:
            print("Erreur lors de l'insertion du matériel")
            return redirect(url_for('etat', id=idMateriel))
    else :
        print("Erreur lors de la validation du formulaire")
        print(f.errors)
    return render_template(
        "modifierMaterielUnique.html",
        title="modifier les informations d'un matériel en stock",
        ModifierMaterielUniqueForm=f,
        id=id,
        chemin=[("base", "accueil"),("inventaire","inventaire"),("inventaire","modifier un matériel unique")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/supprimer-materiel-unique/<int:id>", methods=("GET","POST",))
def supprimer_materiel_unique(id):
    """
    Supprime un matériel unique de la base de données.

    Args:
        id (int): L'identifiant du matériel unique à supprimer.

    Returns:
        redirect: Une redirection vers la page d'état du matériel correspondant.
    """
    print(1)
    id_materiel = Materiel.Get.get_id_materiel_from_id_materiel_unique(cnx, id)
    print(2)
    MaterielUnique.Delete.supprimer_materiel_unique_bdd(cnx, id)
    print(3)
    return redirect(url_for('etat', id=id_materiel))

@app.route("/supprimer-materiels-uniques/<int:id>", methods=("GET","POST",))
def supprimer_materiels_uniques(id):
    """
    Supprime tous les matériels uniques associés à un identifiant donné.
    Supprime également tous les matériels en stock dans le laboratoire associés à cet identifiant.
    Redirige vers la page d'inventaire après la suppression.
    
    Args:
        id (int): L'identifiant du matériel à supprimer.
    
    Returns:
        redirect: Une redirection vers la page d'inventaire.
    """
    MaterielUnique.Delete.delete_all_materiel_unique_with_idMateriel(cnx, id)
    Materiel.Delete.delete_all_materiel_in_Stocklaboratoire_with_idMat(cnx, id)
    return redirect(url_for('inventaire'))

@app.route("/demandes/")
def demandes():
    return render_template(
        "demandes.html",
        title="demandes",
        nb_demande = int(Demande.Get.get_nb_demande(cnx)),
        info_demande = Demande.Get.get_info_demande(cnx),
        chemin = [("base", "accueil"), ("demandes", "demandes")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/demande/<int:idDemande>")
def demande(idDemande):
    id_user = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    info_commande = Demande.Get.get_info_demande_with_id(get_cnx(), idDemande)

    return render_template(
        "demande.html",
        idDemande = idDemande,
        infoCommande = info_commande,
        longeur = len(info_commande),
        idUser = id_user,
        title = "demande de "+ info_commande[0][0] + " " + info_commande[0][1],
        chemin = [("base", "accueil"), ("demandes", "demandes"), ('demandes', 'demandes')],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/inventaire/")
@csrf.exempt
def inventaire():
    rechercher = RechercherForm()
    items = Recherche.recherche_all_in_inventaire(get_cnx())

    print("items : ",items)

    # N'affiche uniquement les matériels qui ont des unités supérieur à 0

    if items[1] != 0:

        final_items = list()
        for (item,qt) in items[0]:
            if qt > 0:
                if (item,qt) not in final_items: # Eviter les doublons
                    final_items.append((item,qt))

        return render_template(
            "inventaire.html",
            RechercherForm=rechercher,
            categories = Domaine.Domaine.get_domaine(get_cnx()),
            items = final_items,
            nbMateriel = items[1],
            alertes = Alert.nb_alert_par_materiel_dict(get_cnx()),
            title="inventaire",
            chemin = [("base", "accueil"), ("inventaire", "inventaire")],
            alerte_tl = Alert.get_nb_alert(cnx),
            demande_tl = Demande.Get.get_nb_demande(cnx)
        )
    else:
        return redirect(url_for('base'))

@app.route("/rechercher-inventaire", methods=("GET","POST",))
@csrf.exempt
def recherche_inventaire():
    """
    Fonction qui effectue une recherche dans l'inventaire et renvoie les résultats.

    Returns:
        Flask response: Le template "inventaire.html" avec les résultats de la recherche.
    """
    rechercher = RechercherForm()
    value = rechercher.get_value()
    items = Recherche.recherche_all_in_inventaire_with_search(get_cnx(),value)
    
    final_items = list()
    for (item,qt) in items[0]:
        if qt > 0:
            if (item,qt) not in final_items: # Eviter les doublons
                final_items.append((item,qt))

    if value != None:
        return render_template(
            "inventaire.html",
            categories = Domaine.Domaine.get_domaine(get_cnx()),
            items = final_items,
            title="inventaire",
            alertes = Alert.nb_alert_par_materiel_dict(get_cnx()),
            nbMateriel = items[1],
            RechercherForm=rechercher,
            chemin = [("base", "Accueil"), ("inventaire", "inventaire")],
            alerte_tl = Alert.get_nb_alert(cnx),
            demande_tl = Demande.Get.get_nb_demande(cnx)
        )
    return redirect(url_for('inventaire'))
  
@app.route("/demander/")
@csrf.exempt
def demander():
    """
    Cette fonction affiche la page de demande de matériel.
    Elle récupère les informations nécessaires à l'affichage de la page,
    telles que la liste du matériel disponible, l'identifiant de la demande actuelle,
    et les informations de l'utilisateur connecté.
    """
    recherche = RechercherForm()
    idUser = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    liste_materiel = Demande.Get.afficher_demande(cnx, idUser)
    idDemande = Demande.Get.get_id_demande_actuel(cnx, idUser)
    print(liste_materiel)
    print(len(liste_materiel))
    return render_template(
        "demander.html",
        title="demander",
        idDemande = idDemande,
        liste_materiel = liste_materiel,
        nbMateriel = len(liste_materiel),
        RechercherForm=recherche,
        categories = Domaine.Domaine.get_domaine(get_cnx()),
        idUser = idUser,
        chemin = [("base", "accueil"), ("demander", "demander")],
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/ajouter-demande/<int:id>", methods=("GET","POST",))
def ajouter_demande(id):
    """
    Ajoute une demande avec l'identifiant de la matière, la quantité et redirige vers la page 'demander'.
    
    Args:
        id (int): L'identifiant de la matière.
    
    Returns:
        redirect: Redirection vers la page 'demander'.
    """
    idMat = request.args.get('idMat')
    qte = request.args.get('qte')

    print("demande ajouter")
    
    return redirect(url_for('demander'))


@app.route("/commentaire/", methods=("GET","POST",))
def commentaire():
    """
    Fonction qui gère l'envoi de commentaires ou de signalements.

    Cette fonction récupère le matériel concerné depuis les arguments de la requête.
    Ensuite, elle récupère les utilisateurs ayant le statut "Gestionnaire".
    Elle crée une instance de CommentaireForm.
    Si le formulaire est valide, elle récupère le texte et le gestionnaire sélectionné.
    Si le texte et le gestionnaire sont renseignés, elle envoie un mail de commentaire ou de signalement.
    Enfin, elle renvoie le template "commentaire.html" avec les utilisateurs, le titre, le matériel, le chemin et le formulaire.

    :return: Le template "commentaire.html" avec les données nécessaires.
    """
    materiel = request.args.get('materiel')
    users = Bon_commande.Utilisateur.Utilisateur.Get.get_user_with_statut(get_cnx(), "Gestionnaire")
    f = CommentaireForm()
    if f.validate_on_submit():
        text, gest = f.get_text()
        if text != None and gest != None:
            if materiel == None:
                mail = session['utilisateur'][2]
                envoyer_mail_commentaire(gest, mail, text)
                time.sleep(.5)
                return redirect(url_for('base'))
            else:
                mail = session['utilisateur'][2]
                envoyer_mail_signalement(gest, mail, text, materiel)
                time.sleep(.5)
                return redirect(url_for('base'))
    return render_template(
        "commentaire.html",
        users = users,
        title ="envoyer un commentaire",
        materiel = materiel,
        chemin = [("base", "accueil"), ("commentaire", "envoyer un commentaire")],
        CommentaireForm=f,
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )


@app.route("/login/", methods=("GET","POST",))
def login():
    """
    Fonction qui gère la page de connexion.
    Permet à l'utilisateur de se connecter en utilisant un formulaire de connexion.
    Si les informations de connexion sont valides, l'utilisateur est redirigé vers la page suivante.
    Sinon, un message d'erreur est affiché.
    """
    f = LoginForm ()
    changerMDP = ChangerMDPForm()
    changerMail = ChangerMailForm()
    mdpOublier = MdpOublierForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        try:
            nom, idStatut, mail, prenom = f.get_authenticated_user()
            user = nom, idStatut, mail, prenom
            if user != None:
                #login_user(user)
                idUt = Bon_commande.Utilisateur.Utilisateur.Get.get_id_with_email(cnx, user[2])
                session['utilisateur'] = (nom, idStatut, mail, prenom, idUt)
                RELOAD.reload_alert(cnx)
                print("login : "+str(session['utilisateur']))
                next = f.next.data or url_for("base")
                return redirect(next)
        except:
            print("erreur de connexion")
            return render_template(
                "login.html",
                title="profil",
                form=f,
                fromChangerMDP=changerMDP,
                fromChangerMail=changerMail,
                MdpOublierForm=mdpOublier,
                erreur = "le mail ou le mot de passe est incorrect",
                alerte_tl = Alert.get_nb_alert(cnx),
                demande_tl = Demande.Get.get_nb_demande(cnx)
            )        
        
    return render_template(
        "login.html",
        title="profil",
        form=f,
        fromChangerMDP=changerMDP,
        fromChangerMail=changerMail,
        MdpOublierForm=mdpOublier,
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )



# @app.route("/login/", methods=("GET","POST",))
# def login():
#     f = LoginForm ()
#     changerMDP = ChangerMDPForm()
#     changerMail = ChangerMailForm()
#     mdpOublier = MdpOublierForm()
#     if not f.is_submitted():
#         f.next.data = request.args.get("next")
#     elif f.validate_on_submit():
#         #nom, idStatut, mail, prenom = f.get_authenticated_user()
#         #user = nom, idStatut, mail, prenom
#         #if user != None:
#             #login_user(user)
#             #idUt = Utilisateur.Get.get_id_with_email(cnx, user[2])
#             session['utilisateur'] = ("Lallier", 3, "mail", "Anna", 1)
#             print("login : "+str(session['utilisateur']))
#             RELOAD.reload_alert(cnx)
#             next = f.next.data or url_for("base")
#             return redirect(next)
#     return render_template(
#         "login.html",
#         title="profil",
#         form=f,
#         fromChangerMDP=changerMDP,
#         fromChangerMail=changerMail,
#         MdpOublierForm=mdpOublier
#     )


@app.route("/logout/")
def logout():
    """
    Déconnecte l'utilisateur en supprimant sa session et redirige vers la page de base.
    """
    session.pop('utilisateur', None)
    return redirect(url_for('base'))

@app.route("/changerMDP/", methods=("GET","POST",))
def changerMDP():
    """
    Cette fonction affiche le formulaire de changement de mot de passe et gère la soumission du formulaire.

    Returns:
        Si le formulaire est soumis avec succès et les conditions sont remplies, la fonction redirige vers la page de confirmation de changement de mot de passe.
        Sinon, la fonction rend le template "login.html" avec le formulaire de changement de mot de passe.
    """
    f = ChangerMDPForm()
    if f.validate_on_submit():
        ancienMDP, nouveauMDP, confirmerMDP = f.get_full_mdp()
        if ancienMDP != None and nouveauMDP != None and confirmerMDP != None:
            if nouveauMDP == confirmerMDP:
                return redirect('/a2f/'+session['utilisateur'][2]+'/2?oldMdp='+ancienMDP+'&newMdp='+nouveauMDP)
    return render_template(
        "login.html",
        fromChangerMDP=f,
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/changerMail/", methods=("GET","POST",))
def changerMail():
    """
    Cette fonction gère le changement d'adresse e-mail de l'utilisateur.

    Returns:
        flask.Response: Redirige vers la page de vérification à deux facteurs si les conditions sont remplies.
        flask.Response: Rend le template "login.html" avec le formulaire de changement d'adresse e-mail.
    """
    f = ChangerMailForm()
    if f.validate_on_submit():
        ancienMail, nouveauMail, confirmerMail, mdp = f.get_full_mail()
        if ancienMail != None and nouveauMail != None and confirmerMail != None and mdp != None:
            if nouveauMail == confirmerMail and ancienMail == session['utilisateur'][2]:
                return redirect('/a2f/'+session['utilisateur'][2]+'/3?newMail='+nouveauMail+'&oldMail='+ancienMail+'&mdp='+mdp)
    return render_template(
        "login.html",
        fromChangerMail=f,
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

@app.route("/ajouterUtilisateur/", methods=("GET","POST",))
def ajouterUtilisateur():
    """
    Ajoute un utilisateur à la base de données en fonction des informations fournies dans le formulaire.
    
    Returns:
        - Si l'ajout est réussi, redirige vers la page 'consulter_utilisateur'.
        - Si l'ajout échoue, redirige vers la page 'consulter_utilisateur' et affiche un message d'erreur.
    """
    f = AjouterUtilisateurForm()
    if f.validate_on_submit():
        nom, prenom, email, statut = f.get_full_user()
        if nom != None and prenom != None and email != None and statut != None:
            if statut == "professeur":
                res = Bon_commande.Utilisateur.Utilisateur.Insert.ajout_professeur(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "gestionnaire":
                res = Bon_commande.Utilisateur.Utilisateur.Insert.ajout_gestionnaire(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "laborantin":
                res = Bon_commande.Utilisateur.Utilisateur.Insert.ajout_laborantin(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
    return render_template(
        "ajouterUtilisateur.html",
        fromAjouterUtilisateur=f,
        alerte_tl = Alert.get_nb_alert(cnx),
        demande_tl = Demande.Get.get_nb_demande(cnx)
    )

def get_domaine_choices():
    """
    Récupère les choix de domaine à partir de la base de données.

    :return: Une liste de tuples contenant les choix de domaine.
    """
    query = text("SELECT nomDomaine, idDomaine FROM DOMAINE;")
    result = cnx.execute(query)
    domaines =  [(str(id_), name) for name, id_ in result]
    domaines.insert(0, ("", "Choisir un domaine"))
    return domaines

def get_categorie_choices_modifier_materiel(idDomaine):
    """
    Récupère les choix de catégorie pour la modification du matériel.

    Args:
        idDomaine (int): L'identifiant du domaine.

    Returns:
        list: Une liste de tuples contenant les noms et les identifiants des catégories.
    """
    query = text("SELECT nomCategorie, idCategorie FROM CATEGORIE WHERE idDomaine =" + str(idDomaine) )
    result = cnx.execute(query)
    categories = [(str(id_), name) for name, id_ in result]
    return categories
