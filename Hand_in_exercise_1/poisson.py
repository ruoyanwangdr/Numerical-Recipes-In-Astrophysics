import numpy as np

# Factorial function. Raises ValueError if x is not integral or is negative.
def factorial(n):
    """
    The factorial function is defined by the product.
    n! = 1*2*3...*(n-2)*(n-1)*n
    Memory will be limited to 64 bits in this function.
    Too large input int will failed to be converted to float.
    """
    fact = 1

    if n < 0:
        raise ValueError('factorial() not defined for negative values')

    elif type(n) == float:
        raise ValueError('factorial() only accepts integral values')

    else:
        # Limiting memory to at most 64 bits.
        for i in range (1,np.int64(n+1)):
            fact = fact * i

    return float(fact)

# Poisson probability distribution for an integer k, given a positive lambda.
def Poisson(Lambda, k):
    Poisson = (Lambda**k)*(np.e**(-Lambda))/factorial(k)
    return Poisson

# Input values as required.
Lambda = [1,5,3,2.6]
k = [0,10,21,40]

# Save as a text file.
np.savetxt('poisson.txt',[Poisson(Lambda[i],k[i]) for i in range(len(k))])
