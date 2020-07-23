import cv2

from data_generator.transformers.element import Element
from data_generator.transformers.transformer import Transformer
from data_generator.transformers import utils


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

        # plt.imshow(image)
        # plt.show()
        # print("Image created")

        element.fimg = image

        return element
