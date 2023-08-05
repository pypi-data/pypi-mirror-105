from typing import Sequence


def linspace(lower, upper, length, container=list):
    return container([lower + x*(upper-lower)/length for x in range(length)])

def hist(*args,steps=10):
    return [x for sublist in [
        linspace(args[i],args[i+1],steps) for i in range(len(args)-1)
    ] for x in sublist]
        
def quarters(
    origin:  float,
    max_val: float,
    steps:   int, #: steps per quarter-cycle
    quarter_cycles: int,
    call=lambda x: x
)->Sequence:
    """
    >>> quarters()
    """
    delta = (max_val - origin)/steps
    return jnp.array([
        jnp.linspace(
             origin if not i%2 else max_val, max_val-delta if not i%2 else origin+delta,  steps-1
        )*(1 if (not i%4) or (not (i-1)%4) else -1)
        for i in range(quarter_cycles) 
    ]).flatten()


def cycle(low, high, steps):
    pass

def path():
    pass

