from math import exp

# Вводимые данные
l = 10
T0 = 300
Fmax = 50
tmax = 10
t_last = 300
period = 3
t = 1
x_step, t_step = 0.1, 1
eps = 1e-2


a1 = 0.0134
b1 = 1
c1 = 4.35e-4
m1 = 1
a2 = 2.049
b2 = 0.563e-3
c2 = 0.528e5
m2 = 1

alpha_0 = 0.05
alpha_N = 0.01

R = 0.5

k_0 = 0.4
k_N = 0.1
b_arg = (k_N * l) / (k_N - 0.4)
a_arg = k_0 * (-b_arg)
d_arg = (alpha_N * l) / (alpha_N - alpha_0)
c_arg = alpha_0 * (-d_arg)

t_values = []


def update_t_values(h_t):
    for i in range(len(t_values)):
        t_values[i] += h_t


# Исходные данные модели
def k(T):
    return a1 * (b1 + c1 * T ** m1)


def k_x(x):
    return a_arg / (x - b_arg)


def get_c(T):
    return a2 + b2 * T ** m2 - (c2 / T ** 2)


def alpha(x):
    return c_arg / (x - d_arg)


def p(x):
    return (2 / R) * alpha(x)


def f(x):
    return (2 * T0 / R) * alpha(x)


# Поток тепла
def F0(t):
    return Fmax / tmax * t * exp(1 - (t / tmax))


def get_total_F(t):
    total_F = F0(t)
    for cur_t in t_values:
        total_F += F0(cur_t)
    return total_F


# Простая аппроксимация
def approc_plus_half(func, n, step):
    return (func(n) + func(n + step)) / 2


def approc_minus_half(func, n, step):
    return (func(n) + func(n - step)) / 2


# Краевые условия
# При х = 0
def left_boundary_condition(T_prev, t):
    c_0 = get_c(T_prev[0])
    c_half = (c_0 + get_c(T_prev[1])) / 2

    p_0 = p(0)
    p_half = approc_plus_half(p, 0, x_step)
    X_half = approc_plus_half(k_x, 0, x_step)

    Ft = get_total_F(t)

    K0 = x_step * (c_half / 8 + c_0 / 4 + t_step / 8 * p_half +
                   (t_step / 4 * p_0)) + X_half * t_step / x_step

    M0 = x_step / 8 * c_half - t_step / x_step * X_half + \
         x_step / 8 * t_step * p_half

    P0 = x_step * (c_half * (T_prev[0] + T_prev[1]) / 8 +
                   c_0 * T_prev[0] / 4 + t_step *
                   (approc_plus_half(f, 0, x_step) + f(0)) / 4) + \
         Ft * t_step

    return K0, M0, P0


# При х = N
def right_boundary_condition(T_prev):
    T_prev_N = T_prev[-1]
    c_minus = approc_minus_half(get_c, T_prev_N, t)
    k_minus = approc_minus_half(k, T_prev_N, t)
    cN = get_c(T_prev_N)

    KN = x_step / 8 * c_minus + x_step / 4 * cN + t / x_step * k_minus + t * alpha_N + \
         t * x_step / 8 * p(l - x_step / 2) + t * x_step / 4 * p(l)

    MN = x_step / 8 * c_minus - t / x_step * k_minus + t * x_step / 8 * p(l - x_step / 2)

    PN = x_step / 8 * c_minus * (T_prev_N + T_prev[-2]) + \
         x_step / 4 * cN * T_prev_N + t * alpha_N * T0 + t * x_step / 4 * (f(l) + f(l - x_step / 2))

    return KN, MN, PN


def get_coeffs(T_prev):
    A, B, C, F = [], [], [], []

    for i in range(1, len(T_prev) - 1):
        cur_x = i * x_step

        a = approc_plus_half(k_x, cur_x, x_step) * t_step / x_step
        c = approc_minus_half(k_x, cur_x, x_step) * t_step / x_step

        A.append(a)
        C.append(c)
        B.append(a + c + get_c(T_prev[i]) * x_step + p(cur_x) * x_step * t_step)
        F.append(f(cur_x) * x_step * t_step + get_c(T_prev[i]) * T_prev[i] * x_step)

    return A, B, C, F

