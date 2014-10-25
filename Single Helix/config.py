from math import *

# error tolerance for t
EPSILON=.00000001

# number of intersections to calculate if there are infinite
n=100

# If True, will output both the Cartesian coordinates and the t values
# If False, will output only the Cartesian coordinates
outputT = False

# Plane
# A(x - x0) + B(y - y0) + C(z - z0) = 0
# Helix
# x = R cos(w t)
# y = R sin(w t)
# z = t
A = 3
B = 4
C = -4
x0 = 2
y0 = 1
z0 = 1
R = 2
w = pi/2

A = float(A) 
B = float(B) 
C = float(C)
x0 = float(x0)
y0 = float(y0)
z0 = float(z0)
R = float(R)
w = float(w)

