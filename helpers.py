import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_3d_scatter(whole_set, centroid, r_last, optimum, f_name):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = np.array(whole_set).T[0]
    ys = np.array(whole_set).T[1]
    zs = np.array(whole_set).T[2]
    ax.scatter(xs=xs, ys=ys, zs=zs, s=5)
    ax.scatter(xs=centroid[0], ys=centroid[1], zs=centroid[2], label='G', s=40)
    ax.scatter(xs=r_last[0], ys=r_last[1], zs=r_last[2], label='R n+1', s=40)
    ax.scatter(xs=optimum[0], ys=optimum[1], zs=optimum[2], label='P', s=40)
    ax.set_xlim(-80, 80)
    ax.set_ylim(-80, 80)
    ax.set_zlim(0, 20)
    plt.legend()
    plt.savefig(f_name)
    plt.close()
