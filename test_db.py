from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
from Data.Models.User import User
from Data.Models.Image import Image
from Data.Models.Interest import Interest
from sqlalchemy.exc import OperationalError
from faker import Faker
import random


def create_users():
    session = db.create_session()
    faker = Faker()
    users = []
    for i in range(10):
        user = User(name=faker.first_name(), surname=faker.last_name(),
                    age=random.randint(16, 80), sex=random.randint(1, 2),
                    password=faker.md5(raw_output=False), email=faker.email())
        users.append(user)
    session.add_all(users)
    session.commit()


def create_interests():
    session = db.create_session()
    i1 = Interest("sport")
    i2 = Interest("fishing")
    i3 = Interest("reading")
    session.add_all([i1, i2, i3])
    session.commit()


def create_images():
    session = db.create_session()
    for i in range(1, 10 + 1):
        user = session.query(User).get(i)
        db_img = Image(user_id=i,
                       image_href=r"static/user_images/test_image.jpg")
        user.images.append(db_img)
    session.commit()


if __name__ == '__main__':
    db = SqlAlchemyDatabase(create=True, delete=True)
    create_users()
    create_images()
    create_interests()
