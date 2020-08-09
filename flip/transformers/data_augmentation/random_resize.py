import cv2
import numpy as np

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class RandomResize(Transformer):
    """ Random Resize image of Element

        Parameters
        ----------
        mode: {'asymmetric', 'symmetric_w', 'symmetric_h'}, default='asymmetric'
        relation: {'alone', 'parent'}
        w_min: when mode='parent' w_min represent a percentage value related to the parent object
        w_max:
        h_min:
        h_max:

        if relation='parent'

        TODO:   asymmetric use w_min, w_max, h_min, h_max / pw_min, pw_max, ph_min, ph_max
                symmetric_w use w_min, w_max / pw_min, pw_max
                symmetric_h use h_min, h_max / ph_min, ph_max
    """
    _SUPPORTED_MODES = {'asymmetric', 'symmetric_w', 'symmetric_h', 'parent'}

    def __init__(
        self,
        mode='asymmetric',
        w_min=None,
        w_max=None,
        h_min=None,
        h_max=None,
    ):
        self.w_min = w_min
        self.w_max = w_max
        self.h_min = h_min
        self.h_max = h_max
        self.mode = mode

    def map(self, element: Element) -> Element:
        assert element, "Element cannot be None"

        w_min = self.w_min if self.w_min is not None else element.image.shape[1]
        h_min = self.h_min if self.h_min is not None else element.image.shape[0]
        w_max = self.w_max if self.w_max is not None else element.image.shape[1]
        h_max = self.h_max if self.h_max is not None else element.image.shape[0]

        if self.mode == 'symmetric_h':
            h = (
                h_min
                if h_min == h_max is not None
                else np.random.randint(low=h_min, high=h_max,)
            )
            w = element.image.shape[1] * (h / element.image.shape[0])
            w = int(w)
        elif self.mode == 'symmetric_w':
            w = (
                w_min
                if w_min == w_max is not None
                else np.random.randint(low=w_min, high=w_max,)
            )
            h = element.image.shape[0] * (w / element.image.shape[1])
            h = int(h)
        else:
            w = (
                w_min
                if w_min == w_max is not None
                else np.random.randint(low=w_min, high=w_max,)
            )

            h = (
                h_min
                if h_min == h_max is not None
                else np.random.randint(low=h_min, high=h_max,)
            )

        element.image = cv2.resize(element.image, (w, h))

        return element
