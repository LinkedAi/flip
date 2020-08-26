import numpy as np

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer
from flip.utils import rotate_bound, crop_from_contour

class Rotate(Transformer):
    """ Flip image of Element

        Parameters
        ----------
        mode : {'random', '90', 'upside_down'}, default='random'
    """

    _SUPPORTED_MODES = {'random', '90', 'upside_down'}

    def __init__(self, mode='random', min=0, max=360):
        self.mode = mode

        if self.mode not in self._SUPPORTED_MODES:
            raise ValueError("Mode '{0:s}' not supported. ".format(self.mode))

        if self.mode == 'upside_down':
            self.angles = [0, 180]
        elif self.mode == '90':
            self.angles = [0, 90, 180, 270]
        else:
            self.angles = [min, max]

    def map(self, element: Element, parent=None) -> Element:
        assert element, "Element cannot be None"

        if self.mode == 'upside_down' or self.mode == 'ninety':
            angle = np.random.choice(self.angles)
        else:
            angle = np.random.uniform(low=self.angles[0], high=self.angles[1],)

        element.image = rotate_bound(element.image, angle)
        element.image = crop_from_contour(element.image)

        return element
