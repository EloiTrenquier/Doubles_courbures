# -------------------- Department Project -------------------- #
# Authors: Eloi Trenquier (eloi.trenquier@eleves.enpc.fr)
#          Maxim Legendre (maxim.legendre@eleves.enpc.fr)
#
# Quadrangle Class
# After a gaussian transform, a quad on the sphere represents a node in real life,
# Our quads are determined by the four angles separating each two consecutive side
# --------------------------------------------------------- #
import numpy as np


class Quad:
    """A quadrangle can be defined by four angles and the length of a side (also an angle in spherical geometry)
    Here we define it with all the angles and all the side lengths in order not to have to compute anything """

    def __init__(self, id, alpha, beta, gamma, delta, a, b, c, d):
        self._id = id
        self._angles = [alpha, beta, gamma, delta]
        self._sides = [a, b, c, d]

    @property
    def a(self):
        return self._sides[0]

    @property
    def b(self):
        return self._sides[1]

    @property
    def c(self):
        return self._sides[2]

    @property
    def d(self):
        return self._sides[3]

    @property
    def alpha(self):
        return self._angles[0]

    @property
    def beta(self):
        return self._angles[1]

    @property
    def gamma(self):
        return self._angles[2]

    @property
    def delta(self):
        return self._angles[3]

    def __str__(self):
        """Short string representaition of a Quad, returns only its _id value
        """
        return f"{self._id}"

    def __repr__(self):
        """Long string representation of a Quad"""
        desc = f"Quad {self._id} is an ABCD quad with " \
               f"\n AB = {self.a}, BC = {self.b}, CD = {self.c}, DA = {self.d}" \
               f"\n and DAB = {self.alpha}, ABC = {self.beta}, BCD = {self.gamma}, CDA = {self.delta}"

    def cote_gauche(self, ang):
        if ang == "alpha":
            return self.a
        if ang == "beta":
            return self.b
        if ang == "gamma":
            return self.c
        if ang == "delta":
            return self.d

    def cote_droite(self, ang):
        if ang == "alpha":
            return self.d
        if ang == "beta":
            return self.a
        if ang == "gamma":
            return self.b
        if ang == "delta":
            return self.c

    def angle(self, ang):
        if ang == "alpha":
            return self.alpha
        if ang == "beta":
            return self.beta
        if ang == "gamma":
            return self.gamma
        if ang == "delta":
            return self.delta

    def area(self):
        return self.alpha + self.beta + self.gamma + self.delta - 2 * np.pi
