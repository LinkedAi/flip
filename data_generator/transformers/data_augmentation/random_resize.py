from data_generator.transformers.transform import Transformer
from data_generator.transformers.constants import Resize


class RandomResize(Transformer):
    def __init__(
        self,
        mode: Resize = Resize.asymmetric,
        wmin=None,
        wmax=None,
        hmin=None,
        hmax=None,
    ):
        self.wmin = wmin
        self.wmax = wmax
        self.hmin = hmin
        self.hmax = hmax
        self.mode = mode

    def map(self, element: Element) -> Element:
        assert element, "Element cannot be None"

        wmin = self.wmin if self.wmin is not None else element.image.shape[1]
        hmin = self.hmin if self.hmin is not None else element.image.shape[0]
        wmax = self.wmax if self.wmax is not None else element.image.shape[1]
        hmax = self.hmax if self.hmax is not None else element.image.shape[0]

        if self.mode == Resize.symmetrich:
            h = (
                hmin
                if hmin == hmax is not None
                else np.random.randint(low=hmin, high=hmax,)
            )
            w = element.image.shape[1] * (h / element.image.shape[0])
            w = int(w)
        if self.mode == Resize.symmetricw:
            w = (
                wmin
                if wmin == wmax is not None
                else np.random.randint(low=wmin, high=wmax,)
            )
            h = element.image.shape[0] * (w / element.image.shape[1])
            h = int(h)
        else:
            w = (
                wmin
                if wmin == wmax is not None
                else np.random.randint(low=wmin, high=wmax,)
            )

            h = (
                hmin
                if hmin == hmax is not None
                else np.random.randint(low=hmin, high=hmax,)
            )

        element.image = cv2.resize(element.image, (w, h))

        return element
