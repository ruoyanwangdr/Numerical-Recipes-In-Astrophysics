import numpy as np
from random_generator import xor_shift_64

# Generate random numbers as required.
a = (2.5-1.1)*xor_shift_64()+1.1
b = (2-0.5)*xor_shift_64()+0.5
c = (4-1.5)*xor_shift_64()+1.5

# Since there's no theta or phi dependence, the 3D spherical
# intergral can be simplied to a 1D integral multiplied with
# 4*pi*x**2. Cancel the constant N_sat on both sides and we have
# an integration equal to 1. A*intergral(n_1d) = 1.
# A is then just 1/result.

n_1d = lambda x:4*np.pi*x**2*(x/b)**(a-3)*np.e**(-(x/b)**c)

# Since the lower bound is 0, the function becomes improper,
# and thus taking the midpoint rule as the integration method.

# Midpoint rule.
def midpoint(f, a, b, N):
    """
    f     ... function to be integrated
    [a,b] ... integration interval
    N     ... number steps(bigger the better but slower)

    This method uses rectangles to approximate the area under the curve.
    Rectangle width is determined by the interval of integration.
    The interval of integration is then divided into n smaller intervals of equal lengths as step sizes increase,
    and n rectangles would used to approximate the integral; each smaller rectangle has the width of the smaller interval.
    The rectangle height is the function’s value at the midpoint of its base.
    """

    h = float(b-a)/N
    output = 0
    for i in range(N):
        output += f((a+h/2.0)+i*h)
    output *= h
    return output

# Calculate A.
A = 1/midpoint(n_1d,0,5,100)

# Write out the density profile of the satellite galaxies.
N_sat = 100
def n(x):
    return A*N_sat*(x/b)**(a-3)*np.e**(-(x/b)**c)

# Save as a text file.
np.savetxt('integrated_result.txt', [a,b,c,A])
