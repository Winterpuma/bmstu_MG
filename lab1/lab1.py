from math import ceil, sqrt

def func(x, u):
    return x ** 2  + u ** 2

def euler(n, h, x, y):
    y_out = []
    for i in range(n):
        y += h * func(x, y)
        x += h
        #print(x)
        y_out.append(y)
    return y_out

def implicit_euler(n, h, x, y):
    y_out = [y]
    for i in range(n):
        D = 1 - 4*h*(y + h*((x + h)**2))
        if D < 0:
            y_out.append('D<0')
            continue
        y = (1 - sqrt(D)) / (2*h)
        x += h
        #print(x)
        y_out.append(y)
    return y_out


def picar(n, h, x):
    def f1(a):
        return a ** 3 / 3
    def f2(a):
        return f1(a) + a ** 7 / 63
    def f3(a):
        return f2(a) +  (a ** 11) * (2 / 2079) + (a ** 15) / 59535
    def f4(a, f3):
        return f3 + (a ** 15)*(2 / 93555) + (a ** 19)*(2 / 3393495) + (a ** 19)*(2 / 2488563) + \
    (a ** 23)*(2 / 86266215) + (a ** 23)*(1 / 99411543) + (a ** 27)*(2 / 3341878155) + (a ** 31)*(1 / 109876902975)

    y_out = [[0, 0]]
    for i in range(n-1):
        x += h
        #print(x)
        y_f3 = f3(x)
        y_out.append([y_f3, f4(x, y_f3)])
    return y_out
        

def work():
    h = 10 ** -2
    x = 0
    y0 = 0
    end = 2

    n = ceil(abs(end - x)/h) # количество повторений

    x_arr = [x + h*i for i in range(n)]
    y1 = euler(n, h, x, y0)
    y2 = implicit_euler(n, h, x, y0)
    y3 = picar(n, h, x)

    print("|    x   |    Пикара 3   |     Пикара 4   |     Явный    |    Неявный     |")
    for i in range(0, len(y1)):
        print("|{:.5f} |  {:.8f}   |   {:.8f}   |  {:.8f}  |   {:.8f}   |".format(x_arr[i],y3[i][0],y3[i][1],y1[i],y2[i]))


work()
