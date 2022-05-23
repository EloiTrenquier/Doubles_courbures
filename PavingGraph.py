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
    """A vertex is a set of two sub_vertices, it corresponds to an edge of our Sphere Paving

        If this (real life) edge is on the outside (Used by only one quad),
    then the subvertices should be in the clockwise order for the quad it is a part of.
        If it is on the inside (Used by two quads) then subvertices are in the clockwise order for the oldest one
    and the anticlockwise order for the new one,
    but it should be okay because we can't 'build' anything in this edge anymore"""
    def __init__(self, sub_vertex1, sub_vertex2, length, id=None):
        """ The id will be used to get the position of the Vertex in the Vertex list"""
        self._id = id
        self._points = [sub_vertex1, sub_vertex2]
        self._length = length # == an angle on the sphere
        self._inside_edge = Edge(self, self, sub_vertex1, sub_vertex2, length, "blue")

    @property
    def id(self):
        return self._id

    @property
    def points(self):
        return self._points

    @property
    def inside_edge(self):
        return self._inside_edge

    def set_id(self, id):
        self._id = id
        for sub_v in self._points:
            sub_v.set_parent_id(id)

    def set_inside_edge(self, edge):
        self._inside_edge = edge


class SubVertex:
    """ A subVertex is a point of a quadrangle on the Sphere Paving"""

    def __init__(self, parent_id=None, in_edge_id=None, out_edge_id=None, neighbour_edge_id=None, id=None):
        """ A SubVertex may be part of multiple vertices, to recognize a SubVertex we use its id"""
        self._parent_id = parent_id #id of the vertex it is in
        self._in_edge_id = in_edge_id #id of the edge that goes from another subvertex to this one
        self._out_edge_id = out_edge_id #id of the edge that goes from this vertex to another
        self._neighbour_edge_id = neighbour_edge_id #id of the blue edge that goes to this neighbour
        self._id = id #Name of this subvertex, unique
        #A subvertex can represent the same vertex in "real life" ('A' for instance),
        #A subvetex representing A is connected to another subvertex by a red edge iff this one also represents A

    @property
    def id(self):
        return self._id

    @property
    def neighbour_edge_id(self):
        return self._neighbour_edge_id

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

    def set_neighbour_edge_id(self, id):
        self._neighbour_edge_id = id

    def set_parent_id(self, id):
        self._parent_id = id

    def set_in_edge_id(self, id):
        self._in_edge_id = id

    def set_out_edge_id(self, id):
        self._out_edge_id = id

class Edge:
    """An Edge here corresponds to the connection of two edges on the sphere, it's weight is the angle between them """

    def __init__(self, vertex1, vertex2, subvertex1, subvertex2, angle, color, id=None):
        """ The id will be used to get the position of the Vertex in the Vertex list"""
        self._id = id
        self._vertices = [vertex1, vertex2]
        self._subvertices = [subvertex1, subvertex2] #The first one is the one this edge originates from,
                                                    # the second is the destination
        self._weight = angle
        self._color = color

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

    @property
    def color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def set_id(self, id):
        out_subv, in_subv = self._subvertices[0], self._subvertices[1]
        if self._color == "red":
            out_subv.set_out_edge_id(id)
            in_subv.set_in_edge_id(id)
        elif self._color == "blue":
            out_subv.set_neighbour_edge_id(id)
            in_subv.set_neighbour_edge_id(id)
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

        for vertex in self._vertices:
            self._subvertices.append(vertex.points[0])
            self._subvertices.append(vertex.points[1])
            vertex.set_id(self._next_vert_id)
            self._used_vert_ids[self._next_vert_id] = True
            self._next_vert_id += 1
            self._edges.append(vertex.inside_edge)

        for edge in self._edges:
            edge.set_id(self._next_edge_id)
            self._used_edge_ids[self._next_edge_id] = True
            self._next_edge_id += 1

        for sv in self._subvertices:
            sv.set_id(self._next_subv_id)
            self._used_subv_ids[self._next_subv_id] = True
            self._next_subv_id += 1

    def add_subvertex(self, subv):
        """ Adds a subvertex and updates the subvertex registry"""
        if self._next_subv_id >= len(self._subvertices):
            self._subvertices.append(subv)
        else:
            self._subvertices[self._next_subv_id] = subv
        subv.set_id(self._next_subv_id)
        self._used_subv_ids[self._next_subv_id] = True
        self._next_subv_id += 1
        while self._used_subv_ids.get(self._next_subv_id, default=False):
            self._next_vert_id += 1

    def add_vertex(self, vertex):
        """ Adds a vertex, at the end of the list of vertices is complete or in the middle if the list is sparse"""
        if self._next_vert_id >= len(self._vertices):
            self._vertices.append(vertex)
        else:
            self._vertices[self._next_vert_id] = vertex
        vertex.set_id(self._next_vert_id)
        self._used_vert_ids[self._next_vert_id] = True
        self._next_vert_id += 1
        while self._used_vert_ids.get(self._next_vert_id, default=False):
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
        """ Generates the adjacency matrix independently of whether the edges are red or blue"""
        N = len(self._subvertices)
        adj_mat = np.zeros((N, N))
        for edge in self._edges:
            adj_mat[edge.subvertices[0].id, edge.subvertices[1].id] = 1 # or edge.weight ?
        for vertex in self._vertices:
            adj_mat[vertex.points[0].id, vertex.points[1].id] = 1 # or vertex.length ?
            adj_mat[vertex.points[1].id, vertex.points[0].id] = 1 # or vertex.length ?
        return adj_mat

    def find_last_subvertex(self, subvertex):
        """A function that finds the last subvertex and the angle around a certain subvertex"""
        tot_angle = 0
        subv = subvertex
        # Either p1.in_edge_id or p1.out_edge_id should be none
        assert subv.in_edge_id is None or subv.out_edge_id is None
        while subv.in_edge_id is not None:
            la_edge = self._edges[subv.in_edge_id]
            tot_angle += la_edge.weight
            subv = la_edge.subvertices[0]
        while subv.out_edge_id is not None:
            la_edge = self._edges[subv.out_edge_id]
            tot_angle += la_edge.weight
            subv = la_edge.subvertices[1]
        return tot_angle, subv

    def add_quad(self, quad, vertex_AB, side=0):
        """ Tries to append a quad to the graph
        by merging its i th side/edge (default first)
        and a specified vertex (a.k.a. real life edge) from the graph

        We consider the quad we have as an ABCD quad with: B = p1, C = p3, A = p2 and D = ?

        If it is possible to add a quad here, does so and returns 0
        else returns -1"""
        add_BC, add_CD1, add_CD2, add_DA = True, True, True, True
        if quad.sides[side] != vertex_AB.length: #Potentiellement ajouter une tolérance d'erreur (?)
            return -1
        #The first side of our quad fits on another edge : no need to create a vertex
        # We need to check for each edge of our quad whether it is free
        # or it coincides with another real life edge (a graph vertex)
        # 1st, we test for the 1st edge (in the clockwise order == edge[0] if we rotate the quad once anticlockwise)
        p1 = vertex_AB.points[0] #Le point B
        tot_angle_p1, n_p1 = self.find_last_subvertex(p1) #N_p1 est le point B mais contenu dans le dernier vertex
        tot_angle_p1 += quad.beta #The first angle clockwise
        if tot_angle_p1 > 2*pi: #+tolerance if we want some tolerance
            return -1
        elif tot_angle_p1 - 2*pi == 0: # < ... if we offer tolerance
            vertex_BC = self._vertices[n_p1.parent_id]
            if quad.b != vertex_BC.length:
                return -1
            else:
                add_BC = False #The second side of our quad fits on another edge : no need to create a vertex
                if vertex_BC.points[0].id == n_p1.id:
                    p3 = vertex_BC.points[1]
                else:
                    p3 = vertex_BC.points[0]
                tot_angle_p3, n_p3 = self.find_last_subvertex(p3) #n_p3 est le point C mais dans le dernier vertex
                tot_angle_p3 += quad.gamma
                if tot_angle_p3 > 2 * pi:  # +tolerance if we want some tolerance
                    return -1
                elif tot_angle_p3 - 2 * pi == 0:  # < ... if we offer tolerance
                    vertex_CD = self._vertices[p3.parent_id]
                    if quad.c != vertex_CD.length:
                        return -1
                    else:
                        add_CD1 = False #The third side of our quad fits on another edge : no need to create a vertex
        p2 = vertex_AB.points[1] #Should be A
        tot_angle_p2, n_p2 = self.find_last_subvertex(p2) #A but in the last vertex (furthest from AB)
        tot_angle_p2 += quad.alpha  # The first angle clockwise
        if tot_angle_p2 > 2 * pi:  # +tolerance if we want some tolerance
            return -1
        elif tot_angle_p2 - 2 * pi == 0:  # < ... if we offer tolerance
            vertex_AD = self._vertices[n_p2.parent_id]
            if quad.d != vertex_AD.length:
                return -1
            else:
                add_DA = False #The fourth edge of our quad fits on another edge : no need to create a vertex
                if vertex_AD.points[0].id == n_p2.id:
                    p4 = vertex_AD.points[1]
                else:
                    p4 = vertex_AD.points[0]
                tot_angle_p4, n_p4 = self.find_last_subvertex(p4)
                tot_angle_p4 += quad.delta
                if tot_angle_p4 > 2 * pi:  # +tolerance if we want some tolerance
                    return -1
                elif tot_angle_p4 - 2 * pi == 0:  # < ... if we offer tolerance
                    vertex_CD = self._vertices[p3.parent_id]
                    if quad.c != vertex_CD.length:
                        return -1
                    else:
                        add_CD2 = False #The third side of our quad fits on another edge : no need to create a vertex
        if add_BC:
            new_B = SubVertex()
            new_C = SubVertex()
            self.add_subvertex(new_B)
            self.add_subvertex(new_C)
            BC = Vertex(B,C, quad.b)
            if add_CD1:
        return 0














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
