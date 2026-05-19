from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db


class Usuario(UserMixin, db.Model):

    __tablename__ = 'usuarios'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    rol = db.Column(
        db.String(50),
        default='admin'
    )

    # PASSWORD HASH

    def set_password(self, password):

        self.password = generate_password_hash(
            password
        )

    # VERIFY PASSWORD

    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )