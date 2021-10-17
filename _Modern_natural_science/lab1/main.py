import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.misc import derivative


def fp():
    def rhs(t, X: list or tuple) -> list:
        x, y = X
        return [y, -x ** 4 + 5 * x ** 2 - 4]
    return rhs


def eq_quiver(rhs, limits: list or tuple, n=16) -> tuple:
    """
    Получаем векторы для каждой точки ФП
    :param rhs: сама функция
    :param limits: границы ФП
    :param n: на сколько частей разбиваем ФП
    :return:
    """

    xlim, ylim = limits
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    U = np.zeros((n, n))
    V = np.zeros((n, n))
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            U[i][j], V[i][j] = rhs(.0, [x, y])
    return xs, ys, U, V


def plotVectors(rhs, limits: list or tuple) -> None:
    """
    Рисуем векторное поле
    :param rhs: сама функция
    :param limits: границы ФП
    :return:
    """

    plt.close()
    xlim, ylim = limits
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    xs, ys, U, V = eq_quiver(rhs, limits)
    plt.quiver(xs, ys, U, V, alpha=0.5)


def plot(rhs, times: list or tuple, point: list or tuple, style: str) -> None:
    """
    Рисуем траектории и СР
    :param rhs: сама функция
    :param times: время
    :param point: координаты точки вида [x, y]
    :param style: b- - линия синего цвета, bo - точка синего цв,
                  b+ - крест красного цв, bx - перевер. крест красного цв
    :return:
    """

    # Рисуем два раза, чтобы получить всю траекторию
    tmp = list(times)
    for i in range(2):
        sol = solve_ivp(rhs, tmp, point, method='RK45', rtol=1e-12)
        xs, ys = sol.y
        plt.plot(xs, ys, style)
        tmp[1] = -tmp[1]


def plotNodes(rhs, times: list or tuple, nodes: list or tuple):
    """
    Рисуем СР
    :param rhs: сама функция
    :param times: время
    :param nodes: вида [{'x': координата по x, 'y': координата по y, 'stable': True or False}, {}, ...]
                                                                      stable: True - уст, False - не уст
    :return:
    """

    for node in nodes:
        if node['stable']:
            style = 'bo'
        else:
            style = 'rx'
            vectors = saddleSeparatrices((node['x'], node['y']))
            plot(rhs, times, (node['x'] + vectors[0][0] / 100000, node['y'] + vectors[0][1] / 100000), 'y-')
            plot(rhs, times, (node['x'] + vectors[1][0] / 100000, node['y'] + vectors[1][1] / 100000), 'y-')
        plot(rhs, times, (node['x'], node['y']), style)


def saddleSeparatrices(nodes: list or tuple) -> np.array:
    matrix = jacobiMatrix(nodes)
    vectors = np.linalg.eigh(matrix)[1]  # Отсекаем собственные числа, выбираем только собственные вектора
    return vectors


def jacobiMatrix(X: list or tuple) -> np.array:
    x, y = X
    return np.array([[0, 1], [-4 * x ** 3 + 10 * x, 0]])


if __name__ == '__main__':
    rhs = fp()
    lim = ((-2.5, 2.5), (-3., 3.))
    limP = (0., 40.)
    states = [{'x': -2., 'y': 0, 'stable': False}, {'x': -1., 'y': 0, 'stable': True},
              {'x': 1., 'y': 0, 'stable': False}, {'x': 2., 'y': 0, 'stable': True}]

    # Рисуем векторное поле
    plotVectors(rhs, lim)
    # Рисуем состояния равновесия (если седло, то ещё и сепаратрисы)
    plotNodes(rhs, limP, states)
    # Рисуем Бесконечные траектории
    plot(rhs, limP, (0., 0.), 'r-')
    plot(rhs, limP, (0.5, 0.), 'r-')
    plot(rhs, limP, (-2.3, 0.), 'r-')
    plot(rhs, limP, (2.5, 0.), 'r-')
    # Рисуем замкнутые траектории
    plot(rhs, limP, (-0.75, 0.), 'g-')
    plot(rhs, limP, (-0.5, 0.), 'g-')
    plot(rhs, limP, (1.3, 0.), 'g-')
    plot(rhs, limP, (1.75, 0.), 'g-')

    plt.show()
