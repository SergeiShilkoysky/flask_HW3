"""
Задание №2
📌 Создать базу данных для хранения информации о книгах в библиотеке.
📌 База данных должна содержать две таблицы: "Книги" и "Авторы".
📌 В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
📌 В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
📌 Необходимо создать связь между таблицами "Книги" и "Авторы".
📌 Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.
"""

from flask import Flask, render_template
from models_hw3_task2 import db, Author, Book
from random import choice, randint
from turtle import isvisible

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app02_s3.db'
db.init_app(app)


@app.route('/')
def index():
    return 'Start page'


@app.route('/createdb/')
# @app.cli.command("createdb")
def createdb():
    db.create_all()
    return 'OK! db is create'
    # print('OK! db is create')


@app.route('/add_table/')
# @app.cli.command("add-table")
def add_table():
    # Добавляем авторов
    cnt_author = 5
    for auth in range(1, cnt_author + 1):
        new_author = Author(username=f'username{auth}', surname=f'Surname{auth}', isvisible=True)
        db.session.add(new_author)
    db.session.commit()
    print('authors added !')
    # Добавляем книги
    for book in range(1, cnt_author ** 2):
        # author = choice(range(1, cnt_author + 1))
        new_book = Book(book_title=f'book_title{book}', public_year=choice(range(2000, 2024)),
                        copy_quantity=choice(range(100, 10000)), author_id=randint(1, 5), isvisible=True)
        db.session.add(new_book)
    db.session.commit()
    print('books added !')
    return 'OK! Tables author, books - added'


@app.cli.command("del-author")
def del_author():
    del_auth = Author.query.filter_by(username='username2', isvisible=False).first()
    # db.session.delete(del_auth)
    db.session.commit()


@app.route('/all_books/')
def get_all_books():
    """функция вывода списка всех книг с указанием их авторов."""

    books = Book.query.all()
    context = {'books': books}
    return render_template('books_task2.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
