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


def generate_points_parallel(N, A, function_number, n,  lock):

    if function_number == 1:
        while True:
            x = f._get_point_func_1(n)
            with lock:
                if len(A) < N:
                    A.append(x)
                else:
                    return
    elif function_number == 2:
        while True:
            x = f._get_point_func_2(n)
            if f._func_2_condition(x, n):
                with lock:
                    if len(A) < N:
                        A.append(x)
                    else:
                        return



def crs2(A_shared, function_number, vec_len):
    A = A_shared[:]
    rn.seed(1)
    iterations = 100000

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

            P[-1] = eval('f.function_' + str(function_number) + '(P[:-1])')

            if P[-1] < M[-1]:
                M = P
                A[i_M] = P
                final_result.append(P[-1])

    return P[-1]
#
# def crs2SM(CPU_num):
# 	FUNCTION_NUMBER = 2
# 	if __name__ == '__main__':
#
# 	    N = 800
#
# 	    manager = multiprocessing.Manager()
# 	    A = manager.list([])
# 	    lock = manager.Lock()
#
# 	    start = time.time()
#
# 	    jobs = []
# 	    for a in range(CPU_num):
# 	        p = multiprocessing.Process(target=generate_points_parallel, args=(N, A, FUNCTION_NUMBER, lock))
# 	        jobs.append(p)
# 	        p.start()
#
# 	    for proc in jobs:
# 	        proc.join()
# 	    start2=time.time()
# 	    result = crs2(A, FUNCTION_NUMBER)
# 	    plik=open("wynikiCRS2SM.txt","a")
# 	    plik.write('\nCPU:' + str(CPU_num) +'\n')
# 	    plik.write('f_num: ' + str(FUNCTION_NUMBER)+"\n")
# 	    plik.write('n: ' + str(f.n)+"\n")
# 	    plik.write('Result: {} \n'.format(result))
# 	    plik.write('CRS2 SM FULL Time: {} \n'.format(time.time() - start))
# 	    plik.write('CRS2 SM Iteration Time: {}+\n'.format(time.time() - start2))
# 	    plik.close()
#

def CRS2_multi(cpu_num, FUNCTION_NUMBER, vec_len):

    start_rand = time.time()
    N = 800
    manager = multiprocessing.Manager()
    A = manager.list([])
    lock = manager.Lock()

    jobs = []
    for a in range(cpu_num):
        p = multiprocessing.Process(target=generate_points_parallel, args=(N, A, FUNCTION_NUMBER, vec_len, lock))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    start_iter = time.time()
    result = crs2(A, FUNCTION_NUMBER, vec_len)
    end = time.time()


    iter_time = end - start_iter
    rand_time = start_iter - start_rand
    full_time = end - start_rand

    return(iter_time, rand_time, full_time, result)