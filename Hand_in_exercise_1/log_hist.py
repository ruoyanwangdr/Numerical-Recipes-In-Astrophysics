import numpy as np
import matplotlib.pyplot as plt
from integration import n
from sampling import one_halo


# Define N(x).
def N(x):
    return n(x)*4*np.pi*x**2

# Generate multiple haloes.
def multi_halo(n_halo):
    """
    This routine will repeat the halo generator as many times
    as the input number to get equivalent amount of haloes.
    """
    r_halo = []
    phi_halo = []
    theta_halo = []

    for i in range(n_halo):
        r, theta,phi = one_halo(100)
        r_halo.append(r)
        theta_halo.append(theta)
        phi_halo.append(phi)

    return r_halo, theta_halo, phi_halo

# Save 1000 haloes for later use.
one_thousand_haloes = multi_halo(1000)

# Convert ndarrays into 1darray and bin them in 20 logarithmic spaces.
all_radii = np.concatenate(one_thousand_haloes[0])
bin_radii = np.histogram(all_radii, bins=np.logspace(np.log10(1.e-4),np.log10(5.0), 21))

# Calculate the average number in each bin.
def average_number_of_satellites(bin_values, bins):
    """
    Calculate the average number of galaxies in each bin by dividing the sum of
    satellites in the bins to get the mean. Since the bins are in logarithmic
    space, the average number is then normalized back to the original scale by
    dividing the bin width.
    """

    average_number = np.zeros(len(bin_values))

    for idx, value in enumerate(bin_values):
        normalized_average = (value/len(one_thousand_haloes[0])) / (bins[idx+1] - bins[idx])
        average_number[idx] = (normalized_average)

    return np.array(average_number)

# Calculate the average number of satellites. 
average_num_of_sat = average_number_of_satellites(bin_radii[0], bin_radii[1])

# Convert the x scale of the histogram to log.
log_spaced_x = np.logspace(np.log10(1.e-4), np.log10(5.0), 20)

# Plot log-log of N(x) and over-plot a histogram of average numer in each bin.
plt.xlabel('log(x)')
plt.ylabel('log(N)')
plt.xscale('log') # log scale for x
plt.yscale('log') # log scale for y
plt.plot(np.arange(1.e-4, 5, 0.001), N(np.arange(1.e-4, 5, 0.001)), 'r', label='N(x)')
plt.hist(log_spaced_x, weights=average_num_of_sat, bins=np.logspace(np.log10(1.e-4), np.log10(5.0), 21), label='Average Number of Satellites')
plt.legend()
plt.savefig('./plots/log_hist.png')
plt.close()
