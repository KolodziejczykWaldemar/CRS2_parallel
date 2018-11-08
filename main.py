import random as rn
import math as mt
import time
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')
    #     xs = np.array(A).T[0]
    #     ys = np.array(A).T[1]
    #     zs = np.array(A).T[2]
    #     ax.scatter(xs=xs, ys=ys, zs=zs, s=5)
    #     ax.scatter(xs=centroid[0], ys=centroid[1], zs=centroid[2], label='G', s=40)
    #     ax.scatter(xs=R_n_plus_1[0], ys=R_n_plus_1[1], zs=R_n_plus_1[2], label='R n+1', s=40)
    #     ax.scatter(xs=P[0], ys=P[1], zs=P[2], label='P', s=40)
    #     ax.set_xlim(-80, 80)
    #     ax.set_ylim(-80, 80)
    #     ax.set_zlim(0, 20)
    #     plt.legend()
    #
    #     if iteration//100 < 10:
    #         f_name = 'results/CRS2_00{}'.format(iteration//100)
    #     elif iteration//100 < 100:
    #         f_name = 'results/CRS2_0{}'.format(iteration//100)
    #     else:
    #         f_name = 'results/CRS2_{}'.format(iteration//100)
    #
    #     plt.savefig(f_name)
    #     plt.close()

end = time.time()
plt.plot(WYNIK)
plt.show()

print('M: '+str(M))
print('L: '+str(L))
print('centroid: '+str(centroid))
print('P: '+str(P))
print(str(end-start)+' s')


