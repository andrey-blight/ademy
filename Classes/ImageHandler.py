import io

from PIL import Image as PILImage


class ImageHandler:
    # TODO: Посмотреть поддерживаемые типы
    @staticmethod
    def get_bytes(image):
        image_jpg = PILImage.open(io.BytesIO(image.read()))  # Open image
        bite = io.BytesIO()
        image_jpg.save(bite, format="webp")  # Convert image to webp
        im_bytes = bite.getvalue()
        return im_bytes
