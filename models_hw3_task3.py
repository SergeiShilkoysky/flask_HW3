from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import enum

db = SQLAlchemy()


class Gender(enum.Enum):
    male = 'malee'
    female = 'femalee'
    LIST_GENDER = [male, female]


class Fags(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    fag_name = db.Column(db.String(80), nullable=False)
    isvisible = db.Column(db.Boolean)
    student = db.relationship('Students', backref=db.backref('fags'), lazy=True)

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

    def __repr__(self):
        return f'{self.name}, {self.last_name}, {self.gender}, \n группа: {self.group}'


class Grades(db.Model):  # таблица Оценки
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id_'), nullable=False)
    student = db.relationship('Students', backref=db.backref('grades'), lazy=True)  # обр.связь с табл.Students

    # course_title = db.Column(db.Integer, db.ForeignKey('fags.id_'), nullable=False)
    course_title = db.Column(db.String, db.ForeignKey('fags.fag_name'), nullable=False)  # название предмета (
    # факультет)
    fags = db.relationship('Fags', backref=db.backref('grades'), lazy=True)  # обр.связь с табл.Fags

    course_grade = db.Column(db.Integer)  # оценка по предмету
    # created_grade = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # дата выставления оценки
    isvisible = db.Column(db.Boolean)

    def __repr__(self):
        return f'{self.course_title}: {self.course_grade}'
