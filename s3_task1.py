"""
Задание №1
📌 Создать базу данных для хранения информации о студентах университета.
📌 База данных должна содержать две таблицы: "Студенты" и "Факультеты".
📌 В таблице "Студенты" должны быть следующие поля: id, имя, фамилия,
возраст, пол, группа и id факультета.
📌 В таблице "Факультеты" должны быть следующие поля: id и название
факультета.
📌 Необходимо создать связь между таблицами "Студенты" и "Факультеты".
📌 Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их факультета.
"""
import enum
from turtle import isvisible

# создал в папке локального проекта wsgi.py и 'sqlite:///app01_t.db' для БД внутри flask_S3


from flask import Flask, render_template
from models_s3_task1 import db, Students, Fags, Gender
from random import choice, randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app01_s3.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("add-user")
def add_user():
    # Добавляем факультеты
    for _ in range(1, 4):
        fag = Fags(fag_name=choice(['math', 'hist', 'lang']))
        db.session.add(fag)
    db.session.commit()
    # Добавляем студентов
    for i in range(1, 11):
        student = Students(name=f'name{i}', last_name=f'last_name{i}', age=i + 20,
                           gender=choice([Gender.male, Gender.female]), group=choice([1, 2, 3]), fags_id=randint(1, 3),
                           isvisible=True)
        db.session.add(student)
    db.session.commit()


@app.cli.command("del-user")
def del_student():
    user = Students.query.filter_by(username='name3', isvisible=False).first()
    # db.session.delete(user)
    db.session.commit()


# функция обработчик
@app.route('/')
def index():
    # print('*' * 50)
    student = Students.query.all()
    # print(student)
    return render_template('index_task1.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
