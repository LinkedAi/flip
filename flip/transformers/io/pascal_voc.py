import os
import json

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class PascalVoc(Transformer):
    def __init__(self, out_dir: str, name: str = None):
        self.out_dir = out_dir
        self.name = name

    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        xml_path = os.path.join(self.out_dir, f"{self.name}.json")
        xml_data = json.dumps(element.tags)

        with open(json_path, mode="w") as f:
            f.write(json_data)

        return element

