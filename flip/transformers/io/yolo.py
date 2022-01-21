import os
import warnings
from typing import Optional, List

warnings.simplefilter('always', UserWarning)

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class CreateYOLO(Transformer):
    def __init__(self, out_dir: str, name: str = None, classes: Optional[List[str]] = None):
        self.out_dir = out_dir
        self.name = name
        self.classes = classes

    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        txt_path = os.path.join(self.out_dir, f"{self.name}.txt")

        with open(txt_path, "w") as f:
            if element.tags is not None:
                bh = element.image.shape[0]
                bw = element.image.shape[1]
                for tag in element.tags:
                    xc = max(0, min(1, (tag["pos"]["x"] + tag["pos"]["w"]/2) / bw))
                    yc = max(0, min(1, (tag["pos"]["y"] + tag["pos"]["h"]/2) / bh))
                    w = max(0, min(1, round(tag["pos"]["w"] / bw, 2)))
                    h = max(0, min(1, round(tag["pos"]["h"] / bh, 2)))

                    f.write(f'{tag.get("name", 0)} {xc} {yc} {w} {h}\n')
            else:
                warnings.warn('There are no bounding boxes')
        return element
