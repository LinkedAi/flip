import numpy as np

from data_generator.transformers.constants import Rotation
from data_generator.transformers.transform import Transformer
from data_generator.transformers.utils import rotate_bound


class Rotate(Transformer):
    def __init__(self, mode: Rotation = Rotation.random, min=0, max=0):
        self.mode = mode
        if self.mode == Rotation.upside_down:
            self.angles = [0, 180]
        elif self.mode == Rotation.ninety:
            self.angles = [0, 90, 180, 270]
        else:
            self.angles = [min, max]

    def map(self, element: Element) -> Element:
        assert element, "Element cannot be None"

        if self.mode == Rotation.upside_down or self.mode == Rotation.ninety:
            angle = np.random.choice(self.angles)
        else:
            angle = np.random.uniform(low=self.angles[0], high=self.angles[1],)

        element.image = rotate_bound(element.image, angle)

        return element
