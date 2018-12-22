import random as rn
import time
import numpy as np
import helpers as hp
import functions as f


FUNCTION_NUMBER = 2

rn.seed(1)
N = 800
iterations = 100000


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

def crs3():
	final_result = list()
	start = time.time()
	A = eval('f.generate_points_func_' + str(FUNCTION_NUMBER) + '(N)')
	start2=time.time()
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

	plik=open("wynikiCRS3.txt","a")
	plik.write('\nf_num' + str(FUNCTION_NUMBER) +'\n')
	plik.write('n: ' + str(f.n)+"\n")
	plik.write('P: '+str(P)+"\n")
	plik.write("CRS3 FULL Time " + str(time.time()-start)+' s'+"\n")
	plik.write("CRS3 iteration Time " + str(time.time()-start2)+' s'+"\n")
	plik.close()

