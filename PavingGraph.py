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

import Quadrangle as qd
import numpy as np

pi = np.pi
eps = 1e-4


class Vertex:
    """A vertex is a set of two sub_vertices, it corresponds to an edge of our Sphere Paving"""

    def __init__(self, sub_vertex1, sub_vertex2, length, id=None):
        """ The id will be used to get the position of the Vertex in the Vertex list"""
        self._id = id
        self._points = [sub_vertex1, sub_vertex2]
        self._length = length # == an angle on the sphere

    @property
    def id(self):
        return self._id

    @property
    def points(self):
        return self._points

    def set_id(self, id):
        self._id = id
        for sub_v in self._points:
            sub_v.set_parent_id(id)


class SubVertex:
    """ A subVertex is a point of a quadrangle on the Sphere Paving"""

    def __init__(self, parent_id, in_edge_id=None, out_edge_id=None, id=None):
        """ A SubVertex may be part of multiple vertices, to recognize a SubVertex we use its id"""
        self._parent_id = parent_id
        self._in_edge_id = in_edge_id
        self._out_edge_id = out_edge_id
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def in_edge_id(self):
        if self._out_edge_id is None:
            return -1
        else:
            return self._in_edge_id

    @property
    def out_edge_id(self):
        if self._out_edge_id is None:
            return -1
        else:
            return self._out_edge_id

    @property
    def parent_id(self):
        return self.parent_id

    def set_id(self, id):
        self._id = id

    def set_parent_id(self, id):
        self._parent_id = id

    def set_in_edge_id(self, id):
        self._in_edge_id = id

    def set_out_edge_id(self, id):
        self._out_edge_id = id

class Edge:
    """An Edge here corresponds to the connection of two edges on the sphere, it's weight is the angle between them """

    def __init__(self, vertex1, vertex2, subvertex1, subvertex2, angle, id=None):
        """ The id will be used to get the position of the Vertex in the Vertex list"""
        self._id = id
        self._vertices = [vertex1, vertex2]
        self._subvertices = [subvertex1, subvertex2]
        self._weight = angle

    @property
    def id(self):
        return self._id

    @property
    def vertices(self):
        return self._vertices

    @property
    def subvertices(self):
        return self._subvertices

    @property
    def weight(self):
        return self._weight

    def set_id(self, id):
        out_subv, in_subv = self._subvertices[0], self._subvertices[1]
        out_subv.set_out_edge_id(id)
        in_subv.set_in_edge_id(id)
        self._id = id

class PavingGraph:
    """ A paving graph should be able to entirely represent a Paving and should be able to represent the addition/
    substraction of a quadrangle to the paving """

    def __init__(self, vertices, edges):
        """ Vertices is a list of all the vertices
            Edges is a list of edges (of the shape [[v1, v2], weight, id])"""
        self._vertices = vertices
        self._subvertices = []
        self._edges = edges
        self._used_vert_ids = {}
        self._next_vert_id = 0
        self._used_subv_ids = {}
        self._next_subv_id = 0
        self._used_edge_ids = {}
        self._next_edge_id = 0

        for vertex in vertices:
            self._subvertices.append(vertex.points[0])
            self._subvertices.append(vertex.points[1])
            vertex.set_id(self._next_vert_id)
            self._used_vert_ids[self._next_vert_id] = True
            self._next_vert_id += 1

        for edge in edges:
            edge.set_id(self._next_edge_id)
            self._used_edge_ids[self._next_edge_id] = True
            self._next_edge_id += 1

        for sv in self._subvertices:
            sv.set_id(self._next_subv_id)
            self._used_subv_ids[self._next_subv_id] = True
            self._next_subv_id += 1

    def add_vertex(self, vertex):
        """ Adds a vertex, at the end of the list of vertices is complete or in the middle if the list is sparse"""
        if self._next_vert_id >= len(self._vertices):
            self._vertices.append(vertex)
        else:
            self._vertices[self._next_vert_id] = vertex
        vertex.set_id(self._next_vert_id)
        self._used_vert_ids[self._next_vert_id] = True
        self._next_vert_id += 1
        while self._used_subv_ids.get(self._next_subv_id, default=False):
            self._next_vert_id += 1

    def remove_vertex(self, vertex):
        """ Removes a vertex by sparsifying the list of used vertices ids"""
        self._used_vert_ids[vertex.id] = False
        self._next_vert_id = min(vertex.id, self._next_vert_id)

    def add_edge(self, edge):
        """ Adds an edge, at the end of the list of edges is complete or in the middle if the list is sparse"""
        if self._next_edge_id >= len(self._edges):
            self._edges.append(edge)
        else:
            self._edges[self._next_edge_id] = edge
        edge.set_id(self._next_edge_id)
        self._used_edge_ids[self._next_edge_id] = True
        self._next_edge_id += 1
        while self._used_edge_ids.get(self._next_edge_id, default=False):
            self._next_edge_id += 1

    def total_adjacency_mat(self):
        N = len(self._subvertices)
        adj_mat = np.zeros((N, N))
        for edge in self._edges:
            adj_mat[edge.subvertices[0].id, edge.subvertices[1].id] = 1 # or edge.weight ?
        for vertex in self._vertices:
            adj_mat[vertex.points[0].id, vertex.points[1].id] = 1 # or vertex.length ?
            adj_mat[vertex.points[1].id, vertex.points[0].id] = 1 # or vertex.length ?
        return adj_mat

    def add_quad(self, quad, vertex, side=0):
        """ Tries to append a quad to the graph
        by merging its i th side/edge (default first)
        and a specified vertex (a.k.a. real life edge) from the graph

        If it is possible to add a quad here, does so and returns 0
        else returns -1"""
        check_list = quad.sides[0] == vertex.length #Potentiellement ajouter une tolérance d'erreur (?)



def add_quad(noeud, quad, angle, cote="d"):
    S = 0
    for i in range(len(noeud)):
        S += noeud[i][0].angle(noeud[i][1])
    cond = (S + quad.angle(angle)) < 2 * pi
    if cond:
        if S >= 2 * pi - eps:
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


def somme_angle_noeud(noeud):
    S = 0
    for i in range(len(noeud)):
        S += noeud[i][0].angle(noeud[i][1])
    return S


def possible_noeud(liste_quad, valence):
    liste_oriente = []
    for quad in liste_quad:
        for angle in ["alpha", "beta", "gamma", "delta"]:
            liste_oriente.append([quad, angle])
    noeud_possible = liste_oriente
    for k in range(valence - 1):
        noeud_popo = []
        for i in range(len(noeud_possible)):
            for j in range(len(liste_oriente)):
                new_noeud, cond = add_quad(noeud_possible[i], liste_oriente[j][0], liste_oriente[j][1])
                if cond:
                    noeud_popo.append(new_noeud)
        noeud_possible = noeud_popo
    noeuds_finaux = []
    for i in range(len(noeud_possible)):
        if somme_angle_noeud(noeud_possible[i]) > 2 * pi - eps:
            noeuds_finaux.append(noeud_possible[i])
    return noeuds_finaux
