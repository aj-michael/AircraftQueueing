#!/usr/bin/python
import sys
from math import *
from config import *

def bisection(a,b,f):
    midpt = (a+b)/2
    if ((b-a)/2<EPSILON):
        output(midpt)
    elif f(a) == copysign(f(a),f(midpt)):
        bisection(midpt,b,f)
    else:
        bisection(a,midpt,f)

def output(t):
    point = [R*cos(w*t),R*sin(w*t),t]
    if outputT:
        print t
    print point


# algorithm starts here
if (C == 0):
    if (abs(A*x0+B*y0+C*z0) > abs(R*sqrt(A*A+B*B))):
        print "none"
        exit(0)
    else:
        n = int(n)
        k = 0
        while k < int(n):   
            t1 = 1/w * (2*k*pi+asin((A*x0+B*y0)/R/sqrt(A*A+B*B))-atan2(A,B))
            t2 = 1/w * ((2*k+1)*pi-asin((A*x0+B*y0)/R/sqrt(A*A+B*B))-atan2(A,B))
            if (t1<t2):
                output(t1) ; output(t2) ; k = k + 2
            elif (t1>t2):
                output(t2) ; output(t1) ; k = k + 2
            else:
                output(t1) ; k = k + 1
else:
    f = lambda t: R*sqrt(A**2+B**2)*sin(w*t+atan2(A,B))-A*x0-B*y0-C*z0+C*t
    period = 2*pi/w
    amplitude=R*sqrt(A**2+B**2)
    m = -C
    b = A*x0+B*y0+C*z0
    t0 = -amplitude / abs(m) - b / m
    t1 =  amplitude / abs(m) - b / m

    if abs(C/(R*w*sqrt(A**2+B**2))) <= 1:
        # extrema1 > extrema2
        extrema1 = 1/w*(acos(-C/(R*w*sqrt(A**2+B**2)))-atan2(A,B))
        extrema2 = 1/w*(-acos(-C/(R*w*sqrt(A**2+B**2)))-atan2(A,B))
        if (extrema2 > t0):
            while (extrema2 > t0):
                extrema1, extrema2 = extrema2, extrema1-2*pi/w
        elif (extrema1 < t0):
            while (extrema1 < t0):
                extrema1, extrema2 = extrema2+2*pi/w, extrema1
        if f(extrema1) == copysign(f(extrema1),f(extrema2)):
            extrema1, extrema2 = extrema2+2*pi/w, extrema1
        while f(extrema1) != copysign(f(extrema1),f(extrema2)):
            bisection(extrema2,extrema1,f)
            extrema1, extrema2 = extrema2+2*pi/w, extrema1
    else:
        bisection(t0,t1,f)
