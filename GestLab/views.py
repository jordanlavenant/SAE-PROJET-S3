from .app import app #, db
from flask import render_template, url_for, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
#from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SubmitField
from wtforms.validators import DataRequired
from wtforms import PasswordField
from hashlib import sha256
from .requette import *

cnx = get_cnx()


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        user = get_nom_and_statut_and_email(get_cnx(), self.email.data)
        mdp = get_password_with_email(get_cnx(), self.email.data)
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
    

@app.route("/")
def base():
    return render_template(
    "home.html",
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
    return render_template(
    "alertes.html",
    title="Alertes"
    )

@app.route("/utilisateurs/")
def utilisateurs():
    return render_template(
    "utilisateurs.html",
    title="Utilisateurs"
    )

@app.route("/demandes/")
def demandes():
    return render_template(
    "demandes.html",
    title="Demandes"
    )

@app.route("/inventaire/")
def inventaire():
    return render_template(
    "inventaire.html",
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
                res = update_mdp_utilisateur(get_cnx(), session['utilisateur'][2], ancienMDP, nouveauMDP)
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
                res = update_email_utilisateur(get_cnx(), nouveauMail, session['utilisateur'][0], mdp)
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