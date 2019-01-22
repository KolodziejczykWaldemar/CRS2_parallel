import random as rn
import time
import numpy as np
import helpers as hp
import functions as f
import multiprocessing


def get_centroid(x):
    return (np.sum(np.array(x), axis=0)/len(x)).tolist()


def get_P(centroid, R_n_plus_1):
    doubled_G = [2*x for x in centroid]
    return [doubled_G[i] - R_n_plus_1[i] for i in range(len(centroid))]


def crs2(A, return_list, function_number, vec_len):

    rn.seed(1)
    iterations = 20000
    final_result = list()


    CLOSE_ENOUGH = 10e-4
    WANTED_RESULT = 0
    last_P_value = 10e4

    for iteration in range(iterations):
    # while abs(last_P_value - WANTED_RESULT) > CLOSE_ENOUGH:

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

            P[-1] = eval('f.function_' + str(function_number) + '(P[:-1])')

            if P[-1] < M[-1]:
                M = P
                A[i_M] = P
                final_result.append(P[-1])

                last_P_value = P[-1]

    return_list.append(P[-1])


def CRS2_local(cpu_num, FUNCTION_NUMBER, vec_len):

    N = 800
    start_rand = time.time()
    A = eval('f.generate_points_func_' + str(FUNCTION_NUMBER) + '(N, vec_len)')
    A_chunked = hp.chunk_list(A, cpu_num)

    start_iter = time.time()
    manager = multiprocessing.Manager()
    return_list = manager.list()
    jobs = []
    for a in A_chunked:
        p = multiprocessing.Process(target=crs2, args=(a, return_list, FUNCTION_NUMBER, vec_len))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    end = time.time()

    iter_time = end - start_iter
    rand_time = start_iter - start_rand
    full_time = end - start_rand

    return iter_time, rand_time, full_time, min(list(return_list))