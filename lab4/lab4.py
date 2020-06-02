# Лабораторная по моделированию №4
# Реализация модели на основе ДУ в частных производных
# с краевыми условиями II и  III рода.

import matplotlib.pyplot as plt
import numpy as np
from math import fabs
from mpl_toolkits.mplot3d import Axes3D


# Исходные данные модели
def k(T):
    return a1 * (b1 + c1 * T**m1)

def c(T):
    return a2 + b2 * T**m2 - (c2 / T**2)

def alpha(x):
    d = (alphaN*l) / (alphaN-alpha0)
    c = - alpha0 * d
    return c / (x-d)

def p(x) :
    return (2/R) * alpha(x)

def f(x): 
    return (2*T0/R) * alpha(x)


def A(T):
    return t/h * approc_minus_half(k, T, t)

def D(T):
    return t/h * approc_plus_half(k, T, t)

def B(x, T):
    return A(T) + D(T) + h*c(T) + h*t*p(x)

def F(x, T):
    return h*t*f(x) + T*h*c(T)


# Простая аппроксимация
def approc_plus_half(func, n, step):
    return (func(n) + func(n + step)) / 2

def approc_minus_half(func, n, step):
    return (func(n) + func(n - step)) / 2


# Краевые условия
# При х = 0
def left_boundary_condition(T_prev):
    T_prev_0 = T_prev[0]
    c_plus = approc_plus_half(c, T_prev_0, t)
    k_plus = approc_plus_half(k, T_prev_0, t)
    c0 = c(T_prev_0)
    
    K0 = h/8 * c_plus + h/4 * c0 + t/h * k_plus + \
         t * h/8 * p(h/2) + t * h/4 * p(0)

    M0 = h/8 * c_plus - t/h * k_plus + t * h/8 * p(h/2)

    P0 = h/8 * c_plus * (T_prev_0 + T_prev[1]) + \
         h/4 * c0 * T_prev_0 + F0 * t + t * h/8 * (3 * f(0) + f(h))

    return K0, M0, P0

# При х = N
def right_boundary_condition(T_prev):
    T_prev_N = T_prev[-1]
    c_minus = approc_minus_half(c, T_prev_N, t)
    k_minus = approc_minus_half(k, T_prev_N, t)
    cN = c(T_prev_N)
    
    KN = h/8 * c_minus + h/4 * cN + t/h * k_minus + t * alphaN + \
         t * h/8 * p(l - h/2) + t * h/4 * p(l)

    MN = h/8 * c_minus - t/h * k_minus + t * h/8 * p(l - h/2)

    PN = h/8 * c_minus * (T_prev_N + T_prev[-2]) + \
         h/4 * cN * T_prev_N + t * alphaN * T0 + t * h/4 * (f(l) + f(l - h/2))

    return KN, MN, PN


def get_T_new(T_prev):
    K0, M0, P0 = left_boundary_condition(T_prev)
    KN, MN, PN = right_boundary_condition(T_prev)

    eps = [0, -M0 / K0]
    eta = [0, P0 / K0]

    x = h
    n = 1
    while (x + h < l):
        T_prev_n = T_prev[n]
        denominator = (B(x, T_prev_n) - A(T_prev_n) * eps[n])
        
        next_eps = D(T_prev_n) / denominator
        next_eta = (F(x, T_prev_n) + A(T_prev_n) * eta[n]) / denominator
        
        eps.append(next_eps)
        eta.append(next_eta)
        
        n += 1
        x += h

    T_new = [0] * (n + 1)
    T_new[n] = (PN - MN*eta[n]) / (KN + MN*eps[n])

    for i in range(n - 1, -1, -1):
        T_new[i] = eps[i+1] * T_new[i+1] + eta[i+1]

    return T_new


# Метод простых итераций
def simple_iter():
    step1 = int(l / h)
    T = [T0] * (step1 + 1)
    T_new = [0] * (step1 + 1)
    ti = 0
    res = []
    res.append(T)
    lent = len(T)

    while True:
        T_prev = T
        while True:
            T_new = get_T_new(T_prev)

            cur_max = fabs((T[0] - T_new[0]) / T_new[0])
            for i in range(lent):
                d = fabs(T[i] - T_new[i]) / T_new[i]
                if d > cur_max:
                    cur_max = d

            if cur_max < 1:
                break
            T_prev = T_new

        res.append(T_new)
        ti += t

        flag_eps_ok = True
        for i in range(lent):
            if fabs((T[i] - T_new[i]) / T_new[i]) > 1e-2:
                flag_eps_ok = False
        if flag_eps_ok:
            break
        T = T_new

    return res, ti


if __name__ == "__main__":
    # Исходные данные
    a1 = 0.0134
    b1 = 1
    c1 = 4.35e-4
    m1 = 1
    a2 = 2.049
    b2 = 0.563e-3
    c2 = 0.528e5
    m2 = 1

    alpha0 = 0.05
    alphaN = 0.01
    l = 10
    T0 = 300
    R = 0.5
    F0 = 50

    h = 1e-3
    t = 1

    # Расчеты
    res, ti = simple_iter()


    # Построение графиков
    lenres = len(res)
    last = int(len(res[0]) / 7) # оставим только седьмую часть графикаы
    res_cutted = [i[0:last:] for i in res] # обрезаем неинтересную часть графика

    # Трехмерный
    x, y = np.mgrid[0:lenres:1, 0:last:1]
    z = np.array([np.array(i) for i in res_cutted])

    fig_3d = plt.figure()
    xyz = fig_3d.add_subplot(111, projection='3d')
    xyz.plot_surface(x, y, z, cmap='inferno')
    fig_3d.show()


    # Проекции
    fig, (first_graph, second_graph) = plt.subplots(
        nrows=1, ncols=2,
        figsize=(8, 4))
    
    # Первая cm - K
    x = list(np.arange(0, l, h))
    x_cutted = x[:last:]
    step = 3
    for i in res_cutted[::step]:
        first_graph.plot(x_cutted, i)
    first_graph.plot(x_cutted, res_cutted[-1])
    first_graph.set_xlabel("x, cm")
    first_graph.set_ylabel("T, K")
    first_graph.grid()

    # Вторая sec - K
    te = list(range(0, ti, t))
    for i in np.arange(0, l/3, 0.2):
        line = [j[int(i/h)] for j in res]
        second_graph.plot(te, line[:-1])
    second_graph.set_xlabel("t, sec")
    second_graph.set_ylabel("T, K")
    second_graph.grid()
    fig.show()


