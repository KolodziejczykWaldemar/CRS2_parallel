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


def generate_points_func_2_parallel(N, A, lock):

    while True:
        x = f._get_point_func_2()
        if f._func_2_condition(x):
            with lock:
                if len(A) < N:
                    A.append(x)
                else:
                    return

def generate_points_func_1_parallel(N, A, lock):

    while True:
        x = f._get_point_func_1()
        with lock:
            if len(A) < N:
                A.append(x)
            else:
                return



def crs2(A_shared):
    A = A_shared[:]
    rn.seed(1)
    iterations = 20000

    final_result = list()

    for iteration in range(iterations):

        i_M = np.argmax(np.array(A).T[-1])
        i_L = np.argmin(np.array(A).T[-1])
        M = A[i_M]
        L = A[i_L]

        A_exclude_L = A.copy()
        A_exclude_L.remove(L)

        R_chosen = rn.sample(A_exclude_L, f.n)
        R_n_plus_1 = R_chosen.pop()
        centroid = get_centroid(R_chosen)
        P = get_P(centroid, R_n_plus_1)

        if f.is_point_in_domain(P):

            P[-1] = eval('f.function_' + str(FUNCTION_NUMBER) + '(P[:-1])')

            if P[-1] < M[-1]:
                M = P
                A[i_M] = P
                final_result.append(P[-1])

    return P[-1]


if __name__ == '__main__':

    CPU_num = 4
    N = 800
    FUNCTION_NUMBER = 1  # tutaj trzeba zmienić numer w zależności od funkcji

    manager = multiprocessing.Manager()
    A = manager.list([])
    lock = manager.Lock()

    start = time.time()

    jobs = []
    for a in range(CPU_num):
        p = multiprocessing.Process(target=generate_points_func_1_parallel, args=(N, A, lock)) # tutaj trzeba zmienić numer w zależności od funkcji
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    result = crs2(A)
    print('Result: {}'.format(result))
    print('Time: {}'.format(time.time() - start))