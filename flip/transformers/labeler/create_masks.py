import numpy as np
import matplotlib.pyplot as plt

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
            x = element.tags[i]['pos']['x']
            y = element.tags[i]['pos']['y']
            w = obj.image.shape[1]
            h = obj.image.shape[0]
            # print(element.tags[i]['pos'])
            # print(obj.image.shape)
            # plt.imshow(obj.image)
            # plt.show()
            if y+h>masks.shape[0]:
                h = masks.shape[0]-y
                obj.image = obj.image[:h,:,:]
            if x+w>masks.shape[1]:
                w = masks.shape[1]-x
                obj.image = obj.image[:,:w,:]
            if i == 0:
                masks[y:y+h,x:x+w]+=np.logical_or(masks[y:y+h,x:x+w],obj.image[:,:,0])*(classes.index(element.tags[i]['name'])+1)/len(classes)
                continue
            inter = np.logical_and(masks[y:y+h,x:x+w],obj.image[:,:,0])
            for a,e in enumerate(inter):
                for b,j in enumerate(e):
                    if j ==True:
                        masks[y+a,x+b] = 0
            masks[y:y+h,x:x+w]+=np.logical_or(masks[y:y+h,x:x+w]*0,obj.image[:,:,0])*(classes.index(element.tags[i]['name'])+1)/len(classes)
        return masks