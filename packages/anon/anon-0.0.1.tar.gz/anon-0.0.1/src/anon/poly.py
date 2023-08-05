"""Procedures involving polynomial families
"""

import jax.numpy as jnp



def lagrange(i=None,n:int=None,p=None,x=None):
    r"""Lagrange polynomial interpolation.

    $$
    \begin{aligned}
        L(x) &= 1\times \frac{x (x - 2)}{-1} + 8\times \frac{x (x-1)}{2} \\
                &= x (-2 + 3x)
    \end{aligned}
    $$

    Parameters
    ----------
    x : array_like
        `x` represents the x-coordinates of a set of datapoints.

    """

    if x is not None: 
        M = len(x)
    else:
        M = n 
        x = jnp.linspace(-1,1,n)
    cf = jnp.ones(1)
    for k in range(M):
        if k == i: continue
        fac = x[i]-x[k]
        cf = jnp.convolve(cf,   jnp.array([1.0, -x[k]])/fac)
    return cf
