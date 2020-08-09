import os

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class CreateCSV(Transformer):
    def __init__(self, out_dir: str, name: str = None):
        self.out_dir = out_dir
        self.name = name

    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        csv_path = os.path.join(self.out_dir, f"{self.name}.csv")
        csv_data = ""

        for tag in element.tags:
            csv_data += f"{tag['name']},{tag['pos']['x']},{tag['pos']['y']},{tag['pos']['w']},{tag['pos']['h']}\n"

        with open(csv_path, mode="w") as f:
            f.write(csv_data)

        return element

