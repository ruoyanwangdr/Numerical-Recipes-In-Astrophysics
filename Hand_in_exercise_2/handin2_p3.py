import numpy as np
import matplotlib.pyplot as plt

# Give the parameters.
H0 = 7.16e-11 # [yr^-1]
omega_0 = 1

# Define a and time-derivative of a.
a = lambda t: ((3/2)*H0*t)**(2/3)
a_dot = lambda t: H0*((3/2)*H0*t)**(-1/3)

# Define the function to be solved.
def ode(t, y):

    """
    y ... A vector function containing D and dD/dt
    t ... time to integrate over

    """

    # Define the initial conditions. Will assign values later.
    D , dD_dt = y[0], y[1]

    d2D_dt2 = -2*(a_dot(t)/a(t))*dD_dt + (3/2)*omega_0*(H0**2)*(D/(a(t)**3))

    return np.array([dD_dt, d2D_dt2])

# define the solver method.
def rk4(ode,y,t,h):

    """
    ode ... ordinary differential equation to solve
    y   ... A vector fucntion containing D and dD/dt
    t   ... time to integrate over
    h   ... integration step

    Method using here is the classic Runge-Kutta (4-th order), acquired L10.

    """

    k1 = h * ode(t, y)
    k2 = h * ode(t+h/2., y+k1/2.)
    k3 = h * ode(t+h/2., y+k2/2.)
    k4 = h * ode(t+h, y+k3)

    return k1/6. + k2/3. + k3/3. + k4/6.

# Define the ode solver.
def ode_solver(init, lower, upper, N):

    # Define the integration step.
    h = (upper-lower)/N

    # Define initial conditions and assign values.
    y, t_values, D_values = init, [], []

    # Solve the ode using rk4.
    for i in np.arange(lower, upper, h):
        t_values.append(i)
        D_values.append(y[0])
        y += rk4(ode,y,i,h)

    return t_values, D_values


# Define the time range and number of data points.
t_init, t_final, t_step = 1., 1000., 10
N = (t_final-t_init)*t_step

# Plot given the initial conditions.
plt.figure()

case1, case2, case3 = [3,2], [10,-10], [5,0]
all_cases = [[case1,'case1'], [case2,'case2'], [case3,'case3']]

for i in range(len(all_cases)):
    t_values, D_values = ode_solver(all_cases[i][0], t_init, t_final, N)
    plt.loglog(t_values, D_values, label=all_cases[i][1])

plt.xlabel('t', fontsize=14)
plt.ylabel('D(t)', fontsize=14)
plt.legend()

plt.savefig('./plots/handin2_p3.png')
plt.close()
