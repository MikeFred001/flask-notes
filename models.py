from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Class for User"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        if cls.query.get(username):
            raise ValueError("Username Already Exists")
        if cls.query.filter(cls.email==email).one_or_none():
            raise ValueError("Email Address Already Registered")

        user = cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct.
        Return user if valid, else returns False"""

        user = cls.query.filter_by(username=username).one_or_none()

        if (user and bcrypt.check_password_hash(user.password,password)):
            return user
        else:
            return False


    # class Note(db.Model):
    #     """Class for notes"""

    #     __tablename__ = "notes"



# Create a Note model:

# id - a unique primary key that is an auto incrementing integer
# title - a not-nullable column that is at most 100 characters
# content - a not-nullable column that is text
# owner_username - a foreign key that references the username column in the users table


