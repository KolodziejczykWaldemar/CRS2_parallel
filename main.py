import random as rn
import time
import numpy as np
import helpers as hp
import functions as f


n = 10
lower_bound = -40
upper_bound = 40
rn.seed(1)
N = 800


def get_point():
    x = [rn.random()*2*upper_bound+lower_bound for i in range(n)]
    y = f.function_1(x)
    x.append(y)
    return x


def get_centroid(x):
    return (np.sum(np.array(x), axis=0)/len(x)).tolist()


def get_P(centroid, R_n_plus_1):
    doubled_G = [2*x for x in centroid]
    return [doubled_G[i] - R_n_plus_1[i] for i in range(len(centroid))]


def is_P_in_V(P):
    for x in P[:-1]:
        if x > upper_bound or x < lower_bound:
            return False
    return True


start = time.time()

final_result = list()

A = [get_point() for i in range(N)]

for iteration in range(20000):

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
            final_result.append(P[-1])

    if iteration % 100 == 0:
        print(str(iteration) + ' Kolejna wartość P' + str(P))

        if iteration//100 < 10:
            f_name = 'results/CRS2_00{}'.format(iteration//100)
        elif iteration//100 < 100:
            f_name = 'results/CRS2_0{}'.format(iteration//100)
        else:
            f_name = 'results/CRS2_{}'.format(iteration//100)

        hp.plot_3d_scatter(whole_set=A, centroid=centroid, r_last=R_n_plus_1, optimum=P, f_name=f_name)

hp.plot_convergence(final_result)

print('M: '+str(M))
print('L: '+str(L))
print('centroid: '+str(centroid))
print('P: '+str(P))
print(str(time.time()-start)+' s')


