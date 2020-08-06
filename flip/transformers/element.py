class Element:
    """The Element class represents the base class than can be use by a Transform
        Commonly used arguments are:
            - image: Numpy Array with the image of the element
            - name: A name for the element can be use for label it
            - objects: Child Elements of this element, mostly used when the parent Element is a background

        Commonly extra parameters:
            - x, y: To set the position of the element over a parent element
            - tags: To save the information of the generated tags for the child objects
    """

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, key):
        return None

    def __repr__(self):

        fields = ", ".join(f"{key}={value}" for key, value in vars(self).items())

        return f"Element({fields})"

