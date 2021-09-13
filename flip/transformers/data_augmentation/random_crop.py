import numpy as np

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer

class RandomCrop(Transformer):
    '''
    x_min : Minimum cut percentage in x axis
    y_min : Minimum cut percentage in y axis
    '''
    def __init__(self, x_min=None, y_min=None, force=True):
        
        self.x_min = x_min
        self.y_min = y_min
        self.force = force
        
        if self.x_min!=None and self.y_min != None:
            self.mode = None
        else:
            self.mode = 'random'
        
    def map(self, element: Element, parent=None) -> Element:
        """ locate objects """
        assert element, "Element cannot be None"
        
        el_h: int = element.image.shape[0]
        el_w: int = element.image.shape[1]
        
        if self.force == False:
            if np.random.randint(low=0, high=2) == 0:
                if self.mode == 'random':
            
                    x = np.random.randint(0,el_w-el_w/5)
                    y = np.random.randint(0,el_h-el_h/5)
                    
                    h = np.random.randint(el_h/5,el_h)
                    w = np.random.randint(el_w/5,el_w)
                    
                    element.image = element.image[y:min(y+h,el_h),x:min(x+w,el_w),:]
                    
                else:
                    
                    x_min = (
                        (self.x_min if self.x_min <= 1 else (self.x_min % 100) / 100) * el_w
                        if self.x_min is not None
                        else 0
                    )
                    y_min = (
                        (self.y_min if self.y_min <= 1 else (self.y_min % 100) / 100) * el_h
                        if self.y_min is not None
                        else 0
                    )
                    
                    x = np.random.randint(0,el_w-x_min)
                    y = np.random.randint(0,el_h-y_min)
                    
                    h = np.random.randint(y_min,el_h)
                    w = np.random.randint(x_min,el_w)
                    
                    element.image = element.image[y:min(y+h,el_h),x:min(x+w,el_w),:]
        else:
            if self.mode == 'random':
        
                x = np.random.randint(0,el_w-el_w/5)
                y = np.random.randint(0,el_h-el_h/5)
                
                h = np.random.randint(el_h/5,el_h)
                w = np.random.randint(el_w/5,el_w)
                
                element.image = element.image[y:min(y+h,el_h),x:min(x+w,el_w),:]
                
            else:
                
                x_min = (
                    (self.x_min if self.x_min <= 1 else (self.x_min % 100) / 100) * el_w
                    if self.x_min is not None
                    else 0
                )
                y_min = (
                    (self.y_min if self.y_min <= 1 else (self.y_min % 100) / 100) * el_h
                    if self.y_min is not None
                    else 0
                )
                
                x = np.random.randint(0,el_w-x_min)
                y = np.random.randint(0,el_h-y_min)
                
                h = np.random.randint(y_min,el_h)
                w = np.random.randint(x_min,el_w)
                
                element.image = element.image[y:min(y+h,el_h),x:min(x+w,el_w),:]
            
        return element