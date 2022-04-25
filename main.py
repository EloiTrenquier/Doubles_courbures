# -------------------- Department Project -------------------- #
# Authors: Eloi Trenquier (eloi.trenquier@eleves.enpc.fr)
#          Maxim Legendre (maxim.legendre@eleves.enpc.fr)
#
# Main
# --------------------------------------------------------- #
#import PavingGraph as pg
import Quadrangle as qd
import numpy as np

carre = qd.Quad("carré", np.pi/2, np.pi/2, np.pi/2, np.pi/2, 1, 1, 1, 1)
print(carre)
print(repr(carre))

rect = qd.Quad("rectangle", np.pi/2, np.pi/2, np.pi/2, np.pi/2, 1, 2, 1, 2)
print(repr(rect))
print(repr(rect.rotate(401)))
