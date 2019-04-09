import numpy as np
import matplotlib.pyplot as plt
from random_generator import xor_shift_64
from integration import a, b, c, A
from interpolation import x_range

# Choose sampling method to be rejection.
def rejection_sampling(function, x_min, x_max, y_min, y_max, N_sample):
    """
    function         ... weighting function to put in
    [x_min, x_max]   ... range of x
    [y_min, y_max]   ... range of y
    N_sample         ... number of sample points

    Sample a point on the x-axis from the proposal distribution.
    Draw a vertical line at this x-position, up to the curve of the proposal distribution.
    Sample uniformly along this line from 0 to the maximum of the probability density function.
    If the sampled value is greater than the value of the desired distribution at this vertical line,
    repeat the first step until reaching number of data points wanted.
    """

    # Create empty sample arrays and assign values later.
    data_x = np.empty(N_sample)
    data_y = np.empty(N_sample)

    # Sample points counter.
    accepted = 0

    # Selection process.
    while accepted < N_sample:

        # Generate random x and y values in the given range.
        test_x = (x_max-x_min)*xor_shift_64()+x_min
        test_y = (y_max-y_min)*xor_shift_64()+y_min

        # Apply rejection method.
        # Taking only points below the curve.
        if test_y <= weight(test_x):
            data_x[accepted] = test_x
            data_y[accepted] = test_y
            accepted += 1

    return data_x, data_y

# Define weighting function.
weight = lambda x: A*4*np.pi*x**2*(x/b)**(a-3)*np.e**(-(x/b)**c)

# Sample the distribution.
sample_x, sample_y = rejection_sampling(weight,
                                        0,
                                        5,
                                        min(weight(np.arange(x_range[0], x_range[-1], 0.001))),
                                        max(weight(np.arange(x_range[0], x_range[-1], 0.001))),
                                        10000)

# Plot the sampling.
plt.xlabel('x')
plt.ylabel('p(x)')
plt.plot(np.arange(0, 5, 0.001), weight(np.arange(x_range[0], x_range[-1], 0.001)), 'r', label='n(x)')
plt.scatter(sample_x, sample_y, s=1, label='Sampled Data')
plt.legend()
plt.savefig('./plots/rejection_sampling.png')
plt.close()


# Define a function to generate r, phi, and theta in one halo.
def one_halo(n_satellite):
    """
    n_satellite     ... number of satellites wanted to generate

    Radii of satellites are choosen from a random sample of data
    points selected by the rejection sampling, while phi and theta
    are generated randomly from ranges [0, 2pi] and [0, pi].
    """
    r_sat = rejection_sampling(weight, 0, 5,
                               min(weight(np.arange(x_range[0], x_range[-1], 0.001))),
                               max(weight(np.arange(x_range[0], x_range[-1], 0.001))),
                               1000)[0][0:n_satellite]
    phi_sat = np.zeros(n_satellite)
    theta_sat = np.zeros(n_satellite)

    for i in range(n_satellite):
        phi_sat[i] = (2*np.pi-0)*xor_shift_64()
        theta_sat[i] = (np.pi-0)*xor_shift_64()
    return r_sat, theta_sat, phi_sat

# Generate 100 satellites.
one_halo_100_sat = one_halo(100)

# Save positions of satellites in a text file.
np.savetxt('positions.txt', \
    np.transpose([one_halo_100_sat[0],one_halo_100_sat[1],one_halo_100_sat[2]]))
