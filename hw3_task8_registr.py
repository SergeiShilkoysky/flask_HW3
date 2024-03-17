from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, PasswordField, DateField, validators, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    """ Form data validation class """

    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    # age = IntegerField('Age', validators=[DataRequired()])
    # birthday = DateField('Date birthday', format='%m/%d/%Y', default=date.today)
    gender = SelectField('Gender', choices=[('MALE', 'мужчина'), ('FEMALE', 'женщина')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6), Length(max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    check = BooleanField('consent to processing', validators=[DataRequired()])
