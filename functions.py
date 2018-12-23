import math as mt
import random as rn

upper_bound = 40
lower_bound = -40


def is_point_in_domain(p):
    for x in p[:-1]:
        if x > upper_bound or x < lower_bound:
            return False
    return True


# -----------------------------FIRST_FUNCTION---------------------------------------------------------------------------
def function_1(x):
    sum_x = sum([arg**2 for arg in x])
    multi = mt.cos(x[0])
    for i in range(len(x)-1):
        multi *= mt.cos(x[i+1]/(i+2))
    return sum_x/40 + 1 - multi


def generate_points_func_1(N, n):
    return [_get_point_func_1(n) for i in range(N)]


def _get_point_func_1(n):
    x = [rn.random()*2*upper_bound+lower_bound for i in range(n)]
    y = function_1(x)
    x.append(y)
    return x


# -----------------------------SECOND_FUNCTION-------------------------------------------------------------------------
def function_2(x):
    sum_x = 0
    for i in range(len(x)-1):
        sum_x += (x[i+1] - x[i]**2)**2 + (1 - x[i])**2
    return sum_x


def generate_points_func_2(N, n):
    A = list()
    while len(A) != N:
        x = _get_point_func_2(n)
        if _func_2_condition(x, n):
            A.append(x)
    return A


def _get_point_func_2(n):
    x = [rn.random()*2*upper_bound+lower_bound for i in range(n)]
    y = function_2(x)
    x.append(y)
    return x


def _func_2_condition(x, n):
    xx = x[:-1]
    n = len(xx)
    result_sum = 0
    for i, val in enumerate(xx):
        result_sum += (val - i - 1)**2
    if result_sum <= n*10:
        return True
    else:
        return False

