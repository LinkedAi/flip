import cv2
import numpy as np

from flip.transformers.constants import Flip
from flip.transformers.transformer import Transformer

from flip import parser


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
