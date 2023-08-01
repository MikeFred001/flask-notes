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
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).one_or_none()

        if (user and bcrypt.check_password_hash(user.password,password)):
            return user
        else:
            return False





