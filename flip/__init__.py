"""
flip
"""

about = {}
with open("flip/__about__.py") as fp:
    exec(fp.read(), about)

__version__ = about['__version__']

from . import transformers
from . import utils
