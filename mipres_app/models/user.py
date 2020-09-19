from sqlalchemy import Column, Unicode
from sqlalchemy_utils import PasswordType

from mipres_app.mipres import db_session


class User(db_session.Model):
    __tablename__ = 'user'

    email_address = Column(Unicode(255), unique=True, nullable=False)
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)
    first_name = Column(Unicode(255))
    last_name = Column(Unicode(255))

    def __repr__(self):
        return '<User: email=%s>' % self.email

    def __str__(self):
        return self.__repr__()
