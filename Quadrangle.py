# -------------------- Department Project -------------------- #
# Authors: Eloi Trenquier (eloi.trenquier@eleves.enpc.fr)
#
#
# Quadrangle Class
# After a gaussian transform, a quad on the sphere represents a node in real life,
# Our quads are determined by the four angles separating each two consecutive side
# --------------------------------------------------------- #
import numpy as np
class Quadrangle:
    """A quadrangle can be defined by four angles and the length of a side (also an angle in spherical geometry)
    Here we define it with all the angles and all the side lengths in order not to have to compute anything """
    def __init__(self, id, alpha, beta, gamma, delta, a, b, c, d):
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._delta = delta
        self._a = a
        self._b = b
        self._c = c
        self._d = d

    @property
    def a(self):
        return self._a
    @property
    def b(self):
        return self._b
    @property
    def c(self):
        return self._c
    @property
    def d(self):
        return self._d
    @property
    def alpha(self):
        return self._alpha
    @property
    def beta(self):
        return self._beta
    @property
    def gamma(self):
        return self._gamma
    @property
    def delta(self):
        return self._delta

    def area(self):
        return self._alpha + self._beta + self._gamma + self._delta - 2*np.pi
