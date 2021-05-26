from app import db, session, Base
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import pbkdf2_sha256
#import hashlib

#https://lectureswww.readthedocs.io/6.www.sync/2.codding/9.databases/2.sqlalchemy/
class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    link = relationship('Link', backref='user',
                                lazy='dynamic')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = pbkdf2_sha256.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not pbkdf2_sha256.verify(password, user.password):
            raise Exception('Неверное имя пользователя или пароль')
        return user


class Original(Base):
    __tablename__ = 'original'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(300), nullable=False, unique=True)
    ink = relationship('Link', backref='original',
                       lazy='dynamic')


class Link(Base):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_id = db.Column(db.Integer, db.ForeignKey('original.id'))
    short_link = db.Column(db.String(200), nullable=False)
    friendly_link = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_id = db.Column(db.Integer)
    counter = db.Column(db.Integer, nullable=True)
