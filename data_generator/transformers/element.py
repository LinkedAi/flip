import numpy as np
from dataclasses import dataclass
import typing as tp


class Element:
    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, key):
        return None

    def __repr__(self):

        fields = ", ".join(f"{key}={value}" for key, value in vars(self).items())

        return f"Element({fields})"

