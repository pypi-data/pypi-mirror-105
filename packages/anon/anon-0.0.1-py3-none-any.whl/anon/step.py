import scipy.linalg
Callable = object()

try:
    import jax
    from jax.ops import index, index_update
    from jax.lax import switch
    import jax.numpy as jnp
except:
    pass # this wont work without jax
from anon import lila



def rk_lin(dt,tableau:dict,B,d,tridiag=False):
    tableau = _pre_proc_tableau(tableau)
    b = tableau["b"]
    no_stages = len(b)
    #n = len(B) if not tridiag else len(B.diag[1])

    if tridiag:
        n = len(B.diag[1])
        stages = [
            _rk_td_stage(i,dt,tableau["A"],B,d)
                for i in range(no_stages)
        ]
    elif callable(d):
        n = len(B)
        stages = [
            _rk_lin_src_stage(i,dt,tableau["A"],tableau["c"],B,d)
                for i in range(no_stages)
        ]

    else:
        n = len(B)
        stages = [
            _rk_lin_stage(i,dt,tableau["A"],B,d)
                for i in range(no_stages)
        ]

    @jax.jit
    def _stage_i(i,carry):
        u,K,t = carry
        K = index_update(
           K,index[:,i],switch(i,stages,(u,K,t)).squeeze()
        )
        return u,K,t

    K0 = jnp.zeros((n,no_stages))

    @jax.jit
    def step(u,t=0.0):
        _,k,__ = jax.lax.fori_loop(0,no_stages,_stage_i,(u,K0,t))
        return u + dt*jnp.average(k,axis=1,weights=b)[:,None]

    return locals()


def _rk_lin_src_stage(s,dt,A,c,B,d: Callable):
    """
    Parameters
    ----------
    s: int
        stage number

    """
    ai = jnp.array(A[s])
    B1 = jnp.eye(len(B)) - dt*ai[s]*B

    @jax.jit
    def _B0(args):
        u,K,t = args
        u_a = B@(u)
        ds = d(t+dt*c[s])
        return jnp.linalg.solve(B1,u_a + ds)

    @jax.jit
    def _B1(args):
        u,K,t = args
        du = dt*jnp.average(K,axis=1,weights=ai)[:,None]
        u_a = B@(u+du)
        return jnp.linalg.solve(B1, u_a + d(t+dt*c[s]))

    if s > 0:
        return _B1
    else:
        return _B0




def _rk_lin_stage(s:int,dt,A,B,d):
    """
    Parameters
    ----------
    s

    """
    ai = jnp.array(A[s])
    print(f"aii: {ai[s]}")
    B1 = jnp.eye(len(B)) - dt*ai[s]*B

    @jax.jit
    def _B1(args):
        u,K,t = args
        du = dt*jnp.average(K,axis=1,weights=ai)[:,None]
        u_a = B@(u+du)
        return jnp.linalg.solve(B1, u_a + d)

    if s > 0:
        return _B1
    else:
        return lambda args: jnp.linalg.solve(B1,B@args[0]+d)


def _rk_td_stage(s,dt,A,B,d):
    """
    Parameters
    ----------

    ai: array (sx0)
    """

    a,b,c = B.diag
    ai = jnp.array(A[s])
    B1 = lila.tridiag(
            -dt*ai[-1]*a,
          1.-dt*ai[-1]*b,
            -dt*ai[-1]*c,
    )

    @jax.jit
    def _B1(args):
        u,K,t = args
        du = dt*jnp.average(K,axis=1,weights=ai)[:,None]
        u_a = B(u+du)
        return B1.inv(u_a + d)

    if s > 0:
        return _B1
    else:
        return lambda args: B1.inv(B(args[0])+d)

def ADI(dt:float,DX:tuple,B):
    def step(u):
        pass

def _pre_proc_tableau(tableau):
    A, b = tableau["A"], tableau["b"]
    S = len(b)
    return dict(
        A = list(A[i] + [0.0]*(S - len(A[i])) for i in range(S)),
        b = b,
        c = tableau["c"] if "c" in tableau else [0.0]*S
    )

