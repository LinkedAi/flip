import numpy as np
import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer

class Color(Transformer):
    _SUPPORTED_MODES = {'hsv', 'lab', 'xyz', 'luv', 'gray', 'red', 'green', 'blue'}
    def __init__(self, color='gray'):
        self.color = color
        
        if self.color =='random':
            self.color = np.random.choice(list(self._SUPPORTED_MODES))
        
        if self.color not in self._SUPPORTED_MODES:
            raise ValueError("Color '{0:s}' not supported. ".format(self.mode))
    
    def map(self, element: Element, parent=None) -> Element:
        assert element, "Element cannot be None"
        
        if self.color == 'hsv':
            img = element.image.copy()
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2HSV)
            element.image = img
            return element
    
        if self.color == 'lab':
            img = element.image.copy()
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2LAB)
            element.image = img
            return element
    
        if self.color == 'xyz':
            img = element.image.copy()
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2XYZ)
            element.image = img
            return element
    
        if self.color == 'luv':
            img = element.image.copy()
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2LUV)
            element.image = img
            return element
    
        if self.color == 'gray':
            img = element.image.copy()
            img[:,:,:3] = cv2.cvtColor(cv2.cvtColor(element.image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)
            element.image = img
            return element
        
        if self.color == 'red':
            img = element.image.copy()
            img[:,:,1:3] = 0
            element.image = img
            return element
        
        if self.color == 'green':
            img = element.image.copy()
            img[:,:,0] = 0
            img[:,:,2:3] = 0
            element.image = img
            return element
        
        if self.color == 'blue':
            img = element.image.copy()
            img[:,:,0:2] = 0
            element.image = img
            return element

class Brightness(Transformer):
    def __init__(self, value=0):
        self.value = value
            
    def map(self, element: Element, parent=None) -> Element:
        img = element.image.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv = np.array(hsv, dtype = np.float64)
        hsv[:,:,1] = hsv[:,:,1]*self.value
        hsv[:,:,1][hsv[:,:,1]>255]  = 255
        hsv[:,:,2] = hsv[:,:,2]*self.value 
        hsv[:,:,2][hsv[:,:,2]>255]  = 255
        hsv = np.array(hsv, dtype = np.uint8)
        img[:,:,:3] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        element.image = img
        return element

class Contrast(Transformer):
    def __init__(self, value=0):
        self.value = value
            
    def map(self, element: Element, parent=None) -> Element:
        img = element.image.copy()
        lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        img[:,:,:3] = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        element.image = img
        return element
    
class Saturation(Transformer):
    def __init__(self, value=0):
        self.value = value
            
    def map(self, element: Element, parent=None) -> Element:
        img = element.image.copy()
        imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(imghsv)
        s = s*self.value
        s = np.clip(s,0,255)
        imghsv = cv2.merge([h,s,v])
        hsv = np.array(imghsv, dtype = np.uint8)
        img[:,:,:3] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        element.image = img
        return element