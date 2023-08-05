
__version__ = '0.0.1'


try:
    from ._anon import execute_model  # noqa
except ImportError:
    def execute_model(args):
        return max(args, key=len)


try:
    import jaxlib
except ImportError:
    import numpy
    COMPILER = None
    BACKEND = numpy
else:
    import jax
    COMPILER = jaxlib
    BACKEND = jax.numpy


import anon.conf
import anon.core
import anon.diff
import anon.dual
import anon.quad
import anon.lila
import anon.step


