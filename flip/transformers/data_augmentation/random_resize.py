import cv2
import numpy as np

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class RandomResize(Transformer):
    """ Random Resize image of Element

        Parameters
        ----------
        mode: {'asymmetric', 'symmetric_w', 'symmetric_h'}, default='asymmetric'
        relation: {'none', 'parent'}
        w_min: when mode='parent' w_min represent a percentage value related to the parent object
        w_max:
        h_min:
        h_max:

        if relation='parent'

        TODO:   asymmetric use w_min, w_max, h_min, h_max / pw_min, pw_max, ph_min, ph_max
                symmetric_w use w_min, w_max / pw_min, pw_max
                symmetric_h use h_min, h_max / ph_min, ph_max
    """
    _SUPPORTED_MODES = {'asymmetric', 'symmetric_w', 'symmetric_h'}

    def __init__(
        self,
        mode='asymmetric',
        w_min=None,
        w_max=None,
        h_min=None,
        h_max=None,
        relation='none',
        w_percentage_min=None,
        w_percentage_max=None,
        h_percentage_min=None,
        h_percentage_max=None,
    ):
        self.w_min = w_min
        self.w_max = w_max
        self.h_min = h_min
        self.h_max = h_max
        self.mode = mode
        self.relation = relation
        self.w_percentage_min = w_percentage_min
        self.w_percentage_max = w_percentage_max
        self.h_percentage_min = h_percentage_min
        self.h_percentage_max = h_percentage_max

        if self.mode not in self._SUPPORTED_MODES:
            raise ValueError("Mode '{0:s}' not supported. ".format(self.mode))

        if self.mode not in self._SUPPORTED_MODES:
            raise ValueError("Relation '{0:s}' not supported. ".format(self.relation))

    def map(self, element: Element, parent=None) -> Element:
        assert element, "Element cannot be None"

        if self.relation == 'parent':
            p_shape = parent.image.shape

            w_min = p_shape[1] * self.w_percentage_min if self.w_percentage_min is not None else 0
            h_min = p_shape[0] * self.w_percentage_min if self.h_percentage_min is not None else 0
            w_max = p_shape[1] * self.w_percentage_min if self.w_percentage_max is not None else p_shape[1]
            h_max = p_shape[0] * self.w_percentage_min if self.h_percentage_max is not None else p_shape[0]
        else:
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
        elif self.mode == 'symmetric_w':
            w = (
                w_min
                if w_min == w_max is not None
                else np.random.randint(low=w_min, high=w_max,)
            )
            h = element.image.shape[0] * (w / element.image.shape[1])
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

        h = int(h)
        w = int(w)

        element.image = cv2.resize(element.image, (w, h))

        return element
