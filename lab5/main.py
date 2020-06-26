import numpy as np
from math import fabs
import pickle

from model import *
from visualization import draw_graphs, overlay_graphs

# Прогонка
def get_T_new(T_prev, t):
    A_list, B_list, C_list, F_list = get_coeffs(T_prev)
    K0, M0, P0 = left_boundary_condition(T_prev, t)
    KN, MN, PN = right_boundary_condition(T_prev)

    ksi = [-M0 / K0]
    eta = [P0 / K0]

    n = len(A_list)
    for i in range(n):
        denominator = B_list[i] - A_list[i] * ksi[i]
        ksi.append(C_list[i] / denominator)
        eta.append((F_list[i] + A_list[i] * eta[i]) / denominator)

    T_new = [0] * (n + 2)
    T_new[-1] = (PN - MN * eta[i]) / (KN + MN * ksi[i])

    for i in range(len(ksi) - 1, -1, -1):
        T_new[i] = ksi[i] * T_new[i+1] + eta[i]

    return T_new


def get_result():
    res = []
    curr_T = [T0 for i in np.arange(0, l, x_step)]

    res.append(curr_T)

    t = t_step
    t_total = t
    while True:
        if t >= period:
            t_values.append(t)
            t = 0
        T_prev = curr_T

        max_diff = 1
        while max_diff > eps:
            T_new = get_T_new(T_prev, t)

            max_diff = 0
            for i in range(len(T_prev)):
                diff = fabs((T_new[i] - T_prev[i]) / T_new[i])
                if max_diff < diff:
                    max_diff = diff

            T_prev = T_new

        curr_T = T_new
        res.append(T_new)

        update_t_values(t_step)
        t += t_step
        t_total += t_step

        if t_total > t_last:
            break

    return res


if __name__ == '__main__':
    # Вычисление результата
    res = get_result()
    #f = open("test_something.pickle", "wb")
    #pickle.dump(res, f)
    #f.close()

    # Отображение графиков
    draw_graphs(res, l, t_last, x_step, t_step)

    print()
