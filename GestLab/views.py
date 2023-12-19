from .app import app, csrf #, db
from flask import render_template, url_for, redirect, request, session, jsonify, send_file
from flask_login import login_user, current_user, logout_user, login_required
#from .models import User
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, HiddenField, FileField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional
from wtforms import PasswordField
from hashlib import sha256
from .requetebd5 import *
from .connexionPythonSQL import *
from .models import *
import time
import datetime
from .genererpdf import *

cnx = get_cnx()

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        user = Utilisateur.Get.get_nom_and_statut_and_email(cnx, self.email.data)
        print(user)
        mdp = Utilisateur.Get.get_password_with_email(cnx, self.email.data)
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

class AjouterUtilisateurForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    choices = [('professeur', 'Professeur'), ('gestionnaire', 'Gestionnaire'), ('laborantin', 'Laborantin')]
    statut = SelectField('ComboBox', choices=choices)
    next = HiddenField()

    def get_full_user(self):
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
    caracteristiques = StringField('caracteristiques')
    infossup = StringField('infossup')
    seuilalerte  = IntegerField('seuilalerte')
    next = HiddenField()

    def get_full_materiel(self):
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
    gestionnaires = SelectField('ComboBox', choices=Utilisateur.Get.get_user_with_statut(get_cnx(), "Gestionnaire"))
    text = TextAreaField('text', validators=[DataRequired()])
    submit = SubmitField('envoyer le commentaire')

    def get_text(self):
        gest = self.gestionnaires.data
        text = self.text.data
        return text, gest
    
class MdpOublierForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('recevoir un nouveau mot de passe')

    def get_email(self):
        email = self.email.data
        return email

class AjouterStockForm(FlaskForm):
    materiel = SelectField('ComboBox', choices=[], id="materiel", name="materiel", validators=[DataRequired()])
    endroit = SelectField('ComboBox', choices=[], id="endroit", name="endroit", validators=[DataRequired()])
    position = SelectField('Position', choices=[], id="position", name="position", validate_choice=False, validators=[DataRequired()])
    domaine = SelectField('ComboBox', choices=[], id="domaine", name="domaine", validators=[DataRequired()])
    categorie = SelectField('Categorie', choices=[], id="categorie", name="categorie", validate_choice=False, validators=[DataRequired()])
    date_reception = DateField('date_reception', validators=[DataRequired()], default =  datetime.datetime.now().date())
    date_peremption = DateField('date_peremption', validators=[Optional()])
    nom = StringField('nom', validators=[DataRequired()])
    reference = StringField('reference', validators=[DataRequired()])
    caracteristiques = TextAreaField('caracteristiques')
    infossup = TextAreaField('infossup')
    seuilalerte  = StringField('seuilalerte')
    quantite_approximative = StringField('quantite_approximative', validators=[DataRequired()])
    commentaire = TextAreaField('commentaire')
    next = HiddenField()

    def get_full_materiel(self):
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

class AjouterMaterielUniqueForm(FlaskForm):
    materiel = SelectField('ComboBox', choices=[], id="materiel", name="materiel", validators=[DataRequired()])
    endroit = SelectField('ComboBox', choices=[], id="endroit", name="endroit", validators=[DataRequired()])
    position = SelectField('Position', choices=[], id="position", name="position", validate_choice=False, validators=[DataRequired()])
    date_reception = DateField('date_reception', validators=[DataRequired()], default =  datetime.datetime.now().date())
    date_peremption = DateField('date_peremption', validators=[Optional()])
    commentaire = TextAreaField('commentaire')
    quantite_approximative = StringField('quantite_approximative', validators=[DataRequired()])
    next = HiddenField()

    def get_full_materiel_unique(self):
        materiel = self.materiel.data
        position = self.position.data
        date_reception = self.date_reception.data
        date_peremption = self.date_peremption.data
        commentaire = self.commentaire.data
        quantite_approximative = self.quantite_approximative.data
        return (materiel, position, date_reception, date_peremption, commentaire, quantite_approximative)
    
    def get_full_materiel_unique_requestform(self):
        materiel = request.form['materiel']
        position = request.form['position']     
        date_reception = request.form['date_reception'] 
        date_peremption = request.form['date_peremption']
        commentaire = request.form['commentaire']
        quantite_approximative = request.form['quantite_approximative']
        return (materiel, position, date_reception, date_peremption, commentaire, quantite_approximative)

def get_domaine_choices():
    query = text("SELECT nomDomaine, idDomaine FROM DOMAINE;")
    result = cnx.execute(query)
    domaines =  [(str(id_), name) for name, id_ in result]
    domaines.insert(0, ("", "Choisir un domaine"))
    return domaines

@app.route('/get_categorie_choices/', methods=['GET'])
def get_categorie_choices():
    selected_domain_id = request.args.get('domaine_id')
    result = cnx.execute(text("SELECT nomCategorie, idCategorie FROM CATEGORIE WHERE idDomaine = " + str(selected_domain_id)))
    categories = {str(id_): name for name, id_ in result}
    return jsonify(categories)


def get_categorie_choices_modifier_materiel(idDomaine):
    query = text("SELECT nomCategorie, idCategorie FROM CATEGORIE WHERE idDomaine =" + str(idDomaine) )
    result = cnx.execute(query)
    categories = [(str(id_), name) for name, id_ in result]
    return categories

@app.route("/ajouter-suggestion/", methods=("GET","POST",))
def ajouter_suggestion():
    f = AjouterSuggestionForm()
    f.domaine.choices = get_domaine_choices() 
    if f.validate_on_submit() :
        categorie, nom, reference, caracteristiques, infossup, seuilalerte = f.get_full_materiel()
        res = Materiel.Insert.insere_materiel(cnx, categorie, nom, reference, caracteristiques, infossup, seuilalerte)
        if res:
            return redirect(url_for('demander'))
        else:
            print("Erreur lors de l'insertion du matériel")
            return redirect(url_for('ajouter_suggestion'))
    else :
        print("Erreur lors de la validation du formulaire")
        print(f.errors)
    return render_template(
    "ajouterSuggestion.html",
    title="ajouter une suggestion",
    AjouterSuggestionForm=f,
    chemin = [("base", "accueil"), ("ajouter_suggestion", "ajouter une suggestion")]
    )

@app.route("/ajouter-stock/", methods=("GET","POST",))
def ajouter_stock():
    rechercherForm = RechercherForm()
    ajouterForm = AjouterStockForm()
    ajouterForm.domaine.choices = get_domaine_choices() 
    if ajouterForm.validate_on_submit() :
        categorie, nom, reference, caracteristiques, infossup, seuilalerte = ajouterForm.get_full_materiel()
        res = Materiel.Insert.insere_materiel(cnx, categorie, nom, reference, caracteristiques, infossup, seuilalerte)
        if res:
            return redirect(url_for('demander'))
        else:
            print("Erreur lors de l'insertion du matériel")
            return redirect(url_for('ajouter_stock'))
    else :
        print("Erreur lors de la validation du formulaire")
        print(ajouterForm.errors)
    return render_template(
        "ajouterStock.html",
        title="ajouter au stock",
        AjouterStockForm=ajouterForm,
        RechercherForm=rechercherForm,
        chemin = [("base", "accueil"), ("ajouter_stock", "ajouter au stock")]
    )

def get_endroit_choices():
    query = text("SELECT endroit, idEndroit FROM ENDROIT;")
    result = cnx.execute(query)
    endroits =  [(str(id_), name) for name, id_ in result]
    endroits.insert(0, ("", "Choisir un endroit de rangement"))
    return endroits

@app.route('/get_position_choices/', methods=['GET'])
def get_position_choices():
    selected_endroit_id = request.args.get('endroit_id')
    result = cnx.execute(text("SELECT position, idRangement FROM RANGEMENT WHERE idEndroit = " + str(selected_endroit_id)))
    positions = {str(id_): name for name, id_ in result}
    return jsonify(positions)

def get_position_choices_modifier_materiel(idEndroit):
    query = text("SELECT position, idRangement FROM RANGEMENT WHERE idEndroit = " + str(idEndroit))
    result = cnx.execute(query)
    positions = [(str(id_), name) for name, id_ in result]
    return positions

def get_materiels_existants():
    query = text("SELECT nomMateriel, idMateriel FROM MATERIEL;")
    result = cnx.execute(query)
    materiels = [(str(id_), name) for name, id_ in result]
    return materiels

@app.route("/ajouter-materiel-unique/<int:id>", methods=("GET","POST",))
def ajouter_materiel_unique(id):
    f = AjouterMaterielUniqueForm()
    f.materiel.choices = get_materiels_existants()
    print(f.materiel.choices)
    print(type(f.materiel.choices))
    print(type(f.materiel.choices[0]))
    print(f.materiel.choices[0])
    f.endroit.choices = get_endroit_choices() 

    if f.validate_on_submit() :
        infosmateriel, position, date_reception, date_peremption, commentaire, quantite_approximative = f.get_full_materiel_unique()
        identifiant = infosmateriel[0]
        print(identifiant) 
        
        if STOCKLABORATOIRE.Get.materiel_dans_stock(get_cnx(), identifiant) <= 0 :
            STOCKLABORATOIRE.Insert.insere_materiel_stock(get_cnx(), identifiant)
        
        res = MaterielUnique.Insert.insere_materiel_unique(cnx, identifiant, position, date_reception, date_peremption, commentaire, quantite_approximative)
        
        if res:
            res = ReserveLaboratoire.Insert.insere_materiel_unique_reserve(cnx, id)
        
        if res:
            return redirect(url_for('etat', id=identifiant))
        
        else:
            print("Erreur lors de l'insertion du matériel")
            return redirect(url_for('ajouter_materiel'))
    else :
        print("Erreur lors de la validation du formulaire")
        print(f.errors)
    return render_template(
    "ajouterMaterielUnique.html",
    title="ajouter un matériel au stock",
    AjouterMaterielUniqueForm=f,
    id = id,
    chemin = [("base", "accueil")]
    )

class A2FForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('Valider')

    def get_code(self):
        code = self.code.data
        return code

@app.route("/")
def base():
    nb_alertes = Alert.get_nb_alert(cnx)
    nb_demandes = Demande.Get.get_nb_demande(cnx)
    return render_template(
    "home.html",
    alertes=str(nb_alertes),
    demandes=str(nb_demandes),
    title="GestLab"
    )

@app.route("/motdepasseoublie/", methods=("GET","POST",))
def mot_de_passe_oublier():
    f = MdpOublierForm()
    if f.validate_on_submit():
        email = f.get_email()
        return redirect(url_for('a2f', mail=email, id=1))
    return render_template(
        "login.html",
        MdpOublierForm=f)

@app.route("/a2f/<string:mail>/<int:id>", methods=("GET","POST",))
def a2f(mail, id):
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
        uri = Utilisateur.Get.get_uri_with_email(cnx, mail)
        if Authentification.verify(uri, code):
            if id == 1:
                Mots_de_passe.recuperation_de_mot_de_passe(cnx, mail)
                print("code valide")
                return redirect(url_for('login'))
            if id == 2:
                res = Utilisateur.Update.update_mdp_utilisateur(cnx, session['utilisateur'][2], oldMdp, newMdp)
                if res:
                    session.pop('utilisateur', None)
                    return redirect(url_for('login'))
                else:
                    print("erreur de changement de mdp")
                    return redirect(url_for('login'))
            if id == 3:
                res = Utilisateur.Update.update_email_utilisateur(cnx, newMail, session['utilisateur'][0], mdp, oldMail)
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
    )

@app.route("/reinitialiser-bon-commande/<int:id>", methods=("GET","POST",))
def reinitialiser_bon_commande(id):
    Materiel.Delete.delete_all_materiel_in_commande(cnx, id)
    return redirect(url_for('commander'))


@app.route("/commander-materiel-unique/<int:id>", methods=("GET","POST",))
def commander_materiel_unique(id):
    idDemande = request.args.get('idDemande')
    idMat = request.args.get('idMat')
    qte = request.args.get('qte')
    Materiel.Insert.ajout_materiel_in_commande(cnx, idMat, id, qte, False)
    # delete_materiel_unique_in_demande(cnx, idDemande, idMat)
    set
    return redirect(url_for('commander'))

@app.route("/commander-demande-materiel-unique/<int:id>", methods=("GET","POST",))
def commander_demande_materiel_unique(id):
    idDemande = request.args.get('idDemande')
    idMat = request.args.get('idMat')
    qte = request.args.get('qte')
    Materiel.Insert.ajout_materiel_in_commande(cnx, idMat, id, qte, True)
    MaterielUnique.Delete.delete_materiel_unique_in_demande(cnx, idDemande, idMat)
    return redirect(url_for('commander'))

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
    rechercher = RechercherForm()
    nb_alertes = Alert.get_nb_alert(cnx)
    nb_demandes = Demande.Get.get_nb_demande(cnx)
    idUser = Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idUser)
    liste_materiel = Bon_commande.Get.afficher_bon_commande(cnx, idUser)
    nbMateriel = len(liste_materiel)
    print(liste_materiel)
    return render_template(
        "commander.html",
        title="commander du matériel",
        categories = Domaine.get_domaine(get_cnx()),
        alertes=str(nb_alertes),
        demandes=str(nb_demandes),
        idUser = idUser,
        idbc = idbc,
        liste_materiel = liste_materiel,
        nbMateriel = nbMateriel,
        RechercherForm=rechercher,
        chemin = [("base", "accueil"), ("commander", "commander")]
    )

@app.route("/recherche-materiel", methods=("GET","POST",))
@csrf.exempt
def recherche_materiel():
    rechercher = RechercherForm()
    idUser = Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, idUser)
    value = rechercher.get_value()
    print("value : "+value)
    if value != None:
        liste_materiel = Recherche.recherche_all_in_materiel_with_search(get_cnx(), idbc, value)
        return render_template(
            "commander.html",
            title="commander",
            idUser = idUser,
            idbc = Bon_commande.Get.get_id_bonCommande_actuel(cnx, Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])),
            categories = Domaine.get_domaine(get_cnx()),
            RechercherForm=rechercher,
            liste_materiel = liste_materiel,
            nbMateriel = len(liste_materiel),
            alertes = Alert.get_nb_alert(cnx),
            demandes = Demande.Get.get_nb_demande(cnx),
            chemin = [("base", "accueil"), ("commander", "commander")]
        )
    return redirect(url_for('commander'))

@app.route("/bon-commande/<int:id>")
def bon_commande(id):
    idUser = Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    liste_materiel = Materiel.Get.get_materiel_commande(cnx, id)
    return render_template(
        "bonDeCommande.html",
        id = id,
        idUser = idUser,
        categories = Domaine.get_domaine(get_cnx()),
        title = "bon de commande",
        liste_materiel = liste_materiel,
        longueur = len(liste_materiel),
        chemin = [("base", "accueil"), ("commander", "commander"), ('demandes', 'bon de commande')]
    )
@app.route("/consulterBonCommande/")
def consulter_bon_commande():
    info_bon_commande = Bon_commande.Get.consulter_bon_commande_without_table(cnx)
    print(info_bon_commande)
    liste_info_user = []
    liste_etat_bon_commande = []
    nb_bon_commande_attente = 0
    for info in info_bon_commande:
        if info[1] == 2:
            nb_bon_commande_attente += 1
        liste_etat_bon_commande.append(Commande.Get.get_statut_from_commande_with_id_etat(cnx, info[1]))
        info_user = Utilisateur.Get.get_all_information_utilisateur_with_id(get_cnx(), info[2])
        liste_info_user.append(info_user)
    return render_template(
        "consulterBonCommande.html",
        title="consultation des bon de commande",
        len = len(info_bon_commande),
        nb_bon_commande_attente = nb_bon_commande_attente,
        bonCommande = info_bon_commande,
        infoUser = liste_info_user,
        listeEtat = liste_etat_bon_commande,
        statutsCommande = Commande.Get.get_statut_from_commande(cnx),
        chemin = [("base", "accueil"), ('consulter_bon_commande', 'consulter bon de commande')]
    )

@app.route("/changer-statut-bon-commande", methods=("GET","POST",))
def changer_statut_bon_commande():
    idbc = request.args.get('idbc')
    idStatut = request.args.get('statut')
    Bon_commande.Update.changer_etat_bonCommande_with_id(cnx, idbc, idStatut)
    return redirect(url_for('consulter_bon_commande'))

@app.route("/delete-materiel/<int:idbc>/<int:idMat>", methods=("GET","POST",))
def delete_materiel(idbc, idMat):
    Materiel.Delete.delete_materiel_in_BonCommande_whith_id(cnx, idMat, idbc)
    return redirect(url_for('bon_commande', id=idbc))

@app.route("/bon-commande-unique", methods=("GET","POST",))
def bon_commande_unique():
    idbc = request.args.get('idbc')
    liste_materiel = Bon_commande.Get.get_bon_commande_with_id(cnx, idbc)
    return render_template(
        "bonCommandeUnique.html",
        liste_materiel = liste_materiel,
        title="bon de commande n°"+str(idbc),
        idbc = idbc,
        chemin = [("base", "accueil"), ("consulter_bon_commande", "consulter bon de commande"), ("bon_commande_unique", "bon de commande")]
    )

@app.route("/historique-bon-commande")
def historique_bon_commande():
    info_bon_commande = Bon_commande.Get.get_bon_commande_with_statut(cnx, 4)
    liste_info_user = []
    liste_etat_bon_commande = []
    for info in info_bon_commande:
        liste_etat_bon_commande.append(Commande.Get.get_statut_from_commande_with_id_etat(cnx, info[1]))
        info_user = Utilisateur.Get.get_all_information_utilisateur_with_id(get_cnx(), info[2])
        liste_info_user.append(info_user)
    return render_template(
        "historiqueBonCommande.html",
        title="Historique des Bon de Commande",
        len = len(info_bon_commande),
        bonCommande = info_bon_commande,
        infoUser = liste_info_user,
        listeetat = liste_etat_bon_commande,
        statutsCommande = Commande.Get.get_statut_from_commande(cnx),
        # chemin = [("base", "accueil"), ("consulter_bon_commande, Consulter bon commande"), ("historique_bon_commande", "Historique des bon de commande")]
    )

@app.route("/delete-bon-commande/<int:id>", methods=("GET","POST",))
def delete_bon_commande(id):
    Bon_commande.Delete.delete_bonCommande_with_id(cnx, id)
    return redirect(url_for('consulter_bon_commande'))

@app.route("/valider-bon-commande/<int:id>", methods=("GET","POST",))
def valider_bon_commande(id):
    idCommande = request.args.get('idCommande')
    liste_materiel = Materiel.Get.get_all_materiel_for_pdf_in_bon_commande(cnx, id)
    print(liste_materiel)
    Bon_commande.Update.changer_etat_bonCommande(cnx, id)
    PDF_BonCommande.genererpdfBonCommande(session['utilisateur'][0], session['utilisateur'][3], liste_materiel, str(idCommande))
    while True:
        pass  # Cette boucle ne se termine jamais  
    return redirect(url_for('base'))

@app.route("/valider-bon-commande-pdf/<int:id>", methods=("GET","POST",))
def valider_bon_commande_pdf(id):
    liste_materiel = Materiel.Get.get_all_materiel_for_pdf_in_bon_commande_after(cnx, id)
    PDF_BonCommande.genererpdfBonCommande(session['utilisateur'][0], session['utilisateur'][3], liste_materiel, str(id))
    return send_file("static/data/bonCommande.pdf", as_attachment=True)

@app.route("/fusion-bon-commande")
def fusion_bon_commande():
    liste_bon_commande = Bon_commande.Get.get_bon_commande_with_statut_fusion(cnx, 2)
    print(liste_bon_commande)
    Bon_commande.Insert.fusion_bon_commande(cnx, liste_bon_commande, session['utilisateur'][4])
    return redirect(url_for('consulter_bon_commande'))

@app.route("/alertes/")
def alertes():
    nb_alertes = Alert.get_nb_alert(cnx)
    info_materiel = Alert.get_info_materiel_alert(cnx)
    return render_template(
        "alertes.html",
        alertes = str(nb_alertes),
        nb_alerte = nb_alertes,
        info_materiels = info_materiel,
        title="alertes",
        chemin = [("base", "accueil"), ("alertes", "Alertes")]
    )

@app.route("/etat/<int:id>")
def etat(id):
    return render_template(
        "etat.html",
        id=id,
        title="etat",
        item_properties = Materiel.Get.get_all_information_to_Materiel_with_id(cnx, id),
        items_unique = MaterielUnique.Get.get_all_information_to_MaterielUnique_with_id(cnx, id),
        alertes = Alert.nb_alert_par_materielUnique_dict(cnx),
        chemin = [("base", "accueil"), ("inventaire", "inventaire"), ("inventaire", "etat")]
    )

@app.route("/ajouter-utilisateur/")
def ajouter_utilisateur():
    f = AjouterUtilisateurForm()
    return render_template(
        "ajouterUtilisateur.html",
        title="ajouter un utilisateur",
        AjouterUtilisateurForm=f,
        chemin = [("base", "accueil"), ("ajouter_utilisateur", "Ajouter un Utilisateur")]
    )

@app.route("/consulter-utilisateur/", methods=("GET","POST",))
@csrf.exempt
def consulter_utilisateur():
    f = RechercherForm()
    if 'cat' in request.form:
        selected_value = request.form['cat']
        print("Option sélectionnée : "+selected_value)
        if selected_value == "Tous":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Utilisateur.Get.get_all_user(get_cnx())[0],
                nbUser = Utilisateur.Get.get_all_user(get_cnx())[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")]
            )
        elif selected_value == "Professeur":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Utilisateur.Get.get_all_user(get_cnx(), 2)[0],
                nbUser = Utilisateur.Get.get_all_user(get_cnx(), 2)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")]
            )
        elif selected_value == "Gestionnaire":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Utilisateur.Get.get_all_user(get_cnx(), 4)[0],
                nbUser = Utilisateur.Get.get_all_user(get_cnx(), 4)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")]
            )
        elif selected_value == "Laborantin":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = Utilisateur.Get.get_all_user(get_cnx(), 3)[0],
                nbUser = Utilisateur.Get.get_all_user(get_cnx(), 3)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="consulter les utilisateurs",
                RechercherForm=f,
                chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")]
            )

    return render_template(
        "consulterUtilisateur.html",
        utilisateurs = Utilisateur.Get.get_all_user(get_cnx())[0],
        nbUser = Utilisateur.Get.get_all_user(get_cnx())[1],
        categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
        title="consulter les utilisateurs",
        RechercherForm=f,
        chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")]
    )

@app.route("/recherche-utilisateur/", methods=("GET","POST",))
@csrf.exempt
def recherche_utilisateur():
    f = RechercherForm()    
    value = f.get_value()
    print("value : "+value)
    if value != None:
        return render_template(
            "consulterUtilisateur.html",
            utilisateurs = Recherche.recherche_all_in_utilisateur_with_search(get_cnx(), value)[0],
            nbUser = Recherche.recherche_all_in_utilisateur_with_search(get_cnx(), value)[1],
            categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
            title="consulter les utilisateurs",
            RechercherForm=f,
            chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs")]
        )

    return render_template(
        "consulterUtilisateur.html",
        utilisateurs = Utilisateur.Get.get_all_user(get_cnx())[0],
        nbUser = Utilisateur.Get.get_all_user(get_cnx())[1],
        categories = ["Tous", "Professeur", "Gestionnaire"],
        title="consulter les utilisateurs",
        RechercherForm=f,
        chemin = [("base", "accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "consulter les utilisateurs")]
    )

@app.route("/supprimer-utilisateur/<int:id>", methods=("GET","POST",))
def supprimer_utilisateur(id):
    Utilisateur.Delete.delete_utilisateur(cnx, id)
    print("supprimer utilisateur : "+str(id))
    return redirect(url_for('consulter_utilisateur'))

@app.route("/modifier-utilisateur/<int:id>/", methods=("GET","POST",))
def modifier_utilisateur(id):
    f = AjouterUtilisateurForm()
    if f.validate_on_submit():
        nom, prenom, email, statut = f.get_full_user()
        print(statut)
        if nom != None and prenom != None and email != None and statut != None:
            if statut == "professeur":
                res = Utilisateur.Update.update_all_information_utillisateur_with_id(cnx, id, 2, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "gestionnaire":
                res = Utilisateur.Update.update_all_information_utillisateur_with_id(cnx, id, 4, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "laborantin":
                res = Utilisateur.Update.update_all_information_utillisateur_with_id(cnx, id, 3, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
    prenom, nom, email, statut = Utilisateur.Get.get_all_information_utilisateur_with_id(get_cnx(), id)
    return render_template(
        "modifierUtilisateur.html",
        title="modifier un utilisateur",
        AjouterUtilisateurForm=f,
        nom=nom,
        prenom=prenom,
        email=email,
        statut=statut,
        id=id,
        chemin = [("base", "accueil"), ("consulter_utilisateur", "consulter les utilisateurs"), ("consulter_utilisateur", "modifier un utilisateur")] 
    )

@app.route("/modifier-materiel/<int:id>", methods=("GET","POST",))
def modifier_materiel(id):
    materiel = Materiel.Get.get_materiel(cnx, id)
    idMateriel, referenceMateriel, idFDS, nomMateriel, idCategorie, seuilAlerte, caracteristiquesCompelmentaires, informationsComplementairesEtSecurite = materiel[0]
                         
    idDomaine = Domaine.get_id_domaine_from_categorie(cnx, idCategorie)
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
        chemin = [("base", "accueil"),("inventaire", "Modifier un Matériel")]
    )

@app.route("/modifier-materiel-unique/<int:id>", methods=("GET","POST",))
def modifier_materiel_unique(id):
    materiel = MaterielUnique.Get.get_materiel_unique(cnx, id)
    idMaterielUnique, idMateriel, idRangement, dateReception, commentaireMateriel, quantiteApproximative, datePeremption = materiel[0]
    idEndroit = Rangement.Get.get_id_endroit_from_id_rangement(cnx, idRangement)
    f = AjouterMaterielUniqueForm()
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
        AjouterMaterielUniqueForm=f,
        id=id,
        chemin=[("base", "accueil")]
    )

@app.route("/supprimer-materiel-unique/<int:id>", methods=("GET","POST",))
def supprimer_materiel_unique(id):
    print(1)
    id_materiel = Materiel.Get.get_id_materiel_from_id_materiel_unique(cnx, id)
    print(2)
    MaterielUnique.Delete.supprimer_materiel_unique_bdd(cnx, id)
    print(3)
    return redirect(url_for('etat', id=id_materiel))

@app.route("/supprimer-materiels-uniques/<int:id>", methods=("GET","POST",))
def supprimer_materiels_uniques(id):
    MaterielUnique.Delete.delete_all_materiel_unique_with_idMateriel(cnx, id)
    return redirect(url_for('inventaire'))

@app.route("/demandes/")
def demandes():

    return render_template(
        "demandes.html",
        title="demandes",
        nb_demande = int(Demande.Get.get_nb_demande(cnx)),
        info_demande = Demande.Get.get_info_demande(cnx),
        chemin = [("base", "accueil"), ("demandes", "demandes")]
    )

@app.route("/demande/<int:idDemande>")
def demande(idDemande):
    id_user = Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2])
    info_commande = Demande.Get.get_info_demande_with_id(get_cnx(), idDemande)

    return render_template(
        "demande.html",
        idDemande = idDemande,
        infoCommande = info_commande,
        longeur = len(info_commande),
        idUser = id_user,
        title = "demande de "+ info_commande[0][0] + " " + info_commande[0][1],
        chemin = [("base", "accueil"), ("demandes", "demandes"), ('demandes', 'demandes')]
    )

@app.route("/inventaire/")
@csrf.exempt
def inventaire():
    rechercher = RechercherForm()
    items = Materiel.Get.get_all_information_to_Materiel(get_cnx())
    # print("-------------------")
    print(items)
    #for item in items[0]:
    #     print(item[0][4])
    # print("-------------------")
    # Longueur de l'inventaire : items[1]
    return render_template(
        "inventaire.html",
        RechercherForm=rechercher,
        categories = Domaine.get_domaine(get_cnx()),
        items = items,
        nbMateriel = items[1],
        alertes = Alert.nb_alert_par_materiel_dict(get_cnx()),
        title="inventaire",
        chemin = [("base", "accueil"), ("inventaire", "inventaire")]
    )

@app.route("/rechercher-inventaire", methods=("GET","POST",))
@csrf.exempt
def recherche_inventaire():
    rechercher = RechercherForm()
    value = rechercher.get_value()
    items = Recherche.recherche_all_in_inventaire_with_search(get_cnx(), value)
    print("value : "+value)
    print(items)
    if value != None:
        return render_template(
            "inventaire.html",
            categories = Domaine.get_domaine(get_cnx()),
            items = items,
            title="inventaire",
            alertes = Alert.nb_alert_par_materiel_dict(get_cnx()),
            nbMateriel = items[1],
            RechercherForm=rechercher,
            chemin = [("base", "Accueil"), ("inventaire", "Inventaire")]
        )
    return redirect(url_for('inventaire'))
  
@app.route("/demander/")
def demander():
    return render_template(
        "demander.html",
        title="demander",
        liste_materiel = Suggestion_materiel.get_all_information_to_Materiel_suggestions(get_cnx()),
        categories = Domaine.get_domaine(get_cnx()),
        idUser = Utilisateur.Get.get_id_with_email(cnx, session['utilisateur'][2]),
        chemin = [("base", "accueil"), ("demander", "demander")]
    )

@app.route("/ajouter-demande/<int:id>", methods=("GET","POST",))
def ajouter_demande(id):
    idMat = request.args.get('idMat')
    qte = request.args.get('qte')

    print("demande ajouter")
    
    return redirect(url_for('demander'))


@app.route("/commentaire/", methods=("GET","POST",))
def commentaire():
    materiel = request.args.get('materiel')
    print(materiel)
    users = Utilisateur.Get.get_user_with_statut(get_cnx(), "Gestionnaire")
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
        CommentaireForm=f
    )

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm ()
    changerMDP = ChangerMDPForm()
    changerMail = ChangerMailForm()
    mdpOublier = MdpOublierForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        nom, idStatut, mail, prenom = f.get_authenticated_user()
        user = nom, idStatut, mail, prenom
        if user != None:
            #login_user(user)
            idUt = Utilisateur.Get.get_id_with_email(cnx, user[2])
            session['utilisateur'] = (nom, idStatut, mail, prenom, idUt)
            print("login : "+str(session['utilisateur']))
            next = f.next.data or url_for("base")
            return redirect(next)
    return render_template(
        "login.html",
        title="profil",
        form=f,
        fromChangerMDP=changerMDP,
        fromChangerMail=changerMail,
        MdpOublierForm=mdpOublier
    )

@app.route("/logout/")
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('base'))

@app.route("/changerMDP/", methods=("GET","POST",))
def changerMDP():
    f = ChangerMDPForm()
    if f.validate_on_submit():
        ancienMDP, nouveauMDP, confirmerMDP = f.get_full_mdp()
        if ancienMDP != None and nouveauMDP != None and confirmerMDP != None:
            if nouveauMDP == confirmerMDP:
                return redirect('/a2f/'+session['utilisateur'][2]+'/2?oldMdp='+ancienMDP+'&newMdp='+nouveauMDP)
    return render_template(
        "login.html",
        fromChangerMDP=f)

@app.route("/changerMail/", methods=("GET","POST",))
def changerMail():
    f = ChangerMailForm()
    if f.validate_on_submit():
        ancienMail, nouveauMail, confirmerMail, mdp = f.get_full_mail()
        if ancienMail != None and nouveauMail != None and confirmerMail != None and mdp != None:
            if nouveauMail == confirmerMail and ancienMail == session['utilisateur'][2]:
                return redirect('/a2f/'+session['utilisateur'][2]+'/3?newMail='+nouveauMail+'&oldMail='+ancienMail+'&mdp='+mdp)
    return render_template(
        "login.html",
        fromChangerMail=f)

@app.route("/ajouterUtilisateur/", methods=("GET","POST",))
def ajouterUtilisateur():
    f = AjouterUtilisateurForm()
    if f.validate_on_submit():
        nom, prenom, email, statut = f.get_full_user()
        if nom != None and prenom != None and email != None and statut != None:
            if statut == "professeur":
                res = Utilisateur.Insert.ajout_professeur(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "gestionnaire":
                res = Utilisateur.Insert.ajout_gestionnaire(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
            elif statut == "laborantin":
                res = Utilisateur.Insert.ajout_laborantin(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('consulter_utilisateur'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('consulter_utilisateur'))
    return render_template(
        "ajouterUtilisateur.html",
        fromAjouterUtilisateur=f)

def get_domaine_choices():
    query = text("SELECT nomDomaine, idDomaine FROM DOMAINE;")
    result = cnx.execute(query)
    domaines =  [(str(id_), name) for name, id_ in result]
    domaines.insert(0, ("", "Choisir un domaine"))
    return domaines

def get_categorie_choices_modifier_materiel(idDomaine):
    query = text("SELECT nomCategorie, idCategorie FROM CATEGORIE WHERE idDomaine =" + str(idDomaine) )
    result = cnx.execute(query)
    categories = [(str(id_), name) for name, id_ in result]
    return categories