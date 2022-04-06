from werkzeug.datastructures import FileStorage
from Data.Forms.LoginForm import LoginForm
from api import MainAPI
from Classes.ServerBuilder import ServerBuilder
from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
from Data.Models.User import User
from Classes.ImageHandler import ImageHandler
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user

application = Flask(__name__, template_folder="templates")
application.config.from_object("config.DevConfig")

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
        user = db_session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template("login.html",
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", title="Авторизация", form=form)


@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file: FileStorage = request.files['file']
        handler = ImageHandler()
        bites = handler.get_bytes(file)
        print(type(bites))
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
