from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField, SelectField, \
    FileField
from wtforms.validators import DataRequired, Email, Length, NumberRange


SEX_LIST = ["Мужской", "Женский"]


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(2, message="NAME INVALID")])
    surname = StringField("Фамилия", validators=[DataRequired(), Length(2)])
    age = IntegerField("Возраст", validators=[DataRequired(), NumberRange(12, 100)])
    sex = SelectField("Пол", validators=[DataRequired()], choices=[sex for sex in SEX_LIST])
    email = EmailField("Почта", validators=[DataRequired(), Email("Некорректный Email")])
    avatar = FileField("Файл", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=100, message="PASS")])
    submit = SubmitField("Зарегистрироваться")
