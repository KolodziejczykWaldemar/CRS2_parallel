import random as rn
import time
import numpy as np
import helpers as hp
import functions as f


def get_centroid(x):
    return (np.sum(np.array(x), axis=0)/len(x)).tolist()


def get_P(centroid, R_n_plus_1):
    doubled_G = [2*x for x in centroid]
    return [doubled_G[i] - R_n_plus_1[i] for i in range(len(centroid))]


def CRS2(FUNCTION_NUMBER, vec_len):
    N = 800
    start_rand = time.time()
    A = eval('f.generate_points_func_' + str(FUNCTION_NUMBER) + '(N, vec_len)')
    rn.seed(1)
    iterations = 100000
    start_iter = time.time()
    final_result = list()

    for iteration in range(iterations):

        i_M = np.argmax(np.array(A).T[-1])
        i_L = np.argmin(np.array(A).T[-1])
        M = A[i_M]
        L = A[i_L]

        A_exclude_L = A.copy()
        A_exclude_L.remove(L)

        R_chosen = rn.sample(A_exclude_L, vec_len)
        R_n_plus_1 = R_chosen.pop()
        centroid = get_centroid(R_chosen)
        P = get_P(centroid, R_n_plus_1)

        if f.is_point_in_domain(P):

            P[-1] = eval('f.function_' + str(FUNCTION_NUMBER) + '(P[:-1])')

            if P[-1] < M[-1]:
                M = P
                A[i_M] = P
                final_result.append(P[-1])

    end = time.time()
    iter_time = end - start_iter
    rand_time = start_iter - start_rand
    full_time = end - start_rand

    return (iter_time, rand_time, full_time, P[-1])

    # if iteration % 100 == 0:
    #     print(str(iteration) + ' Kolejna wartość P' + str(P))

#         if iteration//100 < 10:
#             f_name = 'results/CRS2_00{}'.format(iteration//100)
#         elif iteration//100 < 100:
#             f_name = 'results/CRS2_0{}'.format(iteration//100)
#         else:
#             f_name = 'results/CRS2_{}'.format(iteration//100)
#
#         hp.plot_3d_scatter(whole_set=A,
#                            centroid=centroid,
#                            r_last=R_n_plus_1,
#                            optimum=P,
#                            f_name=f_name,
#                            func_number=FUNCTION_NUMBER)
#
# hp.plot_convergence(final_result)