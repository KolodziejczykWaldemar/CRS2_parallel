import math as mt


def function_1(x):
    sum_x = sum([arg**2 for arg in x])
    multi = mt.cos(x[0])
    for i in range(len(x)-1):
        multi *= mt.cos(x[i+1]/(i+2))
    return sum_x/40 + 1 - multi


def function_2(x):
    sum_x = 0
    for i in range(len(x)-1):
        sum_x += (x[i+1] - x[i]**2)**2 + (1 - x[i])**2
    return sum_x
