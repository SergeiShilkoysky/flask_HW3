"""
Задание №3
📌 Доработаем задача про студентов
📌 Создать базу данных для хранения информации о студентах и их оценках в
учебном заведении.
📌 База данных должна содержать две таблицы: "Студенты" и "Оценки".
📌 В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа
и email.
📌 В таблице "Оценки" должны быть следующие поля: id, id студента, название
предмета и оценка.
📌 Необходимо создать связь между таблицами "Студенты" и "Оценки".
📌 Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их оценок.
"""
from turtle import isvisible
from flask import Flask, render_template
from models_hw3_task3 import db, Students, Fags, Gender, Grades
from random import choice, randint, choices

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app03_s3.db'
db.init_app(app)

COUNT_FAGS = 5  # количество факультетов
LIST_FAGS = ['Math', 'History', 'Linguistics', 'Jurisprudence', 'Chemistry']
COUNT_STUDENTS = COUNT_FAGS * 2
COUNT_GRADES = COUNT_STUDENTS * COUNT_FAGS


@app.route('/')
def index():
    return 'Start page'


# @app.route('/init-db/')
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')
    return 'bd - create !'


# @app.route("/add-user/") # для web формы
@app.cli.command("add-user")
def add_user():
    # Добавляем факультеты
    for _ in range(1, COUNT_FAGS + 1):
        new_fag = Fags(fag_name=choice(LIST_FAGS), isvisible=True)
        db.session.add(new_fag)
    db.session.commit()
    print('table fags added')
    # Добавляем студентов
    for stud in range(1, COUNT_STUDENTS + 1):
        # new_student = Students(name=f'name{stud}', last_name=f'last_name{stud}', age=stud + 20,
        #                        gender=choice(Gender.LIST_GENDER), group=choice([1, 2, 3]),
        #                        fags_id=randint(1, COUNT_FAGS), isvisible=True)

        # new_student = Students(name=f'name{stud}', last_name=f'last_name{stud}', age=stud + 20,
        #                        gender=choice([Gender.male, Gender.female]), group=choice([1, 2, 3]),
        #                        fags_id=randint(1, COUNT_FAGS))

        new_student = Students(name=f'name{stud}', last_name=f'last_name{stud}', age=stud + 20,
                               gender=choice(['male', 'female']), group=choice([1, 2, 3]),
                               fags_id=randint(1, COUNT_FAGS), isvisible=True)

        db.session.add(new_student)
    db.session.commit()
    print('table student added')
    # return 'table fags & students added !' # для web формы


# @app.route("/add-grades/")
@app.cli.command("add-grades")
def add_grades():
    # Добавляем оценки
    for grade in range(1, COUNT_GRADES + 1):
        new_grade = Grades(student_id=choice([student.id_ for student in Students.query.all()]),
                           course_title=choice([fags.fag_name for fags in Fags.query.all()]),
                           course_grade=choice(range(2, 10)),
                           # created_grade=Grades.created_grade,
                           isvisible=True)
        db.session.add(new_grade)
    db.session.commit()
    print('table grades added')
    # return 'table grades added !'


@app.cli.command("/del-user/<text>/")
def del_user(text):
    user = Students.query.filter_by(username='text', isvisible=False).first()
    db.session.delete(user)
    db.session.commit()
    # return f' student {text} grades deleted'


@app.route('/students/')
def get_students():
    student = Students.query.all()
    context = {'student': student}
    return render_template('index_task1.html', **context)


@app.route('/students-with-grades/')
def get_students_grades():
    student = Students.query.all()
    grades = Grades.query.all()
    context = {'student': student,
               'grades': grades}
    return render_template('grades_task3.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
