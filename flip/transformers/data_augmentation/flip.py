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

    def __init__(self, mode='random', force=True):
        self.mode = mode
        self.force = force

        if self.mode not in self._SUPPORTED_MODES:
            raise ValueError("Mode '{0:s}' not supported. ".format(self.mode))

    def map(self, element: Element, parent=None) -> Element:
        assert element, "Element cannot be None"
        
        if self.force == False:
            if np.random.randint(low=0, high=2) == 0:
                self.force = True

        if self.mode == 'x':
            direction = 0
        elif self.mode == 'y':
            direction = 1
        else:
            direction = np.random.randint(low=0, high=2)

        if self.force == True:
            element.image = cv2.flip(element.image, direction)

        return element
