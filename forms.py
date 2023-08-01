"""Forms for Notes App"""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import InputRequired, Optional, Email, Length

class NewUserForm(FlaskForm):
    """Class for new user form"""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(max=20, min=4)
        ])

    # TODO: more validators for password
    password = StringField(
        "Password",
        validators=[
            InputRequired(),
            Length(max=20, min=8)
         ])

    email = StringField(
        "Email",
        validators=[
            Optional(),
            Email(message = "Must be a valid Email"),
            Length(max=50)
        ])

    first_name = StringField(
        "First Name",
        validators=[
            InputRequired(),
            Length(max=30)
        ])

    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(),
            Length(max=30)
        ])