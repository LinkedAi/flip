import numpy as np
import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer

class CutOut(Transformer):
    _SUPPORTED_FIGURES = {'rectangle', 'circle', 'square', 'triangle'}
    _SUPPORTED_COLOR = {'red', 'green', 'blue', 'black', 'white'}
    _SUPPORTED_MODES = {'random', 'percentage'}
    
    def __init__(self, figure = 'rectangle', color='black', mode='random',
                 x_min=None, x_max=None, y_min=None, y_max=None,
                 crop_shape=(None,None), num=1, force=True):
        
        self.figure = figure
        self.color = color
        self.mode = mode
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.w, self.h = crop_shape
        self.num = num
        self.force = force
        
        if self.mode not in self._SUPPORTED_MODES:
            raise ValueError("Noise '{0:s}' not supported. ".format(self.mode))
        if self.figure not in self._SUPPORTED_FIGURES:
            raise ValueError("Noise '{0:s}' not supported. ".format(self.figure))
        if self.color not in self._SUPPORTED_COLOR:
            raise ValueError("Noise '{0:s}' not supported. ".format(self.color))
        
    
    
    def map(self, element: Element, parent=None) -> Element:
        """ locate objects """
        assert element, "Element cannot be None"

        el_h: int = element.image.shape[0]
        el_w: int = element.image.shape[1]
        mask = np.zeros((el_h,el_w,3))
        
        if self.w == None and self.h != None:
            self.w = np.random.randint(1,self.h)
        if self.h == None and self.w != None:
            self.h = np.random.randint(1,self.w)
        if self.w == None and self.h == None:
            self.w = np.random.randint(1,el_w/2)
            self.h = np.random.randint(1,el_h/2)
        
        if self.mode == 'percentage':
            x_min = (
                (self.x_min if self.x_min <= 1 else (self.x_min % 100) / 100) * el_w
                if self.x_min is not None
                else 0
            )
            x_max = (
                (self.x_max if self.x_max <= 1 else (self.x_max % 100) / 100) * el_w
                if self.x_max is not None
                else el_w
            )
            y_min = (
                (self.y_min if self.y_min <= 1 else (self.y_min % 100) / 100) * el_h
                if self.y_min is not None
                else 0
            )
            y_max = (
                (self.y_max if self.y_max <= 1 else (self.y_max % 100) / 100) * el_h
                if self.y_max is not None
                else el_h
            )
        else:
            x_min = self.x_min if self.x_min is not None else 0
            x_max = self.x_max if self.x_max is not None else el_w
            y_min = self.y_min if self.y_min is not None else 0
            y_max = self.y_max if self.y_max is not None else el_h
        
        if self.color == 'red':
            RGB = (255,0,0)
        if self.color == 'green':
            RGB = (0,255,0)
        if self.color == 'blue':
            RGB = (0,0,255)
        if self.color == 'black':
            RGB = (0,0,0)
        if self.color == 'white':
            RGB = (255,255,255)
        
        for n in range(self.num):
            x = np.random.randint(x_min, x_max)
            y = np.random.randint(y_min, y_max)
            if self.force == False:
                if np.random.randint(low=0, high=2) == 0:
                    self.force = True
                    
            if self.figure == 'rectangle' and self.force==True:            
                img = element.image.copy()
                #element.image[:,:,:3] = cv2.rectangle(img, (x,y), (x+self.w,y+self.h), RGB, -1)[:,:,:3]
                element.image = cv2.rectangle(img, (x,y), (x+self.w,y+self.h), RGB, -1)
                if element.name == 'created_final':
                    mask = cv2.rectangle(mask, (x,y), (x+self.w,y+self.h), RGB, -1)
                    
            
            if self.figure == 'circle' and self.force==True:            
                element.image = cv2.circle(element.image, (x,y), min(self.w,self.h), RGB, -1)
                if element.name == 'created_final':
                    mask = cv2.circle(mask, (x,y), min(self.w,self.h), RGB, -1)
                    
                
            if self.figure == 'square' and self.force==True:            
                element.image = cv2.rectangle(element.image, (x,y), (x+min(self.w,self.h),y+min(self.w,self.h)), RGB, -1)
                if element.name == 'created_final':
                    mask = cv2.rectangle(mask, (x,y), (x+min(self.w,self.h),y+min(self.w,self.h)), RGB, -1)
                    
                
            if self.figure == 'triangle' and self.force==True:
                vertices = np.array([[x, y], 
                                     [x+self.w, y], 
                                     [int((x+self.w)/2), y+self.h]], np.int32)
                pts = vertices.reshape((-1, 1, 2))
                element.image = cv2.fillPoly(element.image, [pts], color=RGB)
                if element.name == 'created_final':
                    mask = cv2.fillPoly(mask, [pts], color=RGB)
                    
        mask = cv2.cvtColor(mask.astype('float32'), cv2.COLOR_RGB2GRAY)
        element.cut_out = Element(image=mask)
        return element