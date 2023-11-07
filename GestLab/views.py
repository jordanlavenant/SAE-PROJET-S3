from .app import app #, db
from flask import render_template, url_for, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
#from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import PasswordField
from hashlib import sha256
from .requetebd5 import *
from .connexionPythonSQL import *
from .models import *


cnx = get_cnx()

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        user = get_nom_and_statut_and_email(cnx, self.email.data)
        mdp = get_password_with_email(cnx, self.email.data)
        if user is None:
            return None
        # m = sha256()
        # m.update(self.password.data.encode('utf-8'))
        # passwd = m.hexdigest()
        passwd = hasher_mdp(self.password.data)
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
      
class RechercherFrom(FlaskForm):
    value = StringField('value')
    submit = SubmitField('Rechercher')

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

class CommentaireForm(FlaskForm):
    gestionnaires = SelectField('ComboBox', choices=get_user_with_statut(get_cnx(), "Gestionnaire"))
    text = TextAreaField('text', validators=[DataRequired()])
    submit = SubmitField('envoyer le commentaire')

    def get_text(self):
        gest = self.gestionnaires.data
        text = self.text.data
        return text, gest
    
class MdpOublierForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('Recevoir un nouveau mot de passe')

    def get_email(self):
        email = self.email.data
        return email


@app.route("/")
def base():
    nb_alertes = get_nb_alert(cnx)
    nb_demandes = get_nb_demande(cnx)
    return render_template(
    "home.html",
    alertes=str(nb_alertes),
    demandes=str(nb_demandes),
    title="votre chemin vers la facilité"
    )

@app.route("/motdepasseoublie/", methods=("GET","POST",))
def mot_de_passe_oublier():
    f = MdpOublierForm()
    if f.validate_on_submit():
        email = f.get_email()
        print("email : "+email)
        recuperation_de_mot_de_passe(cnx, email)
        return redirect(url_for('login'))
    return render_template(
        "login.html",
        MdpOublierForm=f)

@app.route("/commander/")
def commander():
    return render_template(
    "commander.html",
    title="Commander",
    chemin = [("base", "Accueil"), ("commander", "Commander")]
    )

@app.route("/bon-commande/")
def bon_commande():
    return render_template(
        "bonDeCommande.html",
        title = "Bon De Commande",
        chemin = [("base", "Accueil"), ("demandes", "Demandes"), ('demandes', 'Bon de Commande')]
    )

@app.route("/commander-materiel/")
def commander_materiel():
    nb_alertes = get_nb_alert(cnx)
    nb_demandes = get_nb_demande(cnx)
    return render_template(
        "commanderMateriel.html",
        title="Commander du Matériel",
        categories = get_domaine(get_cnx()),
        alertes=str(nb_alertes),
        demandes=str(nb_demandes),
        liste_materiel = get_info_rechercheMateriel(get_cnx()),
        chemin = [("base", "Accueil"), ("commander", "Commander"), ("commander_materiel", "Commander du Matériel")]
    )

@app.route("/alertes/")
def alertes():
    nb_alertes = get_nb_alert(cnx)
    nom_materiel = get_info_materiel_alert(cnx)
    return render_template(
    "alertes.html",
    alertes = str(nb_alertes),
    nb_alerte = nb_alertes,
    nom_materiels = nom_materiel,
    title="Alertes",
    chemin = [("base", "Accueil"), ("alertes", "Alertes")]
    )

@app.route("/etat/<int:id>")
def etat(id):
    return render_template(
    "etat.html",
    id=id,
    title="Etat",
    item_properties=get_all_information_to_Materiel_with_id(cnx, id),
    chemin = [("base", "Accueil"), ("inventaire", "Inventaire"), ("inventaire", "Etat")]
    )

@app.route("/utilisateurs/")
def utilisateurs():
    return render_template(
    "utilisateurs.html",
    title="Utilisateurs",
    chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs")]
    )

@app.route("/ajouter-utilisateur/")
def ajouter_utilisateur():
    f = AjouterUtilisateurForm()
    return render_template(
    "ajouterUtilisateur.html",
    title="Ajouter un Utilisateur",
    AjouterUtilisateurForm=f,
    chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("ajouter_utilisateur", "Ajouter un Utilisateur")]
    )

@app.route("/consulter-utilisateur/", methods=("GET","POST",))
def consulter_utilisateur():
    f = RechercherFrom()
    if 'cat' in request.form:
        selected_value = request.form['cat']
        print("Option sélectionnée : "+selected_value)
        if selected_value == "Tous":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = get_all_user(get_cnx())[0],
                nbUser = get_all_user(get_cnx())[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="Consulter les Utilisateurs",
                RechercherFrom=f,
                chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs")]
            )
        elif selected_value == "Professeur":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = get_all_user(get_cnx(), 2)[0],
                nbUser = get_all_user(get_cnx(), 2)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="Consulter les Utilisateurs",
                RechercherFrom=f,
                chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs")]
            )
        elif selected_value == "Gestionnaire":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = get_all_user(get_cnx(), 4)[0],
                nbUser = get_all_user(get_cnx(), 4)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="Consulter les Utilisateurs",
                RechercherFrom=f,
                chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs")]
            )
        elif selected_value == "Laborantin":
            return render_template(
                "consulterUtilisateur.html",
                utilisateurs = get_all_user(get_cnx(), 3)[0],
                nbUser = get_all_user(get_cnx(), 3)[1],
                categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
                title="Consulter les Utilisateurs",
                RechercherFrom=f,
                chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs")]
            )

    return render_template(
        "consulterUtilisateur.html",
        utilisateurs = get_all_user(get_cnx())[0],
        nbUser = get_all_user(get_cnx())[1],
        categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
        title="Consulter les Utilisateurs",
        RechercherFrom=f,
        chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs")]
    )

@app.route("/recherche-utilisateur/", methods=("GET","POST",))
def recherche_utilisateur():
    f = RechercherFrom()
    print("recherche utilisateur")
    
    value = f.get_value()
    print("value : "+value)
    if value != None:
        return render_template(
            "rechercheUtilisateur.html",
            utilisateurs = recherche_all_in_utilisateur_with_search(get_cnx(), value)[0],
            nbUser = recherche_all_in_utilisateur_with_search(get_cnx(), value)[1],
            categories = ["Tous", "Professeur", "Gestionnaire", "Laborantin"],
            title="Consulter les Utilisateurs",
            RechercherFrom=f,
            chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs")]
        )

    return render_template(
    "consulterUtilisateur.html",
    utilisateurs = get_all_user(get_cnx())[0],
    nbUser = get_all_user(get_cnx())[1],
    categories = ["Tous", "Professeur", "Gestionnaire"],
    title="Consulter les Utilisateurs",
    RechercherFrom=f,
    chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs")]
    )

@app.route("/modifier-utilisateur/<int:id>/", methods=("GET","POST",))
def modifier_utilisateur(id):
    f = AjouterUtilisateurForm()
    if f.validate_on_submit():
        nom, prenom, email, statut = f.get_full_user()
        if nom != None and prenom != None and email != None and statut != None:
            if statut == "professeur":
                res = update_all_information_utillisateur_with_id(cnx, id, 2, nom, prenom, email)
                if res:
                    return redirect(url_for('utilisateurs'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('utilisateurs'))
            elif statut == "gestionnaire":
                res = update_all_information_utillisateur_with_id(cnx, id, 4, nom, prenom, email)
                if res:
                    return redirect(url_for('utilisateurs'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('utilisateurs'))
            elif statut == "laborantin":
                res = update_all_information_utillisateur_with_id(cnx, id, 3, nom, prenom, email)
                if res:
                    return redirect(url_for('utilisateurs'))
                else:
                    print("erreur de modification d'utilisateur")
                    return redirect(url_for('utilisateurs'))
    prenom, nom, email, statut = get_all_information_utilisateur_with_id(get_cnx(), id)
    return render_template(
    "modifierUtilisateur.html",
    title="Modifier un Utilisateur",
    AjouterUtilisateurForm=f,
    nom=nom,
    prenom=prenom,
    email=email,
    statut=statut,
    id=id,
    chemin = [("base", "Accueil"), ("utilisateurs", "Utilisateurs"), ("consulter_utilisateur", "Consulter les Utilisateurs"), ("consulter_utilisateur", "Modifier un Utilisateur")] 
    )


@app.route("/demandes/")
def demandes():
    return render_template(
    "demandes.html",
    title="Demandes",
    nb_demande = get_nb_demande(cnx),
    info_demande = get_info_demande(cnx),
    chemin = [("base", "Accueil"), ("demandes", "Demandes")]
    )

@app.route("/inventaire/")
def inventaire():
    return render_template(
    "inventaire.html",
    categories = get_categories(get_cnx()),
    items = get_all_information_to_Materiel(get_cnx()),
    title="Inventaire",
    chemin = [("base", "Accueil"), ("inventaire", "Inventaire")]
    )

@app.route("/demander/")
def demander():
    return render_template(
    "demander.html",
    title="Demander",
    chemin = [("base", "Accueil"), ("demander", "Demander")]
    )

@app.route("/commentaire/", methods=("GET","POST",))
def commentaire():
    users = get_user_with_statut(get_cnx(), "Gestionnaire")
    f = CommentaireForm()
    if f.validate_on_submit():
        text, gest = f.get_text()
        if text != None and gest != None:
            mail = session['utilisateur'][2]
            envoyer_mail_commentaire(gest, mail, text)
            return redirect(url_for('base'))
    return render_template(
    "commentaire.html",
    users = users,
    title ="envoyer un commentaire",
    chemin = [("base", "Accueil"), ("commentaire", "envoyer un commentaire")],
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
        user = f.get_authenticated_user()
        if user != None:
            #login_user(user)
            session['utilisateur'] = user
            print("login : "+str(session['utilisateur']))
            next = f.next.data or url_for("base")
            return redirect(next)
    return render_template(
        "login.html",
        title="Profil",
        form=f,
        fromChangerMDP=changerMDP,
        fromChangerMail=changerMail,
        MdpOublierForm=mdpOublier
        )

@app.route("/logout/")
def logout():
    #logout_user()
    session.pop('utilisateur', None)
    return redirect(url_for('base'))

@app.route("/changerMDP/", methods=("GET","POST",))
def changerMDP():
    f = ChangerMDPForm()
    if f.validate_on_submit():
        ancienMDP, nouveauMDP, confirmerMDP = f.get_full_mdp()
        if ancienMDP != None and nouveauMDP != None and confirmerMDP != None:
            if nouveauMDP == confirmerMDP:
                res = update_mdp_utilisateur(cnx, session['utilisateur'][2], ancienMDP, nouveauMDP)
                if res:
                    session.pop('utilisateur', None)
                    return redirect(url_for('login'))
                else:
                    print("erreur de changement de mdp")
                    return redirect(url_for('login'))
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
                res = update_email_utilisateur(cnx, nouveauMail, session['utilisateur'][0], mdp)
                print(nouveauMail, session['utilisateur'][0], mdp)
                if res:
                    session.pop('utilisateur', None)
                    return redirect(url_for('login'))
                else:
                    print("erreur de changement de mail")
                    return redirect(url_for('login'))
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
                res = ajout_professeur(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('utilisateurs'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('utilisateurs'))
            elif statut == "gestionnaire":
                res = ajout_gestionnaire(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('utilisateurs'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('utilisateurs'))
            elif statut == "laborantin":
                res = ajout_laborantin(cnx, nom, prenom, email)
                if res:
                    return redirect(url_for('utilisateurs'))
                else:
                    print("erreur d'insertion d'utilisateur")
                    return redirect(url_for('utilisateurs'))
    return render_template(
        "ajouterUtilisateur.html",
        fromAjouterUtilisateur=f)

@app.route("/ajouter-materiel/")
def ajouter_materiel():
    return render_template(
    "ajouterMateriel.html",
    title="Ajouter un Matériel",
    chemin = [("base", "Accueil"), ("ajouter_materiel", "Ajouter un Matériel")]
    )