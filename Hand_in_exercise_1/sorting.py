import numpy as np
import matplotlib.pyplot as plt
from poisson import Poisson
from log_hist import one_thousand_haloes, all_radii, bin_radii, average_num_of_sat

# Choose the sorting method to be Mergesort.
def mergesort(array):
    if len(array) > 1:
        # Break the array up into a left and right half.
        mid_point = int(len(array)/2)
        left_half = array[:mid_point]
        right_half = array[mid_point:]

        # Repeat the above process recursively until single elements.
        mergesort(left_half)
        mergesort(right_half)

        # Merge pairs of adjacent sub-arrays while putting their elements in order
        left_idx = 0
        right_idx = 0
        array_idx = 0

        while left_idx < len(left_half) and right_idx < len(right_half):
            if left_half[left_idx] < right_half[right_idx]:
                array[array_idx] = left_half[left_idx]
                left_idx += 1
            else:
                array[array_idx] = right_half[right_idx]
                right_idx += 1
            array_idx += 1

        # If number of elements is odd, check whether the extra element is in the
        # left or right half, and then add it the sorted list.
        while left_idx < len(left_half):
            array[array_idx] = left_half[left_idx]
            left_idx += 1
            array_idx += 1

        while right_idx < len(right_half):
            array[array_idx] = right_half[right_idx]
            right_idx += 1
            array_idx += 1

        # Return the sorted array.
        return array

# Define median calculator.
def median(lst):
    # Split the input array into two halves.
    quotient, remainder = divmod(len(lst), 2)
    # If N is odd, then that is our median.
    if remainder:
        return mergesort(lst)[quotient]
    # If not, we sort our array and find the two points in the middle and take the average.
    return float(sum(mergesort(lst)[quotient - 1:quotient + 1]) / 2)

# Define quantile function.
def quantile(lst, per):
    # If array is sorted, array[x*N] = xth percentile.
    i = int(0.01*per*len(lst))
    quant = mergesort(lst)[i]
    return quant


# Get the radial bin containing the largest number of galaxies.
def largest_radial_bin(values, bin_values):
    """
    Take the radial bin from 1000 haloes and find the one that contains the largest
    number. In my case the biggest bin is the 18th bin due to my choice of seed.
    """

    largest_bin = values[np.where((values>bin_values[18])*(values<bin_values[19]))]

    return largest_bin

largest_rad_bin = largest_radial_bin(all_radii, bin_radii[1])

# Counting the number of galaxies in this radial bin in each halo.
def counting_galaxies_in_halo(input_bin, halo_bin):
    number = np.zeros(len(halo_bin))
    for i in range(len(halo_bin)):
        # Find the intersection between the two sets.
        number[i] = len(list(set(input_bin) & set(halo_bin[i])))
    return number

num_galaxies_in_halo = counting_galaxies_in_halo(largest_rad_bin, one_thousand_haloes[0])

# Get the Poisson distribution, where lambda equals to the mean number of galaxies
# in the radial bin that contains the largest number of galaxies.
Poisson_galaxies = []
for i in range(20,55):
    Poisson_galaxies.append(Poisson(max(average_num_of_sat), i))

# Plot the histogram and the Poisson distribution.
plt.xlabel('Bins')
plt.ylabel('Normalized Counts')
plt.plot(range(20,55), Poisson_galaxies, label='Poisson')
plt.hist(num_galaxies_in_halo, bins=range(20,55), density=True, label='Number of galaxies')
plt.legend()
plt.savefig('./plots/sorting_Poisson.png')
plt.close()

# Calculate the median, 16th, and 84th percentile of the input radial bin.
largest_rad_bin_median = median(largest_rad_bin)
largest_rad_bin_16_percentile = quantile(largest_rad_bin,16)
largest_rad_bin_84_percentile = quantile(largest_rad_bin,84)

# Save as a text file.
np.savetxt('sorting.txt',\
    np.transpose([largest_rad_bin_median,\
    largest_rad_bin_16_percentile,\
    largest_rad_bin_84_percentile]))
