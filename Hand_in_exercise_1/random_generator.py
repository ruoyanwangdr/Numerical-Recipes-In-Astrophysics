import numpy as np
import matplotlib.pyplot as plt

# Set seed. Fixed during the entire run.
I0=283947129834792

# All three methods from lecture slides are combined by setting
# the output of the previous method as the input the following method.

# (Multip.) Linear Congruential Generators.
def lcg(I=I0, m=2**64-1, a=56675949247, c=10139042236):

    global I0
    I0 = (a*I0 + c) % m
    return I0

# Multiply with Carry (MWC) with base b = 2**32.
# Parameters acquired from lecture slides.
def mwc(a=4294957665):

    # Use the output of LCG as the input of MWC.
    n = a*(lcg() & (2**32-1))+(lcg()>>32)
    return n

# 64-bit XOR-shift.
# Parameters acquired from lecture notes.
def xor_shift_64(a1=21, a2=35, a3=4, P=2**64-1, ):

    # Use the output of MWC as the input of XOR-shift.
    X = mwc()
    Y = mwc()
    Z = mwc()
    W = mwc()

    # Set to 64-bit.
    bit64 = 0xffffffffffffffff

    t = X^(X<<a2) & bit64 # Keep in 64-bit.
    X = Y
    Y = Z
    Z = W
    W = W^(W>>a1)^t^(t>>a3) & bit64 # Keep in 64-bit.

    return W / P # Gernerate numbers between 0 and 1.

# Create two zeros arrays and assign x_i and x_i+1 with 1000 random numbers.
x_i = np.zeros(1000)
x_i_plus_1 = np.zeros(1000)
for i in range(len(x_i)):
    x_i[i] = xor_shift_64()
    x_i_plus_1[i] = xor_shift_64()

# Plot x_i vs x_i+1 for the first 1000 numbers generated.
plt.xlabel('x$_{\mathrm{i}}$')
plt.ylabel('x$_{\mathrm{i+1}}$')
plt.scatter(x_i, x_i_plus_1, alpha=0.5)
plt.savefig('./plots/one_thousand_random_numbers.png')
plt.close()

# Create an zeros array and assign 1000000 random numbers.
one_million = np.zeros(1000000)
for i in range(len(one_million)):
    one_million[i] = xor_shift_64()

# Put 1000000 random numbers in 20 bins with 0.05 wide and plot them.
plt.xlabel('Bins')
plt.ylabel('Number of Data Points')
plt.hist(one_million, bins=20)
plt.savefig('./plots/one_million_random_numbers.png')
plt.close()
