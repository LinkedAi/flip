"""
flip
"""
from . import transformers, utils

about = {}
with open('flip/__about__.py') as fp:
    exec(fp.read(), about)

__version__ = about['__version__']
