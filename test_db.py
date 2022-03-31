from data.db_session import global_init, create_session
from data.db_models import User, Image
from PIL import Image as PILImage
import io
from sqlalchemy.exc import OperationalError


def create_users():
    session = create_session()
    u1 = User(name="Andrey", surname="Kizhinov", age=17, sex=1, password="12djfefd", email="kizhinov05@gmail.com")
    u2 = User(name="Daria", surname="Lavrenteva", age=17, sex=2, password="eifavb", email="Daria@gmail.com")
    u3 = User(name="Vadim", surname="Dragan", age=16, sex=1, password="weqifl", email="Vadim@gmail.com")
    session.add_all([u1, u2, u3])
    session.commit()


def create_images():
    for i in range(1, 8):
        try:
            source = fr"test_images/{i}.jpg"
            image_jpg = PILImage.open(source)  # Open image
            bite = io.BytesIO()
            image_jpg.save(bite, format="webp")  # Convert image to webp
            im_bytes = bite.getvalue()
            session = create_session()
            db_img = Image(user_id=3, image=im_bytes)
            session.add(db_img)
            session.commit()
        except OperationalError as ex:
            print(ex.args[0].split("'")[1])


if __name__ == '__main__':
    global_init()
    create_images()
