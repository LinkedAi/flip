import cv2
import numpy as np

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer

from flip import parser


@parser.parseable
class Flip(Transformer):
    """ Flip image of Element

        Parameters
        ----------
        mode : {'random', 'x', 'y'}, default='random'
    """
    _SUPPORTED_MODES = {'random', 'x', 'y'}

    def __init__(self, mode='random'):
        self.mode = mode

        if self.mode not in self._SUPPORTED_MODES:
            raise ValueError("Mode '{0:s}' not supported. ".format(self.mode))

    def map(self, element: Element, parent=None) -> Element:
        assert element, "Element cannot be None"

        if self.mode == 'x':
            direction = 0
        elif self.mode == 'y':
            direction = 1
        else:
            direction = np.random.randint(low=0, high=2)

        if np.random.randint(low=0, high=2) == 0:  # Flip if 0
            element.image = cv2.flip(element.image, direction)

        return element
