import numpy as np
from integration import a, b, c, A, N_sat, n

# Analytical solution calculated by hand.
# -(b**3*A*N_sat*(x/b)**a*(c*(x/b)**c-a+3)*e**(-(x/b)**c))/x**4

analytical_solution_x_equal_to_b = -A*N_sat*(c-a+3)/(b*np.e)

# Define the numerical differentiator using central difference method.
def central_difference(f,a,h=6.e-6):
    """
    f   ... function to be differentiated
    a   ... value computed at x = a
    h   ... step size
    """
    return (f(a + h) - f(a - h))/(2*h)

# Save as a text file.
np.savetxt('differentiation.txt',np.transpose([analytical_solution_x_equal_to_b,central_difference(n, b)]))
