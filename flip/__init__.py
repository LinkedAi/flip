"""
flip
"""
from . import transformers, utils
import os

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

about = {}
with open(f'{APP_ROOT}/flip/__about__.py') as fp:
    exec(fp.read(), about)

__version__ = about['__version__']
__title__ = about['__title__']
__package_name__ = about['__package_name__']
__description__ = about['__description__']
__email__ = about['__email__']
__author__ = about['__author__']
__github__ = about['__github__']
__pypi__ = about['__pypi__']
__license__ = about['__license__']