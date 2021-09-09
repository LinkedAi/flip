import numpy as np
import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer

class Noise(Transformer):
    _SUPPORTED_MODES = {'gaussian_blur', 'avg_blur', 'median_blur', 'salt_pepper'}
    def __init__(self, noise = 'gray', value = 0.5):
        self.noise = noise
        self.value = value
        
        if self.noise =='random':
            self.noise = np.random.choice(list(self._SUPPORTED_MODES))
        
        if self.noise not in self._SUPPORTED_MODES:
            raise ValueError("Noise '{0:s}' not supported. ".format(self.mode))
    
    def map(self, element: Element, parent=None) -> Element:
        assert element, "Element cannot be None"
        
        if self.noise == 'gaussian_blur':
            img = element.image.copy()
            img[:,:,:3] = cv2.GaussianBlur(element.image, (5,5), self.value)[:,:,:3]
            element.image = img
            return element
    
        if self.noise == 'avg_blur':
            img = element.image.copy()
            img1 = cv2.blur(element.image, (5,5))
            img[:,:,:3]= img1[:,:,:3]
            element.image = img
            return element
    
        if self.noise == 'median_blur':
            img = element.image.copy()
            img[:,:,:3] = cv2.medianBlur(element.image, self.value)[:,:,:3]
            element.image = img
            return element
    
        if self.noise == 'salt_pepper':
            img = element.image.copy()
            img1 = img[:,:,:3]
            #salt
            num_salt = np.ceil(self.value*img1.size*0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt))
                      for i in img1.shape]
            
            img1[coords[0],coords[1],:] = 255
        
            #pepper
            num_pepper = np.ceil(self.value*img1.size*0.5)
            coords = [np.random.randint(0, i - 1, int(num_pepper))
                      for i in img1.shape]
            #coords = [list(a) for a in zip(list(coords[0]), list(coords[1]))]
            img1[coords[0],coords[1],:] = 0
            img[:,:,:3] = img1
            element.image = img1
            return element