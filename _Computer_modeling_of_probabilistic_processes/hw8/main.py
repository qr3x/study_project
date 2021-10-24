import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


def f(x):
    return np.sin(x) ** 2


def main():
    # Теор. значение интеграла
    theory = 1.570796326794897  # pi/2
    a = 0
    b = np.pi
    nt = 7  # кол-во точек

    n = 1000
    x = np.linspace(a, b, n)
    y = f(x)
    plt.plot(x, y)
    fmax = max(y)
    fmin = min(y)
    x = np.random.uniform(a, b, n)
    y = np.random.uniform(fmin, fmax, n)

    color = ['m'] * n
    for i in range(n):
        if y[i] < f(x[i]):
            color[i] = 'green'

    plt.scatter(x, y, c=color, s=5, marker='X')
    plt.xlabel('x')
    plt.title('(sin(x))^2')
    plt.show()

    table = PrettyTable()
    table.field_names = ['n', 'инт', 'error1', 'error2']
    for i in range(1, nt):
        n = 10 ** i

        """ Интегрирование методом Монте-Карло (случайное значение величины) """
        x = np.random.uniform(a, b, n)
        m1 = sum(f(x))
        int1 = (b - a) / n * m1
        err1 = abs(theory - int1)

        """ Считаем кол-во точек под кривой """
        y = np.random.uniform(fmin, fmax, n)
        m = sum(y < f(x))
        int2 = m / n * (fmax - fmin) * (b - a)
        err2 = abs(theory - int2)

        table.add_row([n, theory, err1, err2])
        plt.plot(np.log10(n), err1, 'bo')
        plt.plot(np.log10(n), err2, 'rx')
    print(table)
    plt.xlabel('ln(n)')
    plt.ylabel('error1 - o, error2 - x')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    np.random.seed(20)
    main()
