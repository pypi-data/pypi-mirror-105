"""Automatic differentiation API
"""

from typing import Callable, Union, Sequence
try:
    import jax
    import jax.numpy as jnp
    import jax.linear_util as lu
    from jax import grad
    from jax.util import partial
    from jax.interpreters import batching
    from jax.api_util import argnums_partial

except:
    pass


from anon import lila

def _jacfwd(
    fun: Callable,
    outnums: Union[int, Sequence[int]] = None,
    argnums: Union[int, Sequence[int]] = 0,
    *,
    squeeze: bool = True,
    holomorphic: bool = False,
    nf: int = None,
    return_val: bool = False,
) -> Callable:
    """
    """
    if outnums is None:
        if nf is None:
            f_transformed = fun
        else:
            f_transformed = lambda *args,**kwds: fun(*args,**kwds)[:nf,:nf]
    else:
        f_transformed = lambda *args,**kwds: fun(*args,**kwds)[outnums]



    if return_val:
        def jacobian(*args,**kwds):
            f = lu.wrap_init(f_transformed, kwds)
            f_partial, dyn_args = argnums_partial(f, argnums, args)
            jax.api.tree_map(partial(jax.api._check_input_dtype_jacfwd, holomorphic), dyn_args)
            pushfwd = partial(jax.api._jvp, f_partial, dyn_args)
            y, jac = jax.vmap(pushfwd, out_axes=(None, -1))(jax.api._std_basis(dyn_args))
            jax.api.tree_map(partial(jax.api._check_output_dtype_jacfwd, holomorphic), y)
            example_args = dyn_args[0] if isinstance(argnums, int) else dyn_args
            jac = jax.tree_util.tree_map(partial(jax.api._unravel_array_into_pytree, example_args, -1), jac)
            return jac, y
    else:
        def jacobian(*args,**kwds):
            f = lu.wrap_init(f_transformed, kwds)
            f_partial, dyn_args = argnums_partial(f, argnums, args)
            jax.api.tree_map(partial(jax.api._check_input_dtype_jacfwd, holomorphic), dyn_args)
            pushfwd = partial(jax.api._jvp, f_partial, dyn_args)
            y, jac = jax.vmap(pushfwd, out_axes=(None, -1))(jax.api._std_basis(dyn_args))
            jax.api.tree_map(partial(jax.api._check_output_dtype_jacfwd, holomorphic), y)
            example_args = dyn_args[0] if isinstance(argnums, int) else dyn_args
            jac = jax.tree_util.tree_map(partial(jax.api._unravel_array_into_pytree, example_args, -1), jac)
            return jac

    if squeeze:
        return lambda *args, **kwds: jnp.squeeze(jacobian(*args,**kwds))
    else:
        return jacobian


def jacfwd(
    fun: Callable,
    outnums: Union[int, Sequence[int]] = None,
    argnums: Union[int, Sequence[int]] = 0,
    *,
    squeeze: bool = True,
    holomorphic: bool = False, 
    nf: int = None
) -> Callable:
    """
    """
    return _jacfwd(fun, outnums, argnums, squeeze=squeeze,
                    holomorphic=holomorphic,nf=nf,return_val=False)

def value_and_jacfwd(
    fun: Callable,
    outnums: Union[int, Sequence[int]] = None,
    argnums: Union[int, Sequence[int]] = 0,
    *,
    squeeze: bool = True,
    holomorphic: bool = False, 
    nf: int = None
) -> Callable:
    """
    Adapted from https://github.com/google/jax/pull/762 
    """
    return _jacfwd(fun, outnums, argnums, squeeze=squeeze,
                    holomorphic=holomorphic,nf=nf,return_val=True)


def jacrev(fun: Callable, outnums: Union[int, Sequence[int]] = None,
            argnums: Union[int,Sequence[int]]=0, *,
            holomorphic: bool = False, squeeze=True) -> Callable:
    if outnums is None:
        jac = jax.jacrev(fun, argnums, holomorphic)
    else:
        jac = jax.jacrev(lambda *args,**kwds: fun(*args,**kwds)[outnums],argnums,holomorphic)
    if squeeze:
        return lambda *args, **kwds: jnp.squeeze(jac(*args,**kwds))
    else:
        return jac

def stiffness_matrix(f, nf, mode='fwd',jit=False):
    F = lambda x, **params: f(x,**params)
    if mode == 'fwd':
        Df = lambda x, **params: jnp.squeeze(jax.jacfwd(f)(x,**params))[:nf,:nf]
        if jit: Df = jax.jit(Df)
        return Df

def jacx(fun:Callable):
    if hasattr(fun, "jacx"):
        return fun.jacx
    else:
        return jacfwd(fun,1,0)


#-------------------------------------------------------------------
# Finite Difference Operators
#-------------------------------------------------------------------

#@linear("tridiagonal")
def finite_ctr(n,dx,scale=1.,boun=("n","n")):
    """Create a centered finite difference operator.

    """

    a,b,c = (
        [ 1.0/(dx**2)*scale]*(n-2),
        [-2.0/(dx**2)*scale]*(n-2),
        [ 1.0/(dx**2)*scale]*(n-2)
    )
    if boun[0].lower()[0] == "n":
        a = a + [2.0/(dx**2)*scale]
        c = [2.0/(dx**2)*scale] + c
        b = [-2.0/(dx**2)*scale] + b + [-2.0/(dx**2)*scale]

    return lila.tridiag(*map(jnp.array,(a,b,c)))











