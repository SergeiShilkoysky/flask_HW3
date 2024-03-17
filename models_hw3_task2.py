from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)
    isvisible = db.Column(db.Boolean)


def __repr__(self):
    return f'Autor({self.username}, {self.surname})'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(80), nullable=False)  # название,
    public_year = db.Column(db.Integer, nullable=False)  # год издания
    copy_quantity = db.Column(db.Integer)  # количество экземпляров
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    isvisible = db.Column(db.Boolean)


def __repr__(self):
    return f'Book({self.book_title}, {self.public_year})'
