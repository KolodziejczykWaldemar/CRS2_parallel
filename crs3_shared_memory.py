import random as rn
import time
import numpy as np
import helpers as hp
import functions as f
import multiprocessing


def get_G(x):
    return (np.sum(np.array(x), axis=0)/len(x)).tolist()


def get_P(centroid, w):
    doubled_G = [2*x for x in centroid]
    return [doubled_G[i] - w[i] for i in range(len(centroid))]


def get_Q(centroid, w):
    added = [centroid[i] + w[i] for i in range(len(centroid))]
    return [0.5*x for x in added]


def get_R(centroid, w):
    return [4*centroid[i] - 3*w[i] for i in range(len(centroid))]


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


def crs3(A_shared, function_number, vec_len):

    A = A_shared[:]
    rn.seed(1)
    iterations = 100000

    final_result = list()

    for iteration in range(iterations):

        i_W = np.argmax(np.array(A).T[-1])
        W = A[i_W]

        A_exclude_W = A.copy()
        A_exclude_W.remove(W)

        R_chosen = rn.sample(A_exclude_W, vec_len)

        i_S = np.argmax(np.array(A_exclude_W).T[-1])
        S = A_exclude_W[i_S]

        centroid = get_G(R_chosen)

        P = get_P(centroid, W)
        Q = get_Q(centroid, W)
        R = get_R(centroid, W)

        if f.is_point_in_domain(P):

            P[-1] = eval('f.function_' + str(function_number) + '(P[:-1])')

            if P[-1] < S[-1]:
                if not f.is_point_in_domain(R):
                    W = P
                    A[i_W] = P
                    final_result.append(P[-1])
                else:
                    R[-1] = eval('f.function_' + str(function_number) + '(R[:-1])')
                    if R[-1] < S[-1]:
                        W = R
                        A[i_W] = R
                        final_result.append(R[-1])
                    else:
                        W = P
                        A[i_W] = P
                        final_result.append(P[-1])
        else:
            if not f.is_point_in_domain(Q):
                continue
            else:
                Q[-1] = eval('f.function_' + str(function_number) + '(Q[:-1])')
                if Q[-1] < S[-1]:
                    W = Q
                    A[i_W] = Q
                    final_result.append(Q[-1])
                else:
                    continue

    return final_result[-1]

# def crs3SM(CPU_num):
# 	FUNCTION_NUMBER = 2
# 	N = 800
# 	     # tutaj trzeba zmienić numer w zależności od funkcji
#
# 	manager = multiprocessing.Manager()
# 	A = manager.list([])
# 	lock = manager.Lock()
#
# 	start = time.time()
#
# 	jobs = []
# 	for a in range(CPU_num):
# 		p = multiprocessing.Process(target=generate_points_parallel,args=(N, A, lock))
# 	jobs.append(p)
# 	p.start()
#
# 	for proc in jobs:
# 		proc.join()
#
#
# 	start2=time.time()
# 	result = crs3(A)
# 	plik=open("wynikiCRS3SM.txt","a")
# 	plik.write('\nCPU:' + str(CPU_num) +'\n')
# 	plik.write('f_num: ' + str(FUNCTION_NUMBER)+"\n")
# 	plik.write('n: ' + str(f.n)+"\n")
# 	plik.write('Result: {} \n'.format(result))
# 	plik.write('CRS3 SM FULL Time: {} \n'.format(time.time() - start))
# 	plik.write('CRS3 SM Iteration Time: {}+\n'.format(time.time() - start2))
# 	plik.close()


def CRS3_multi(cpu_num, FUNCTION_NUMBER, vec_len):

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
    result = crs3(A, FUNCTION_NUMBER, vec_len)
    end = time.time()

    iter_time = end - start_iter
    rand_time = start_iter - start_rand
    full_time = end - start_rand

    return (iter_time, rand_time, full_time, result)
