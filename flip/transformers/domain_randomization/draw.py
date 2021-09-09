import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer
from flip import utils


class Draw(Transformer):
    def map(self, element: Element) -> Element:
        image = element.image.copy()

        img = cv2.GaussianBlur(element.objects[0].image, (7, 7), 0)
        b, g, r, a = cv2.split(img)

        cimg = element.objects[0].image.copy()
        cimg[:, :, 3] = a

        for obj in element.objects:
            image = utils.overlay_transparent(
                background=image,
                overlay=obj.image[..., :-1],
                mask=obj.image[..., -1],
                x=obj.x,
                y=obj.y,
            )

        print("Image created")

        element.created_image = Element(image=image, name='created_final')

        return element
