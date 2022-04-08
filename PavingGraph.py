# -------------------- Department Project -------------------- #
# Authors: Eloi Trenquier (eloi.trenquier@eleves.enpc.fr)
#          Maxim Legendre (maxim.legendre@eleves.enpc.fr)
#
# Class Graph
# Represents a paving,
# Each vertex is a group of two points of the paving, (sub vertices)
# There are two types of vertices: blue ones, that join two different vertices that ccoorespond to the same point
# Red ones that join points that adjacent in our paving (connected)
# --------------------------------------------------------- #

from Quadrangle import *
from Spheric_representation import *
import numpy as np

pi = np.pi
eps = 1e-4


class Vertex:
    """A vertex is a set of two sub_vertices, it corresponds to an edge of our Sphere Paving"""

    def __init__(self, id, sub_vertex1, sub_vertex2, length):
        self._id = id
        self._points = [sub_vertex1, sub_vertex2]
        self._length = length


class SubVertex:
    """ A subVertex is a point of a quadrangle on the Sphere Paving"""

    def __init__(self, id):
        self._id

    @property
    def id(self):
        return self._id


class PavingGraph:
    """ A paving graph should be able to entirely represent a Paving and should be able to represent the addition/
    substraction of a quadrangle to the paving """

    def __init__(self, vertices, subvertices, edges):
        self._vertices = vertices
        self._subvertices = subvertices
        self._edges = edges


def add_quad(noeud, quad, angle, cote="d"):
    S = 0
    for i in range(len(noeud)):
        S += noeud[i][0].angle(noeud[i][1])
    cond = (S + quad.angle(angle)) < 2 * pi
    if cond:
        if S >= 2 * pi-eps :
            cond = cond and (quad.cote_gauche(angle) == noeud[-1][0].cote_droite(noeud[-1][1])) and (
                        quad.cote_droit(angle) == noeud[-1][0].cote_gauche(noeud[-1][1]))
            if cond:
                noeud.append([quad, angle])
        if cote == "d":
            cond = cond and (quad.cote_gauche(angle) == noeud[-1][0].cote_droite(noeud[-1][1]))
            if cond:
                noeud.append([quad, angle])

        else:
            cond = cond and (quad.cote_droit(angle) == noeud[-1][0].cote_gauche(noeud[-1][1]))
            if cond:
                noeud = [[quad, angle]] + noeud
    return noeud, cond

def possible_noeud(liste_quad, valence):
    liste_oriente= []
    for quad in liste_quad:
        for angle in ["alpha", "beta", "gamma", "delta"]:
            liste_oriente.append([quad, angle])
    noeud_possible = liste_oriente
    for i in range(valence-1):
        noeud_popo =[]
        for i in range(len(noeud_possible)):
            for j in range(len(liste_oriente)):
                new_noeud, cond = add_quad(noeud_possible[i],liste_oriente[j][0],liste_oriente[j][1])
                if cond :
                    noeud_popo.append(new_noeud)







