"""

"""
import anon.atom as anp
import numpy as np
import matplotlib.pyplot as plt


def read_m228(filename):
    data = anp.asarray(np.loadtxt(filename))
    points = data[:,:2]
    weights = data[:,2]
    return points, weights

def plot(
    self,
    triangle=np.array([[-0.5, 0.0], [+0.5, 0.0], [0, 0.5 * (np.sqrt(3))]]),
    show_axes=False,
):
    """Shows the quadrature points on a given triangle. The size of the circles
    around the points coincides with their weights.
    """
    from matplotlib import pyplot as plt

    plt.plot(triangle[:, 0], triangle[:, 1], "-k")
    plt.plot(
        [triangle[-1, 0], triangle[0, 0]], [triangle[-1, 1], triangle[0, 1]], "-k"
    )

    if not show_axes:
        plt.gca().set_axis_off()

    transformed_pts = transform(self.points, triangle.T).T

    vol = get_vol(triangle)
    plot_disks(plt, transformed_pts, self.weights, vol)

    plt.axis("equal")

class Simplex:
    @classmethod
    def load(cls, filename):
        points, weights = read_m228(filename)
        return cls(points=points,weights=weights)

    def __init__(self,points=None,weights=None):
        self.points = points
        self.weights = weights

    def quad(f, *args, **kwds):
        nIP
        def f(x, y, state, *args):
            return vol * np.dot()

