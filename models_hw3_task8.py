import random

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from enum import Enum

from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class enumproperty(object):
    "" "like property, but on an enum class """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, ownerclass=None):
        if ownerclass is None:
            ownerclass = instance.__class__
        return self.fget(ownerclass)

    def __set__(self, instance, value):
        raise AttributeError("can't set pseudo-member %r" % self.name)

    def __delete__(self, instance):
        raise AttributeError("can't delete pseudo-member %r" % self.name)


class Gender(Enum):
    """ Базовый класс модели Gender (наследует от класса Enum из библиотеки Enum) """

    FEMALE = 'female'
    MALE = 'male'

    @enumproperty
    def RANDOM(cls):
        return random.choice(list(cls.__members__.values()))


class User(db.Model):
    """ Класс модели User (наследует от класса Model из библиотеки SQLAlchemy) """

    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(30), nullable=False)

    # full_name = db.Column(db.String(80), nullable=False)

    # age = db.Column(db.Integer, nullable=True)
    # birthday = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(6), nullable=False)

    # created_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # updated_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # isvisible = db.Column(db.Boolean)

    # def __repr__(self):
    #     return (f'{self.name}, {self.surname}, {self.email} \n,'
    #             f'  {self.age}, {self.birthday} {self.gender}')
    def __repr__(self):
        return (f'{self.name}, {self.surname}, {self.gender} \n,'
                f'  {self.email} {self.password}')

    # def __repr__(self):
    #     return f'User("{self.full_name}", "{self.e_mail}")'

    def password_encryption(self, password):
        self.password = generate_password_hash(password)

    def password_validate(self, password):
        return check_password_hash(self.password, password)
