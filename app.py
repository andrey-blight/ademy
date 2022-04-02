from api import MainAPI

from flask import Flask

application = Flask(__name__)
application.config.from_object("config.DevConfig")

MainAPI(application)

if __name__ == "__main__":
    application.run(host="localhost", port=8080)
