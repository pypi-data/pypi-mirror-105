"""
Linear algebra routines
"""
from typing import List

import numpy as np
try:
    import jax
    import jax.numpy as anp
except:
    anp = np
    class jax: pass
    jax.jit = lambda x: x

def tridiag(a,b,c):
    """Tridiagonal linear operator.
    Parameters
    ==========

    a,b,c: Sequence[float]
        sequences of values on the diagonals of a tridiagonal matrix.
    """
    n = len(b)
    a,b,c = map(anp.array,(a,b,c))
    a0 = anp.pad(a,(1,0)).reshape((n,1))
    c0 = anp.pad(c,(0,1)).reshape((n,1))
    b0 = b.reshape((n,1))

    @jax.jit
    def fwd(y):
        y0 = anp.pad(y,((1,1),(0,0)))
        du = y0[:-2]*a0 + y0[1:-1]*b0 + y0[2:]*c0
        return du

    def as_array():
        return anp.array([
        [b[0],c[0],*[0.0]*(n-2)],
        *[[*[0.0]*(i),a[i],b[i+1],c[i+2],*[0.0]*((n-3)-i)] for i in range(n-2)],
        [*[0.0]*(n-2), a[-1],b[-1]]
        ])

    w= np.zeros(n-1)

    w[0] = c[0]/b[0]

    for i in range(1,n-1):
        w[i] = c[i]/(b[i] - a[i-1]*w[i-1])

    @jax.jit
    def _g(gn:float,h):
        g = (h[3] - h[0]*gn) / (h[1] - h[0]*h[2])
        return g,g
    @jax.jit
    def _p(pn,m):
        p = m[1] - m[0] * pn
        return [p]*2

    H = anp.array([[a[i-1],b[i],w[i-1]] for i in range(1,n)])

    @jax.jit
    def inv(y):
        hh = anp.concatenate((H,y[1:]),1)
        g0 = anp.array([y[0]/b[0]])
        _, g1 = jax.lax.scan(_g, g0[0], hh)
        g = anp.concatenate([g0,g1],0)
        mm = anp.concatenate((w[:,None],g[:-1]),1)
        p0 = g[n-1]
        _,p1 = jax.lax.scan(_p, p0, mm, reverse=True)
        return anp.concatenate([p1,p0[:,None]],0)

    fwd.inv = inv
    fwd.diag = (a,b,c)
    fwd.as_array = as_array
    return fwd


def _TDMAsolver(a, b, c, d):
    '''
    TDMA solver, a b c d can be NumPy array type or Python list type.
    refer to http://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
    and to http://www.cfd-online.com/Wiki/Tridiagonal_matrix_algorithm_-_TDMA_(Thomas_algorithm)
    '''
    nf = len(d) # number of equations
    ac, bc, cc, dc = map(np.array, (a, b, c, d)) # copy arrays
    ac, bc, cc, dc = map(lambda x: x.flatten(), (ac, bc, cc, dc)) # copy arrays
    for it in range(1, nf):
        mc = ac[it-1]/bc[it-1]
        bc[it] = bc[it] - mc*cc[it-1]
        dc[it] = dc[it] - mc*dc[it-1]

    xc = bc
    xc[-1] = dc[-1]/bc[-1]

    for il in range(nf-2, -1, -1):
        xc[il] = (dc[il]-cc[il]*xc[il+1])/bc[il]

    return xc

