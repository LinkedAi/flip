import numpy as np
import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer

class Color(Transformer):
    _SUPPORTED_MODES = {'hsv', 'lab', 'xyz', 'luv', 'gray', 'red', 'green', 'blue',
                        'purple', 'yellow', 'cyan'}
    def __init__(self, color='random', force=True):
        self.color = color
        self.force = force
        
        if self.color =='random':
            self.color = np.random.choice(list(self._SUPPORTED_MODES))
        
        if self.color not in self._SUPPORTED_MODES:
            raise ValueError("Color '{0:s}' not supported. ".format(self.color))
    
    def map(self, element: Element, parent=None) -> Element:
        assert element, "Element cannot be None"
        
        img = element.image.copy()
        if self.force == False:
            if np.random.randint(low=0, high=2) == 0:
                self.force = True
        
        if self.color == 'hsv' and self.force == True:
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2HSV)
    
        if self.color == 'lab' and self.force == True:
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2LAB)
            
        if self.color == 'xyz' and self.force == True:
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2XYZ)
            
        if self.color == 'luv' and self.force == True:
            img[:,:,:3] = cv2.cvtColor(element.image, cv2.COLOR_BGR2LUV)
            
        if self.color == 'gray' and self.force == True:
            img[:,:,:3] = cv2.cvtColor(cv2.cvtColor(element.image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)

        if self.color == 'red' and self.force == True:
            img[:,:,1:3] = 0
            
        if self.color == 'green' and self.force == True:
            img[:,:,0] = 0
            img[:,:,2:3] = 0
            
        if self.color == 'blue' and self.force == True:
            img[:,:,0:2] = 0
            
        if self.color == 'purple' and self.force == True:
            img[:,:,1] = 0
            
        if self.color == 'yellow' and self.force == True:
            img[:,:,2] = 0
            
        if self.color == 'cyan' and self.force == True:
            img[:,:,0] = 0
            
        element.image = img
        
        return element
        
class Brightness(Transformer):
    def __init__(self, value=1, force=True):
        self.value = value
        self.force = force
            
    def map(self, element: Element, parent=None) -> Element:
        
        if self.force == False:
            if np.random.randint(low=0, high=2) == 0:
                self.force = True
        
        if self.force == True:
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
    def __init__(self, value=1, force=True):
        self.value = value
        self.force = force
            
    def map(self, element: Element, parent=None) -> Element:
        
        if self.force == False:
            if np.random.randint(low=0, high=2) == 0:
                self.force = True
                
        if self.force==True:
            img = element.image.copy()
            img[:,:,:3] = cv2.addWeighted(img[:,:,:3], self.value, np.zeros((img.shape[0],img.shape[1],3), img.dtype), 0, 0)
            element.image = img
        return element
    
class Saturation(Transformer):
    def __init__(self, value=1, force=True):
        self.value = value
        self.force = force
            
    def map(self, element: Element, parent=None) -> Element:
        
        if self.force == False:
            if np.random.randint(low=0, high=2) == 0:
                self.force = True
                
        if self.force == True:
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