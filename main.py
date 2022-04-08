# -------------------- Department Project -------------------- #
# Authors: Eloi Trenquier (eloi.trenquier@eleves.enpc.fr)
#
#
# Class Graph
# Represents a paving,
# Each vertex is a group of two points of the paving, (sub vertices)
# There are two types of vertices: blue ones, that join two different vertices that ccoorespond to the same point
# Red ones that join points that adjacent in our paving (connected)
# --------------------------------------------------------- #

class Vertex:
    """A vertex is a set of two sub_vertices, it corresponds to an edge of our Sphere Paving"""

    def __init__(self, id, sub_vertex1, sub_vertex2, length):
        self._id = id
        self._points = [sub_vertex1, sub_vertex2]
        self._length = length

class Paving_graph:
    """ A paving graph should be able to entirely represent a Paving and should be able to represent the addition/
    substraction of a quadrangle to the paving """

    def __init__(self, vertices, subvertices, edges):
        self._vertices = vertices
        self._subvertices = subvertices
        self._edges = edges