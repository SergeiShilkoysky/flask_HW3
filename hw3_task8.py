"""
Задание №8
📌 Создать форму для регистрации пользователей на сайте.
📌 Форма должна содержать поля "Имя", "Фамилия", "Email",
"Пароль" и кнопку "Зарегистрироваться".
📌 При отправке формы данные должны сохраняться в базе
данных, а пароль должен быть зашифрован.
"""

from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from models_hw3_task8 import db, User
from flask_wtf.csrf import CSRFProtect
from hw3_task8_registr import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'be8cc38eac9cb4409b386cf380b7ed31d90a779e3a58e7b84ecb1d6275e0a880'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw3_task8_.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  #
db.init_app(app)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/init-db/')
# @app.cli.command("init-db")
def init_db():
    """ Function of table creation via Html (or via console command)."""

    db.create_all()
    print('OK, bd - create !')
    # return 'bd created successfully <br> для регистрации введите /register/'
    return redirect(url_for('register'))


@app.get('/hello/<name>')
def hello(name):
    return render_template('hello_task8.html', name=name)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Function for processing data from a form"""

    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        new_user = User(
            name=form.name.data,
            surname=form.surname.data,
            # age=form.age.data,
            # birthday=form.birthday.data,
            gender=form.gender.data,
            email=form.email.data,
            password=form.password.data)
        print(User)

        # ---------- if this returns a user, then the email already exists in database
        if User.query.filter_by(email=form.email.data).first():
            resp = make_response(redirect(url_for('register')))
            flash('Пользователь с таким email уже существует!', 'danger')
            return resp

        new_user.password_encryption(password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        resp = make_response(render_template('hello_task8.html', name=new_user.name, surname=new_user.surname))
        flash('Registration successfully!', 'success')
        return resp
    return render_template('register_task8.html', form=form)


@app.route('/users/', methods=['GET', 'POST'])
def get_users():
    """Function registered user output"""
    users = User.query.all()
    context = {'users': users}
    return render_template('users_bd_task8.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
