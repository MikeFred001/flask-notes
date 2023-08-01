"""Flask app for notes"""

import os

from flask import Flask, render_template, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, User, db
from forms import NewUserForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")

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


        #reject duplicate data
        if User.query.get(username):
            form.username.errors = ["That username is not available"]
        elif User.query.filter(User.email==email).one_or_none():
            form.email.errors =(
                ["An account with that email address already exists"]
            )
            #TODO: is there an easy way to show both errors?
        else:
            #register the user
            user = User(
                username=username,
                password=hashed,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            db.session.add(user)
            db.session.commit()

            #login as new user
            session['user_id'] = user.username
            return redirect(f'users/{user.username}')

    return render_template('new_user.html', form=form)


@app.route('/login', methods=["GET","POST"])
def handle_login():
    """Handles logins if user form is validated
    Shows the login form on GET or invalid form"""

    form = LoginForm()

    if form.validate_on_submit():
        #test user data against db
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username=username, password=password)

        if user:
            session['user_id'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad username/password"]

    return render_template('login.html', form=form)