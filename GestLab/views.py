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
        user = get_nom_and_statut_with_email(get_cnx(), self.email.data)
        mdp = get_password_with_email(get_cnx(), self.email.data)
        if user is None:
            return None
        # m = sha256()
        # m.update(self.password.data.encode('utf-8'))
        # passwd = m.hexdigest()
        passwd = hasher_mdp(self.password.data)
        print(str(mdp)+" == "+str(passwd))
        return user if passwd == mdp else None
    

@app.route("/")
def base():
    return render_template(
    "home.html",
    title="GestLab"
    )


@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm ()
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
        form=f)

@app.route("/logout/")
def logout():
    #logout_user()
    session.pop('utilisateur', None)
    return redirect(url_for('base'))

@app.route("/changerMDP/")
def changerMDP():
    return render_template(
    "changerMDP.html",
    title="GestLab"
    )
