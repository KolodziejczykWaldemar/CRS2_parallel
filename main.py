import random as rn
import math as mt
import time
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import helpers as hp


n = 10
low = -40
high = 40
rn.seed(1)
N = 800


def function_1(x):
    sum_x = sum([arg**2 for arg in x])
    multi = mt.cos(x[0])
    for i in range(len(x)-1):
        multi *= mt.cos(x[i+1]/(i+2))
    return sum_x/40 + 1 - multi


def function_2(x):
    sum_x = 0
    for i in range(len(x)-1):
        sum_x += (x[i+1] - x[i]**2)**2 + (1 - x[i])**2
    return sum_x


def get_point():
    x = [rn.random()*2*high+low for i in range(n)]
    y = function_1(x)
    x.append(y)
    return x


def get_centroid(x):
    return (np.sum(np.array(x), axis=0)/len(x)).tolist()


def get_P(centroid, R_n_plus_1):
    doubled_G = [2*x for x in centroid]
    return [doubled_G[i] - R_n_plus_1[i] for i in range(len(centroid))]


def is_P_in_V(P):
    for x in P[:-1]:
        if x > high or x < low:
            return False
    return True


start = time.time()

WYNIK = list()

A = [get_point() for i in range(N)]

for iteration in range(200000):

    i_M = np.argmax(np.array(A).T[-1])
    i_L = np.argmin(np.array(A).T[-1])
    M = A[i_M]
    L = A[i_L]

    A_exclude_L = A.copy()
    A_exclude_L.remove(L)

    R_chosen = rn.sample(A_exclude_L, n)
    R_n_plus_1 = R_chosen.pop()
    centroid = get_centroid(R_chosen)
    P = get_P(centroid, R_n_plus_1)

    if is_P_in_V(P):

        P[-1] = function_1(P[:-1])

        if P[-1] < M[-1]:
            M = P
            A[i_M] = P
            WYNIK.append(P[-1])

    if iteration % 100 == 0:
        print(str(iteration) + ' Kolejna wartość P' + str(P))

        if iteration//100 < 10:
            f_name = 'results/CRS2_00{}'.format(iteration//100)
        elif iteration//100 < 100:
            f_name = 'results/CRS2_0{}'.format(iteration//100)
        else:
            f_name = 'results/CRS2_{}'.format(iteration//100)

        hp.plot_3d_scatter(whole_set=A, centroid=centroid, r_last=R_n_plus_1, optimum=P, f_name=f_name)

end = time.time()
plt.plot(WYNIK)
plt.show()

print('M: '+str(M))
print('L: '+str(L))
print('centroid: '+str(centroid))
print('P: '+str(P))
print(str(end-start)+' s')


