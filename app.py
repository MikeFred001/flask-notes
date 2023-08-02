"""Flask app for notes"""
# TODO: Secret key in .env
import os

from flask import Flask, render_template, redirect, session, flash
from flask_bcrypt import Bcrypt

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import NewUserForm, LoginForm, CSRFProtectForm

bcrypt = Bcrypt()
app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")

toolbar = DebugToolbarExtension(app)

connect_db(app)

SESSION_USERNAME = 'username'

@app.get('/')
def start():
    """Redirects to registration page"""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def show_and_handle_register_form():
    """GET/Form Fail: Displays form for a user to register
    POST: Attempts to register user. On success, directs to user page."""

    form = NewUserForm()

    if form.validate_on_submit():


        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            #login as new user
            session[SESSION_USERNAME] = user.username
            return redirect(f'users/{user.username}')

        except ValueError as err:
            flash(str(err))
            return redirect('/register')

    return render_template('new_user.html', form=form)


@app.route('/login', methods=["GET","POST"])
def handle_login():
    """GET/Form fail: Shows login form
    POST: Attempts to log user in. On success, redirects to user page"""

    form = LoginForm()

    if form.validate_on_submit():
        #test user data against db
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username=username, password=password)

        if user:
            session[SESSION_USERNAME] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad username/password"]

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def display_user_info(username):
    """Displays info about current user if user is authorized"""

    if username != session.get('username'):
        flash("You must be logged in to view that page")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        form = CSRFProtectForm()
        return render_template('user.html', user=user, form=form)


@app.post('/logout')
def logout():
    """Logs current user out and redirects to home page"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(SESSION_USERNAME, None)

    else:
        flash('Quit scammin')
        return redirect('/')