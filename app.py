"""Flask app for notes"""

import os

from flask import Flask, render_template, redirect, session, flash
from flask_bcrypt import bcrypt
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, User, db
from forms import NewUserForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
#     "DATABASE_URL", "postgresql:///placeholder")

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get('/')
def start():
    """Redirects to registration page"""

    return redirect('/register')


# TODO: Include redirect for already logged-in users.
@app.route('/register', methods=["GET", "POST"])
def show_register_form():
    """Displays form to register a user"""

    form = NewUserForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        if User.query.get(username):
            flash("That username is not available")
            return redirect('/register')

        if User.query.get(email):
            flash("An account with that email address already exists")
            return redirect('/register')

        user = User(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.username


    return render_template('new_user.html', form=form)