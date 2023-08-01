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


@app.get('/')
def start():
    """Redirects to registration page"""

    return redirect('/register')


# TODO: Include redirect for already logged-in users.
@app.route('/register', methods=["GET", "POST"])
def show_register_form():
    #TODO: more descriptive function name
    """GET/Form Fail: Displays form for a user to register
    POST: Attempts to register user. On success, directs to user page."""

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
            #TODO: Abstract user registration to class method
            #TODO: Use try/except for database error catching,
            # implement in class method
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
            # TODO: global variable to hold session user pk

            #login as new user
            session['username'] = user.username
            return redirect(f'users/{user.username}')

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
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad username/password"]

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def display_user_info(username):
    """Displays info about current user if user is authorized"""
    #TODO: Verify authorization before retrieving user from db
    #TODO: Fail fast

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    if user.username == session.get('username'):
        return render_template('user.html', user=user, form=form)
    else:
        flash("You must be logged in to view that page")
        return redirect('/login')


@app.post('/logout')
def logout():
    """Logs current user out and redirects to home page"""
    #TODO:

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')