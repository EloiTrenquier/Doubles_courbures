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

    @property
    def id(self):
        return self._id

    def __str__(self):
        """Short string representaition of a Quad, returns only its _id value
        """
        return f"{self._id}"

    def __repr__(self):
        """Long string representation of a Quad"""
        desc = f"Quad {self._id} is an ABCD quad with " \
               f"\n AB = {self.a}, BC = {self.b}, CD = {self.c}, DA = {self.d}" \
               f"\n and DAB = {self.alpha}, ABC = {self.beta}, BCD = {self.gamma}, CDA = {self.delta}"
        return desc

    def rotate(self, number_rotations=1):
        """ Rotates the quad in the anti clock wise direction
        ABCD.rotate(1) -> BCDA """
        ang = self._angles
        cot = self._sides
        number_rotations = -number_rotations
        n_rot = number_rotations%4
        n_rot = 4-n_rot
        ang = ang[n_rot:] + ang[:n_rot]
        cot = cot[n_rot:] + cot[:n_rot]
        return Quad(self._id, ang[0], ang[1], ang[2], ang[3], cot[0], cot[1], cot[2], cot[3])

    def cote_gauche(self, ang):
        if ang == "alpha":
            return self._sides[0]
        if ang == "beta":
            return self._sides[1]
        if ang == "gamma":
            return self._sides[2]
        if ang == "delta":
            return self._sides[3]

    def cote_droite(self, ang):
        if ang == "alpha":
            return self._sides[3]
        if ang == "beta":
            return self._sides[0]
        if ang == "gamma":
            return self._sides[1]
        if ang == "delta":
            return self._sides[2]

    def angle(self, ang):
        if ang == "alpha":
            return self._angles[0]
        if ang == "beta":
            return self._angles[1]
        if ang == "gamma":
            return self._angles[2]
        if ang == "delta":
            return self._angles[3]


    def area(self):
        return self.alpha + self.beta + self.gamma + self.delta - 2 * np.pi
