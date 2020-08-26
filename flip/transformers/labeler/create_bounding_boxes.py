import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class CreateBoundingBoxes(Transformer):
    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        element.tags = self.create(element)

        return element

    def create(self, element):
        array = []
        for obj in element.objects:
            new_x, new_y, new_w, new_h = self.bounding_box(obj.image)
            data = {"name": obj.name, "pos": {}}
            data["pos"]["x"] = (obj.x or 0) + new_x
            data["pos"]["y"] = (obj.y or 0) + new_y
            data["pos"]["w"] = new_w
            data["pos"]["h"] = new_h

            array.append(data)

        return array

    def bounding_box(self, image):
        """
        Args:
          image: image to process its width and height
        Description:
          This function
        Returns:
        """

        # Canny edge detection - edge gradient
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_filtered = cv2.bilateralFilter(img_gray, 7, 50, 50)
        edged = cv2.Canny(gray_filtered, 60, 120)
        edges_filtered = cv2.Canny(edged, 60, 120)

        # Morphological Transformations
        # applying closing function
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(edges_filtered, cv2.MORPH_CLOSE, kernel)

        # Finding_contours
        (cnts, _) = cv2.findContours(
            closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        x1, x2 = img_gray.shape[1], 0
        y1, y2 = img_gray.shape[0], 0
        for c in cnts:

            x, y, w, h = cv2.boundingRect(c)

            if x < x1:
                x1 = x
            if y < y1:
                y1 = y
            if x+w > x2:
                x2 = x+w
            if y+h > y2:
                y2 = y+h

        # new_img = image[y1: y2, x1: x2]

        return x1, y1, x2, y2
