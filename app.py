import pprint

from Classes.Lang import Lang
from api import MainAPI
from Classes.ServerBuilder import ServerBuilder
from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
from Classes.Token import Token
from Data.Models.User import User
from Data.Forms.LoginForm import LoginForm
from Data.Forms.RegisterForm import RegisterForm
from Data.Functions import load_environment_variable

import os

import requests
from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, current_user

application = Flask(__name__, template_folder="templates")
application.config.from_object("config.DevConfig")

load_environment_variable()

API = MainAPI(application)
server = ServerBuilder().get_server()

db = SqlAlchemyDatabase()

login_manager = LoginManager()
login_manager.init_app(application)


@login_manager.user_loader
def load_user(user_id):
    session = db.create_session()
    return session.query(User).get(user_id)


@application.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_session = db.create_session()
        user = db_session.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            access_token = Token()
            response = make_response(
                render_template("login.html", title="Авторизация",
                                message="Успешно!", form=form))
            response.set_cookie(
                "access_token",
                access_token.get_token(user.id),
                max_age=60 * 60 * 24 * 265 * 2
            )
            redirect("/")
            return response
        return render_template("login.html",
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", title="Авторизация", form=form)


@application.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        json_dict = {}
        data = dict(request.form)
        interests = []
        for key, val in data.items():
            if key.startswith("interest"):
                interests.append(val)
        if data["sex"] == "Мужской":
            data["sex"] = 1
        elif data["sex"] == "Женский":
            data["sex"] = 2
        json_dict["name"] = data["name"]
        json_dict["surname"] = data["surname"]
        json_dict["age"] = int(data["age"])
        json_dict["sex"] = data["sex"]
        json_dict["password"] = data["password"]
        json_dict["email"] = data["email"]
        json_dict["interests"] = interests
        url = "http://localhost:8080/api/v1/users"
        user_json = requests.post(url,
                                  json=json_dict).json()  # add user using api
        filename = user_json["user"]["images"][0][
            "image_href"]  # get image filename
        # TODO: проверить расширения файлов
        file = request.files['avatar']
        img_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
        file.save(img_path)  # save image to upload folder
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# TODO: Проверять, если access_token есть, то делать редирект на страницу с подбором пользователей
@application.route('/', methods=["GET"])
def index():
    return render_template("index.html", title="Главная")


# Test route
@application.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(application.config['UPLOAD_FOLDER'], filename))
    return '''
    <!doctype html>
    <title>Загрузить новый файл</title>
    <h1>Загрузить новый файл</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </html>
    '''


if __name__ == "__main__":
    application.run(host="localhost", port=8080)
