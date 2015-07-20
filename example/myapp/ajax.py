import sys


if sys.version_info >= (3, 0):
    from .ajax3 import *  # noqa
else:
    from .ajax2 import *  # noqa
