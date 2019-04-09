import numpy as np
import matplotlib.pyplot as plt
from integration import n, n_1d

# Create x and n lists for plotting.
x_range = [1.e-4, 1.e-2, 1.e-1, 1, 5]
n_x = []

# Append values and save them for plotting.
for i in range(len(x_range)):
    n_x.append(n(x_range[i]))

# Define the natural cubic spline method.
def cubic_spline(x, y, N):
    """
    x     ... input x value
    y     ... funtion of x
    N     ... number of fits (bigger the more accurate but slower)

    Choose interpolation method to be cubic spline.
    Natural cubic spline is a piece-wise interpolation method with low-degree polynomials, which will prevent excessive oscillations
    and non-convergence. In this problem, we have nearly a linear log fit and the number of data points is only 5, meaning that the
    degree of polynomials will be low and the interpolation will be relatively accurate.


    """

    # Initial setup.
    n = len(x)
    f = np.zeros(n)
    u = np.zeros(n)

    # The formula goes to N-2, so extend two more datapoints.
    xout = np.zeros(N+2)
    yout = np.zeros(N+2)

    # Define a polynomial to fit up to n orders.
    poly_nd = (y[n-1] - y[n-2])/(x[n-1] - x[n-2]) - (y[n-2] - y[n-3])/(x[n-2] -
          x[n-3]) + (y[n-1] - y[n-3])/(x[n-1] - x[n-3])

    # LU decomposition loop.
    for i in range(1, n-1):
        sigma = (x[i] - x[i-1])/(x[i+1] - x[i-1])
        P = sigma*f[i-1] + 2.
        f[i] = (sigma - 1.)/P
        u[i] = (y[i+1] - y[i])/(x[i+1] - x[i]) - (y[i] - y[i-1])/(x[i] - x[i-1])
        u[i] = (6.*u[i]/(x[i + 1] - x[i - 1]) - sigma*u[i - 1])/P
        qn = 0.5
        un = (3./(x[n-1]-x[n-2]))*(poly_nd-(y[n-1]-y[n-2])/(x[n-1]-x[n-2]))

    f[n-1] = (un - qn*u[n-2])/(qn*f[n-2] + 1.)

    for k in range(n-2, 1, -1):
        f[k] = f[k]*f[k+1] + u[k]

    # Initialization ends, begin fit.
    for i in range(1, N+2):
        xout[i] = x[0] + (x[n-1] - x[0])*(i-1)/(N)

        # Use bisection method to find the interval between x_j and x_{j+1}.
        j = 0;    j_plus_1 = n-1
        while (j_plus_1 - j >1):
            k = (j_plus_1 + j) >> 1
            if (x[k] > xout[i]):
                j_plus_1  = k
            else:
                j = k

        if (x[k] > xout[i]):
            j_plus_1 = k
        else:
            j = k

        # Apply the interpolation formula. Acquired from page 121 of the textbook.
        h = x[j_plus_1] - x[j]
        A = (x[j_plus_1] - xout[i])/h
        B = (xout[i] - x[j])/h
        C = (A**3-A)*(h**2)/6.
        D = (B**3-B)*(h**2)/6.
        yout[i] = A*y[j] + B*y[j_plus_1] + C*f[j] + D*f[j_plus_1]

    # The first index of the output will be zero since everything starts there,
    # so taking the index number starting from one.
    return xout[1:], yout[1:]

# Perform interpolation.
interp_density = cubic_spline(x_range, n_x, 1000)

# Plot log-log of n(x) and its interplolation.
plt.xlabel('log(x)')
plt.ylabel('log(n)')
plt.xscale('log') # log scale for x
plt.yscale('log') # log scale for y
plt.scatter(x_range, n_x, alpha=0.5, label='Data Points')
plt.plot(interp_density[0], interp_density[1], 'r', label='Interplolation')
plt.legend()
plt.savefig('./plots/interpolation.png')
plt.close()

# Save as a text file.
np.savetxt('density_profile.txt', np.transpose([x_range, n_x]))
