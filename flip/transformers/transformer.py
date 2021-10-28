import typing as tp
import warnings

import flip
from flip import parser
from flip.transformers.element import Element

warnings.simplefilter('always', UserWarning)
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

warnings.formatwarning = custom_formatwarning

class Transformer:
    @classmethod
    def parse(cls, **kwargs):
        return cls(**kwargs)

    def __call__(self, elements=None) -> tp.Iterable[Element]:
        assert hasattr(self, "map") != hasattr(self, "process")

        if elements is None:
            elements = ()
        elif isinstance(elements, Element):
            elements = (elements,)

        if hasattr(self, "map"):
            for element in elements:

                elements = self.map(element)

                if isinstance(elements, Element):
                    yield elements
                else:
                    yield from elements

        else:
            yield from self.process(elements)

    def __or__(self, other):
        return Compose([self, other])


@parser.parseable
class Compose(Transformer):
    @classmethod
    def parse(cls, transformers):

        transformers = [parser.parse(transformer) for transformer in transformers]

        return cls(transformers)

    def __init__(self, transformers: tp.List[Transformer]):

        final_transformers = []

        for transformer in transformers:
            if isinstance(transformer, Compose):
                final_transformers += transformer.transformers
            else:
                final_transformers.append(transformer)

        self.transformers = final_transformers

    def process(self, elements: tp.Iterable[Element]) -> tp.Iterable[Element]:

        for transformer in self.transformers:
            elements = transformer(elements)

        return elements


@parser.parseable
class ApplyToObjects(Transformer):
    def __init__(self, transforms: tp.List[Transformer]):
        if hasattr(transforms, "__iter__"):
            self.transforms = transforms
        else:
            self.transforms = [transforms]

    def map(self, element: Element) -> Element:
        for obj in element.objects:
            for system in self.transforms:
                if type(system) == flip.transformers.domain_randomization.Draw or type(system) == flip.transformers.domain_randomization.ObjectsRandomPosition:
                    warnings.warn('{}. This transformer is not allowed for the object image.'.format(type(system)))
                    continue
                obj = system.map(obj, parent=element)
        return element

@parser.parseable
class ApplyToBackground(Transformer):
    def __init__(self, transforms: tp.List[Transformer]):
        if hasattr(transforms, "__iter__"):
            self.transforms = transforms
        else:
            self.transforms = [transforms]

    def map(self, element: Element) -> Element:
        for system in self.transforms:
            if type(system) == flip.transformers.domain_randomization.Draw or type(system) == flip.transformers.domain_randomization.ObjectsRandomPosition:
               warnings.warn(f'{type(system)}. This transformer is not allowed for the background image.')
               continue
            element = system.map(element, parent=element)
        return element
    
@parser.parseable
class ApplyToCreatedImage(Transformer):
    def __init__(self, transforms: tp.List[Transformer]):
        if hasattr(transforms, "__iter__"):
            self.transforms = transforms
        else:
            self.transforms = [transforms]

    def map(self, element: Element) -> Element:
        for system in self.transforms:
            if type(system) == flip.transformers.data_augmentation.Rotate or type(system) == flip.transformers.domain_randomization.Draw or type(system) == flip.transformers.domain_randomization.ObjectsRandomPosition or type(system) == flip.transformers.data_augmentation.RandomCrop or type(system) == flip.transformers.data_augmentation.Flip or type(system) == flip.transformers.data_augmentation.RandomResize:
               warnings.warn(str(type(system))+' This transformer is not allowed for the created image.')
               continue
            element.created_image = system.map(element.created_image, parent=element)
        return element