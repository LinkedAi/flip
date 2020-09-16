import os
import json

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class CreatePascalVoc(Transformer):
    def __init__(self, out_dir: str, name: str = None):
        self.out_dir = out_dir
        self.name = name

    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        xml_path = os.path.join(self.out_dir, f"{self.name}.xml")

        x = self.out_dir.split('/')
        folder = x[len(x)-1]

        f = open(xml_path, "w")
        f.write("")
        f.close()

        f = open(xml_path, "a")
        f.write("<annotation>\n")
        f.write("	<folder>{}</folder>\n".format(folder))
        f.write("	<filename>{}.jpg</filename>\n".format(self.name))
        f.write("	<path>{}/{}.jpg</path>\n".format(self.out_dir, self.name))
        f.write("	<source>\n")
        f.write("		<database>Unknown</database>\n")
        f.write("	</source>\n")
        f.write("	<size>\n")
        f.write("		<width>{}</width>\n".format(element.created_image.shape[1]))
        f.write("		<height>{}</height>\n".format(element.created_image.shape[0]))
        f.write("		<depth>{}</depth>\n".format(element.created_image.shape[2]))
        f.write("	</size>\n")
        f.write("	<segmented>0</segmented>\n")

        for tag in element.tags:
            x_min = int(tag['pos']['x'])
            y_min = int(tag['pos']['y'])
            x_max = x_min + int(tag['pos']['w'])
            y_max = y_min + int(tag['pos']['h'])

            f.write("	<object>\n")
            f.write("		<name>{}</name>\n".format(tag['name']))
            f.write("		<pose>Unspecified</pose>\n")
            f.write("		<truncated>0</truncated>\n")
            f.write("		<difficult>0</difficult>\n")
            f.write("		<bndbox>\n")
            f.write("			<xmin>{}</xmin>\n".format(x_min))
            f.write("			<ymin>{}</ymin>\n".format(y_min))
            f.write("			<xmax>{}</xmax>\n".format(x_max))
            f.write("			<ymax>{}</ymax>\n".format(y_max))
            f.write("		</bndbox>\n")
            f.write("	</object>\n")
        f.write("</annotation>\n")
        f.close()

        return element

