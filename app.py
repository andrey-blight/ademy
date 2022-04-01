from flask import Flask
from api import MainAPI

application = Flask(__name__)
application.config.from_object('config.DevConfig')


MainAPI(application)

if __name__ == '__main__':
    application.run(host='localhost', port=8080)
