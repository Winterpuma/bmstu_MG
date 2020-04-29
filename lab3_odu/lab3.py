# Лабораторная по моделированию №3
# Реализация модели на основу ОДУ второго
# порядка с краевыми условиями II и III рода.

import matplotlib.pyplot as plt
import numpy as np

# Исходные данные модели
def get_constants():
    b = (kN * N) / (kN - k0)
    d = (aN * N) / (aN - a0)
    a = -k0 * b
    c = -a0 * d
    return a, b, c, d

def k(x):
    return a / (x - b)

def alpha(x):
    return c / (x - d)

def p(x):
    return (2 * alpha(x)) / R

def f(x):
    return (2 * T0 * alpha(x)) / R


# Разностная схема
def A(n):
    return approc_plus_half(k, n) / h

def C(n):
    return approc_minus_half(k, n) / h

def B(n):
    return A(n) + C(n) + p(n) * h

def D(n):
    return f(n) * h


# Простая аппроксимация
def approc_plus_half(func, n):
    return (func(n) + func(n + h)) / 2

def approc_minus_half(func, n):
    return (func(n - h) + func(n)) / 2


# Краевые условия
# При х = 0
def left_boundary_condition():
    k0 = approc_plus_half(k, 0) + (h*h*approc_plus_half(p, 0) / 8) + ((h*h*p(0)) / 4)
    M0 = -approc_plus_half(k, 0) + (h*h*approc_plus_half(p, 0) / 8)
    P0 = h*F0 + (h*h / 4) * (approc_plus_half(f, 0) + f(0))
    return k0, M0, P0

# При x = N
def right_boundary_condition():
    kN = (approc_minus_half(k, N) / h) - (h*approc_minus_half(p, N)/ 8)
    MN = -aN - (approc_minus_half(k, N) / h) - (h*p(N) / 4) - (h*approc_minus_half(p, N) / 8)
    PN = -(h/4) * (f(N) + approc_minus_half(f, N)) - T0*aN
    return kN, MN, PN


if __name__ == "__main__":
    # Исходные данные
    k0 = 0.4
    kN = 0.1
    a0 = 0.05
    aN = 0.01
    N = 10
    T0 = 300
    R = 0.5
    F0 = 50
    h = 1e-3
 
    a, b, c, d = get_constants()

    k0, M0, P0 = left_boundary_condition()
    kN, MN, PN = right_boundary_condition()

    # Прямой ход
    eps = [0, -M0 / k0]
    eta = [0, P0 / k0]

    x = h
    n = 1
    while x + h < N:
        eps.append(C(x) / (B(x) - A(x) * eps[n]))
        eta.append((A(x) * eta[n] + D(x)) / (B(x) - A(x) * eps[n]))
        n += 1
        x += h

    # Обратный ход
    t = [0] * (n + 1)
    
    t[n] = (PN - MN * eta[n]) / (kN + MN * eps[n])

    for i in range(n - 1, -1, -1):
        t[i] = eps[i + 1] * t[i + 1] + eta[i + 1]

    # График
    x = [i for i in np.arange(0, N, h)]

    plt.plot(x, t[:-1], 'r-')
    plt.xlabel("x, cm")
    plt.ylabel("temperature, K")
    plt.grid()
    plt.show()
