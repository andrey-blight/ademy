from data.db_session import global_init, create_session
from data.db_models import User, Image
from PIL import Image as PILImage
import io

global_init()

for i in range(1, 7):
    source = fr"test_images/{i}.jpg"
    destination = fr"test_images/{i}.webp"
    image = PILImage.open(source)  # Open image
    b = io.BytesIO()
    image.save(b, format="webp")  # Convert image to webp
    im_bytes = b.getvalue()
    if im_bytes.__sizeof__() < 55000:
        session = create_session()
        db_img = Image(user_id=1, image=im_bytes)
        session.add(db_img)
        session.commit()
