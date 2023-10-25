from .app import app #, db
from flask import render_template, url_for, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
#from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import PasswordField
from hashlib import sha256
from .requette import *
from .connexionPythonSQL import *


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
    value = StringField('value', validators=[DataRequired()])

    def get_value(self):
        value = self.value.data
        return value

class AjouterUtilisateurForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    choices = [('professeur', 'Professeur'), ('gestionnaire', 'Gestionnaire')]
    statut = SelectField('ComboBox', choices=choices)
    next = HiddenField()

    def get_full_user(self):
        nom = self.nom.data
        prenom = self.prenom.data
        email = self.email.data
        statut = self.statut.data
        return (nom, prenom, email, statut)


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

@app.route("/commander/")
def commander():
    return render_template(
    "commander.html",
    title="Commander"
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
    title="Alertes"
    )

@app.route("/etat/<int:id>")
def etat(id):
    return render_template(
    "etat.html",
    id=id,
    title="Etat",
    item_properties=get_all_information_to_Materiel_with_id(cnx, id)
    )

@app.route("/utilisateurs/")
def utilisateurs():
    return render_template(
    "utilisateurs.html",
    title="Utilisateurs"
    )

@app.route("/ajouter-utilisateur/")
def ajouter_utilisateur():
    f = AjouterUtilisateurForm()
    return render_template(
    "ajouterUtilisateur.html",
    title="Ajouter un Utilisateur",
    AjouterUtilisateurForm=f
    )

@app.route("/consulter-utilisateur/")
def consulter_utilisateur():
    return render_template(
    "consulterUtilisateur.html",
    title="Consulter les Utilisateurs"
    )

@app.route("/demandes/")
def demandes():
    return render_template(
    "demandes.html",
    title="Demandes"
    )

@app.route("/inventaire/")
def inventaire():
    javascript_code = """
    const maCombo = document.getElementById('categorie-select');
    maCombo.addEventListener('change', function () {
        console.log(maCombo.value);
    });
    """
    return render_template(
    "inventaire.html",
    categories = get_categories(get_cnx()),
    javascript_code = javascript_code,
    items = get_all_information_to_Materiel(get_cnx()),
    title="Inventaire"
    )

@app.route("/demander/")
def demander():
    return render_template(
    "demander.html",
    title="Demander"
    )

@app.route("/commentaire/")
def commentaire():
    return render_template(
    "commentaire.html",
    users= get_user_with_statut(get_cnx(), "Gestionnaire"),
    title="Envoyer un Commentaire"
    )

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm ()
    changerMDP = ChangerMDPForm()
    changerMail = ChangerMailForm()
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
        fromChangerMail=changerMail)

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
    return render_template(
        "ajouterUtilisateur.html",
        fromAjouterUtilisateur=f)