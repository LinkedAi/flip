import cv2
import numpy as np

from data_generator.transformers.constants import Flip
from data_generator.transformers.transformer import Transformer

from data_generator import parser


@parser.parseable
class Flip(Transformer):
    def __init__(self, mode: Flip = Flip.random):
        self.mode = mode

    def map(self, element: Element) -> Element:
        assert element, "Element cannot be None"

        if self.mode == Flip.x:
            dir = 0
        elif self.mode == Flip.y:
            dir = 1
        else:
            dir = np.random.randint(low=0, high=2)

        if np.random.randint(low=0, high=2) == 0:  # Flip if 0
            element.image = cv2.flip(element.image, dir)

        return element
