from Data.Forms.LoginForm import LoginForm
from api import MainAPI
from Classes.ServerBuilder import ServerBuilder
from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
from Data.Models.User import User

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user

application = Flask(__name__, template_folder=r"templates")
application.config.from_object("config.DevConfig")

API = MainAPI(application)
server = ServerBuilder().get_server()

db = SqlAlchemyDatabase()

login_manager = LoginManager()
login_manager.init_app(application)

# add log
@login_manager.user_loader
def load_user(user_id):
    session = db.create_session()
    return session.query(User).get(user_id)


@application.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session = db.create_session()
        user = db_session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", title="Авторизация", form=form)


if __name__ == "__main__":
    application.run(host="localhost", port=8080)
