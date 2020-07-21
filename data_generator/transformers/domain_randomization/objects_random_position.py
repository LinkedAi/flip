import numpy as np

from data_generator.transformers.constants import Position
from data_generator.transformers.transform import Transformer


# Only for element with objects
class ObjectsRandomPosition(Transformer):
    def __init__(
        self,
        mode: Position = Position.random,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
    ):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.mode = mode

    def map(self, element: Element) -> Element:
        assert element, "Element cannot be None"

        el_h: int = element.image.shape[0]
        el_w: int = element.image.shape[1]

        if self.mode == Position.percentage:
            xmin = (
                (self.xmin if self.xmin <= 1 else (self.xmin % 100) / 100) * el_w
                if self.xmin is not None
                else 0
            )
            xmax = (
                (self.xmax if self.xmax <= 1 else (self.xmax % 100) / 100) * el_w
                if self.xmax is not None
                else el_w
            )
            ymin = (
                (self.ymin if self.ymin <= 1 else (self.ymin % 100) / 100) * el_h
                if self.ymin is not None
                else 0
            )
            ymax = (
                (self.ymax if self.ymax <= 1 else (self.ymax % 100) / 100) * el_h
                if self.ymax is not None
                else el_h
            )
        else:
            xmin = self.xmin if self.xmin is not None else 0
            xmax = self.xmax if self.xmax is not None else el_w
            ymin = self.ymin if self.ymin is not None else 0
            ymax = self.ymax if self.ymax is not None else el_h

        lastx, lasty = 0, 0
        for obj in element.objects:
            obj_h: int = int(obj.image.shape[0])
            obj_w: int = int(obj.image.shape[1])

            while True:
                obj.x = np.random.randint(
                    low=max(0, xmin - obj_w / 2), high=min(xmax, el_w),
                )

                if obj.x > lastx + obj_w / 2 or obj.x < lastx - obj_w / 2:
                    break

            while True:
                obj.y = np.random.randint(
                    low=max(0, ymin - obj_h / 2), high=min(ymax, el_h),
                )

                if obj.y > lasty + obj_h / 2 or obj.y < lasty - obj_h / 2:
                    break

            lastx, lasty = obj.x, obj.y

        return element
