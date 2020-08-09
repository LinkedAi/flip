import os
import cv2
import numpy as np

from flip.transformers.transformer import Transformer
from flip.transformers.element import Element
from flip import utils


class SaveImage(Transformer):
    def __init__(self, out_dir: str, name: str = None):
        self.out_dir = out_dir
        self.name = name

    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        if self.name is None:
            self.name = "f%d" % np.random.randint(0, 5000)

        element.name = self.name
        image_path = os.path.join(
            self.out_dir, f"{self.name}.jpg"
        )  # "{self.name}.{extension}"

        image = utils.inv_channels(element.created_image)
        cv2.imwrite(image_path, image)

        return element
