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

FUNCTION_NUMBER = 2


def crs3(A, return_list):

    rn.seed(1)
    iterations = 20000
    start = time.time()

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
    #
    #     if iteration % 100 == 0:
    #         print(str(iteration) + ' Kolejna wartość P' + str(P))
    #
    #         if iteration//100 < 10:
    #             f_name = 'results/CRS2_00{}'.format(iteration//100)
    #         elif iteration//100 < 100:
    #             f_name = 'results/CRS2_0{}'.format(iteration//100)
    #         else:
    #             f_name = 'results/CRS2_{}'.format(iteration//100)
    #
    #         hp.plot_3d_scatter(whole_set=A,
    #                            centroid=centroid,
    #                            r_last=W,
    #                            optimum=P,
    #                            f_name=f_name,
    #                            func_number=FUNCTION_NUMBER)
    #
    # hp.plot_convergence(final_result)

    return_list.append(P[-1])


if __name__ == '__main__':

    CPU_num = 4
    N = 800
    FUNCTION_NUMBER = 1
    A = eval('f.generate_points_func_' + str(FUNCTION_NUMBER) + '(N)')
    A_chunked = hp.chunk_list(A, CPU_num)

    start = time.time()
    manager = multiprocessing.Manager()
    return_list = manager.list()
    jobs = []
    for a in A_chunked:
        p = multiprocessing.Process(target=crs3, args=(a, return_list))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    print(return_list)
    print(time.time() - start)