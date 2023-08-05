

try:
    from jax.config import config
except:
    config = {}

_BACKEND = {
    'ops': 'jax',
    'numeric': 'jax'
}


#config.update('jax_disable_jit', True)

def use(backend, **kwds):
    _BACKEND['ops'] = backend
    _BACKEND['numeric'] = backend





