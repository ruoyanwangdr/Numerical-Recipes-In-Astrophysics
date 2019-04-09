import numpy as np
from integration import n


# Define N(x).
def N(x):
    return n(x)*4*np.pi*x**2

# Choose root-finding method to be bisection.
def bisection(xminus, xplus, iterations, eps, root):
    """
    [x-,x+]     ... bracket of the root
    iterations  ... max number of iterations
    eps         ... floating-point relative accuracy
    root        ... wanted y value of the input funtion

    """

    for i in range(0,iterations):
        x=(xminus+xplus)/2  # Split the x range from the mid point
        if N(x) > root:   # If root in other half
            xplus=x   # Change x+ to x
        else:   # If not
            xminus=x   # Change x- to x
        if(xplus-xminus<eps):   # If converged
            #print('root found with precision eps = ',eps)
            break
        if i==iterations-1: # If not converged
            #print('root not found after Nmax iterations. ')
            break
    return x

# Range of x given as the input of the function.
# Root wanted in this case is the half of maximum value of N(x).

x_space = np.arange(1.e-4, 5, 0.001)
half_max = max(N(x_space))/2
root=bisection(1.e-4, 5, 100, 1.e-9, half_max)

# Save as a text file.
np.savetxt('root_found.txt', [root])
