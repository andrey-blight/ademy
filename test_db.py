import os.path

from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase, SqlAlchemyBase

from data.models.User import User
from data.models.Image import Image
from data.models.Interests import Interest
from PIL import Image as PILImage
import io
from sqlalchemy.exc import OperationalError


def create_users():
    session = db.create_session()
    u1 = User(name="Andrey", surname="Kizhinov", age=17, sex=1, password="12djfefd", email="kizhinov05@gmail.com")
    u2 = User(name="Daria", surname="Lavrenteva", age=17, sex=2, password="eifavb", email="Daria@gmail.com")
    u3 = User(name="Vadim", surname="Dragan", age=16, sex=1, password="weqifl", email="Vadim@gmail.com")
    session.add_all([u1, u2, u3])
    session.commit()


def create_interests():
    session = db.create_session()
    u1 = session.query(User).get(1)
    u2 = session.query(User).get(2)
    u3 = session.query(User).get(3)
    i1 = Interest("sport")
    i2 = Interest("fishing")
    i3 = Interest("reading")
    session.add_all([i1, i2, i3])
    u1.interests.append(i1)
    u1.interests.append(i3)
    u2.interests.append(i2)
    u2.interests.append(i3)
    u3.interests.append(i1)
    session.commit()


def create_images():
    for i in range(1, 8):
        try:
            source = fr"test_images/{i}.jpg"
            image_jpg = PILImage.open(source)  # Open image
            bite = io.BytesIO()
            image_jpg.save(bite, format="webp")  # Convert image to webp
            im_bytes = bite.getvalue()
            session = db.create_session()
            db_img = Image(user_id=3, image=im_bytes)
            u3 = session.query(User).get(3)
            u3.images.append(db_img)
            # session.add(db_img)
            session.commit()
        except OperationalError as ex:
            print(ex.args[0].split("'")[1])


if __name__ == '__main__':
    db = SqlAlchemyDatabase()
    session = db.create_session()
    print(session.query(User).all())
