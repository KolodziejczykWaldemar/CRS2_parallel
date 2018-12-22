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


def crs3(A_shared):

    A = A_shared[:]
    rn.seed(1)
    iterations = 100000

    final_result = list()

    for iteration in range(iterations):

        i_W = np.argmax(np.array(A).T[-1])
        W = A[i_W]

        A_exclude_W = A.copy()
        A_exclude_W.remove(W)

        R_chosen = rn.sample(A_exclude_W, f.n)

        i_S = np.argmax(np.array(A_exclude_W).T[-1])
        S = A_exclude_W[i_S]

        centroid = get_G(R_chosen)

        P = get_P(centroid, W)
        Q = get_Q(centroid, W)
        R = get_R(centroid, W)

        if f.is_point_in_domain(P):

            P[-1] = eval('f.function_' + str(FUNCTION_NUMBER) + '(P[:-1])')

            if P[-1] < S[-1]:
                if not f.is_point_in_domain(R):
                    W = P
                    A[i_W] = P
                    final_result.append(P[-1])
                else:
                    R[-1] = eval('f.function_' + str(FUNCTION_NUMBER) + '(R[:-1])')
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
                Q[-1] = eval('f.function_' + str(FUNCTION_NUMBER) + '(Q[:-1])')
                if Q[-1] < S[-1]:
                    W = Q
                    A[i_W] = Q
                    final_result.append(Q[-1])
                else:
                    continue

    return P[-1]

def crs3SM(CPU_num):
	FUNCTION_NUMBER = 2 
	N = 800
	     # tutaj trzeba zmienić numer w zależności od funkcji
	
	manager = multiprocessing.Manager()
	A = manager.list([])
	lock = manager.Lock()
	
	start = time.time()
	
	jobs = []
	for a in range(CPU_num):
		p = multiprocessing.Process(target=generate_points_func_2_parallel,args=(N, A, lock))  # tutaj trzeba zmienić numer w zależności od funkcji
	jobs.append(p)
	p.start()
	
	for proc in jobs:
		proc.join()

    
	start2=time.time()
	result = crs3(A)
	plik=open("wynikiCRS3SM.txt","a")
	plik.write('\nCPU:' + str(CPU_num) +'\n')
	plik.write('f_num: ' + str(FUNCTION_NUMBER)+"\n")
	plik.write('n: ' + str(f.n)+"\n")
	plik.write('Result: {} \n'.format(result))
	plik.write('CRS3 SM FULL Time: {} \n'.format(time.time() - start))
	plik.write('CRS3 SM Iteration Time: {}+\n'.format(time.time() - start2))
	plik.close()
