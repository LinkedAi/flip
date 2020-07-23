import typing as tp

import cytoolz as cz

import data_generator.transformers as tr
from data_generator import parser


@parser.parseable
class Increment(tr.Transformer):
    def __init__(self, inc=1):
        self.inc = inc

    def map(self, element: tr.Element) -> tr.Element:

        if element.x is None:
            element.x = self.inc
        else:
            element.x += self.inc

        return element


class Range(tr.Transformer):
    def __init__(self, n):
        self.n = n

    def process(self, elements: tp.Iterable[tr.Element]) -> tp.Iterable[tr.Element]:
        for i in range(self.n):
            yield tr.Element(x=i)


class Take(tr.Transformer):
    def __init__(self, n):
        self.n = n

    def process(self, elements: tp.Iterable[tr.Element]) -> tp.Iterable[tr.Element]:
        return cz.take(self.n, elements)


class TestTransformer:
    def test_basic(self):

        transformer = Increment()
        element = tr.Element()

        assert element.x is None

        [element] = transformer(element)

        assert element.x == 1

    def test_compose(self):

        transformer = tr.Compose([Increment(), Increment()])
        element = tr.Element()

        assert element.x is None

        [element] = transformer(element)

        assert element.x == 2

    def test_compose_pipe(self):

        transformer = Increment() | Increment()

        element = tr.Element()

        assert isinstance(transformer, tr.Compose)
        assert element.x is None

        [element] = transformer(element)

        assert element.x == 2

    def test_compose_flatten(self):

        transformer = (
            Increment()
            | Increment()
            | Increment()
            | tr.Compose([Increment(), tr.Compose([Increment(), Increment()])])
        )

        assert isinstance(transformer, tr.Compose)
        assert len(transformer.transformers) == 6
        assert all(
            not isinstance(transformer, tr.Compose)
            for transformer in transformer.transformers
        )

    def test_range(self):

        transformer = Range(5)

        n = 0
        for i, element in enumerate(transformer()):
            n += 1

            assert element.x == i

        assert n == 5

    def test_iterable(self):

        transformer = Range(5) | Increment()

        elements = transformer()

        assert not isinstance(elements, (tr.Transformer, list))

        n = 0

        for i, element in enumerate(elements):
            n += 1
            assert element.x == i + 1

        assert n == 5

    def test_iterable_composition(self):

        transformer = Range(5) | Take(3) | Increment()

        elements = transformer()

        assert not isinstance(elements, (tr.Transformer, list))

        n = 0

        for i, element in enumerate(elements):
            n += 1
            assert element.x == i + 1

        assert n == 3

    def test_parse(self):

        structure = dict(
            Compose=dict(
                transformers=[dict(Increment=None), dict(Increment=dict(inc=2))]
            )
        )

        transformer = parser.parse(structure)

        [element] = transformer(tr.Element())

        assert isinstance(transformer, tr.Compose)
        assert len(transformer.transformers) == 2
        assert element.x == 3

    def test_parse_list(self):

        structure = [dict(Increment=None), dict(Increment=dict(inc=2))]

        transformer = parser.parse(structure)

        [element] = transformer(tr.Element())

        assert isinstance(transformer, tr.Compose)
        assert len(transformer.transformers) == 2
        assert element.x == 3

    def test_load(self):

        with open("test/test_transformer.yml", "r") as f:
            transformer = parser.load(f, values=dict(inc=2))

        [element] = transformer(tr.Element())

        assert isinstance(transformer, tr.Compose)
        assert len(transformer.transformers) == 2
        assert element.x == 3
