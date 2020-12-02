import numpy as np

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


# Only for element with objects
class ObjectsRandomPosition(Transformer):
    """ Set a random position to the objects of Element

        Parameters
        ----------
        mode : {'random', 'percentage'}, default='random'
        overlap : percentage 0 to 1, default=0
                  1 for allowing a complete overlap
                  0 for avoiding overlap
    """
    _SUPPORTED_MODES = {'random', 'percentage'}

    def __init__(
        self,
        mode='random',
        x_min=None,
        x_max=None,
        y_min=None,
        y_max=None,
        overlap=0
    ):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.overlap = overlap
        self.mode = mode

        if self.mode not in self._SUPPORTED_MODES:
            raise ValueError("Mode '{0:s}' not supported. ".format(self.mode))

    def makemask(self, masks, obj_h, obj_w, low_x, high_x, low_y, high_y,
                 el_h, el_w, factor):
        """ Set a mask

            Parameters
            ----------
            masks : list of masks. Every mask is a dictionary that stores
                    previous objects positions.
            obj_h : high of the new object to insert
            obj_w : width of the new object to insert
            low_x : min x allowed
            high_x : max x allowed
            low_y : min y allowed
            high_y : max y allowed
            el_h: background high
            el_w: background width
            factor: overlapping factor
                    percentage 0 - 1

            Return
            ------
            grid : completed mask
        """
        # create a base mask based on allowed limits

        grid = np.zeros((el_h, el_w))
        grid[low_y:high_y, low_x:high_x] = 1

        # iterate masks - construct and add new masks
        for m in masks:
            c_x = m['w'] / 2
            c_y = m['h'] / 2

            y1 = int(m['y'] + (1 - factor) * c_y)
            x1 = int(m['x'] + (1 - factor) * c_x)
            y2 = int(m['y'] + m['h'] - (1 - factor) * c_y)
            x2 = int(m['x'] + m['w'] - (1 - factor) * c_x)

            y_a = max(0, y1 - obj_h)
            x_a = max(0, x1 - obj_w)
            grid[y_a:y2, x_a:x2] = 0

        return grid

    def map(self, element: Element) -> Element:
        """ locate objects """
        assert element, "Element cannot be None"

        el_h: int = element.image.shape[0]
        el_w: int = element.image.shape[1]

        if self.mode == 'percentage':
            x_min = (
                (self.x_min if self.x_min <= 1 else (self.x_min % 100) / 100) * el_w
                if self.x_min is not None
                else 0
            )
            x_max = (
                (self.x_max if self.x_max <= 1 else (self.x_max % 100) / 100) * el_w
                if self.x_max is not None
                else el_w
            )
            y_min = (
                (self.y_min if self.y_min <= 1 else (self.y_min % 100) / 100) * el_h
                if self.y_min is not None
                else 0
            )
            y_max = (
                (self.y_max if self.y_max <= 1 else (self.y_max % 100) / 100) * el_h
                if self.y_max is not None
                else el_h
            )
        else:
            x_min = self.x_min if self.x_min is not None else 0
            x_max = self.x_max if self.x_max is not None else el_w
            y_min = self.y_min if self.y_min is not None else 0
            y_max = self.y_max if self.y_max is not None else el_h

        masks = []
        for obj in element.objects:
            # object dimension

            obj_h: int = int(obj.image.shape[0])
            obj_w: int = int(obj.image.shape[1])

            # max and min limits for the object with respect to the background
            low_x = int(max(0, x_min))
            high_x = int(min(x_max, el_w - obj_w))
            low_y = int(max(0, y_min))
            high_y = int(min(y_max, el_h - obj_h))

            # overlapping percentage
            factor = self.overlap

            # index_av stores available positions to place the object
            index_av = []

            # find positions to place the object
            # if there is not space the overlapping is increased
            while len(index_av) == 0 and factor < 1:
                factor += 0.1
                params = [masks, obj_h, obj_w, low_x,
                          high_x, low_y, high_y, el_h, el_w, factor]
                grid_available = self.makemask(*params)
                index_av = np.argwhere(grid_available)

            # if despite increasing overlapping there is not space
            # the limits are moved based on a new factor
            factor = 0
            while len(index_av) == 0:
                if high_y == (el_h - obj_h) and high_x == (el_w - obj_w):
                    # when the object doesn't have an available space
                    # despite changing overlapping and limits
                    # the complete background is available
                    index_av = np.argwhere(np.ones((el_h, el_w)))
                low_x = int(max(0, x_min - factor))
                high_x = int(min(x_max + factor, (el_w - obj_w)))
                low_y = int(max(0, y_min - factor))
                high_y = int(min(y_max + factor, el_h - obj_h))
                grid_available = np.zeros((el_h, el_w))
                grid_available[low_y:high_y, low_x:high_x] = 1
                index_av = np.argwhere(grid_available)
                factor += 1

            # random index
            index = np.random.choice(index_av.shape[0])
            obj.y, obj.x = int(index_av[index][0]), int(index_av[index][1])
            # save mask for the inserted object
            masks.append({'x': obj.x, 'y': obj.y, 'w': obj_w, 'h': obj_h})

        return element
