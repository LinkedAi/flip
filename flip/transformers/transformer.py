import typing as tp

from flip import parser
from flip.transformers.element import Element


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
                obj = system.map(obj, parent=element)
        return element
