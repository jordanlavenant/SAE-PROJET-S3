from .app import app #, db
from flask import render_template, url_for, redirect, request
#from flask_login import login_user, current_user, logout_user, login_required
#from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SubmitField
from wtforms.validators import DataRequired
from wtforms import PasswordField
from hashlib import sha256
from .requette import connexion_utilisateur, get_nom_whith_email, get_cnx

cnx = get_cnx()


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        user = get_nom_whith_email(get_cnx(), self.email.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None
    

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
        if user:
            get_nom_whith_email(get_cnx(), user)
            next = f.next.data or url_for("base")
            return redirect(next)
    return render_template(
        "login.html",
        form=f)

# @app.route("/logout/")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

