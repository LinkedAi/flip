import numpy as np
import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class CreateMasks(Transformer):
    def __init__(self, classes=[]):
        self.classes = classes
    
    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        element.masks = self.create(element)

        return element

    def create(self, element):
        masks = np.zeros((element.created_image.shape[0],element.created_image.shape[1]))
        classes = self.classes
        
        for i, obj in enumerate(element.objects):
            # Find mask object position
            x = obj.x
            y = obj.y
            w = obj.image.shape[1]
            h = obj.image.shape[0]
            if x>=element.created_image.shape[1] or y>=element.created_image.shape[0]:
                continue
            if y+h>masks.shape[0]:
                h = masks.shape[0]-y
                obj.image = obj.image[:h,:,:]
            if x+w>masks.shape[1]:
                w = masks.shape[1]-x
                obj.image = obj.image[:,:w,:]
            
            # Create the first mask
            obje = cv2.cvtColor(obj.image, cv2.COLOR_BGR2GRAY)
            if i == 0:
                masks[y:y+h,x:x+w]+=np.logical_or(masks[y:y+h,x:x+w],obje)*(classes.index(obj.name)+1)
                continue
            # Delete the intersection between objects
            
            inter = np.logical_and(masks[y:y+h,x:x+w],obje)
            for a,e in enumerate(inter):
                for b,j in enumerate(e):
                    if j ==True:
                        masks[y+a,x+b] = 0
            # Place the final object mask
            masks[y:y+h,x:x+w]+=np.logical_or(masks[y:y+h,x:x+w]*0,obje)*(classes.index(obj.name)+1)
        return masks