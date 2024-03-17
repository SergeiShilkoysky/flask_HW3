from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()


class Gender(enum.Enum):
    male = 'malee'
    female = 'femalee'


class Fags(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    fag_name = db.Column(db.String(80), nullable=False)
    student = db.relationship('Students', backref=db.backref('fags'), lazy=True)

    # 'fags' - ссылка на ('fags.id_')

    def __repr__(self):
        return f'Fags({self.fag_name})'


class Students(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    group = db.Column(db.Integer, nullable=False)
    fags_id = db.Column(db.Integer, db.ForeignKey('fags.id_'), nullable=False)
    isvisible = db.Column(db.Boolean)

    # где fags таблица id_ класса Fags (переводится в нижний регистр)

    def __repr__(self):
        return f'Students({self.name}, {self.last_name}, {self.gender})'
