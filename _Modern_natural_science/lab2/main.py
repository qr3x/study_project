import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def fp():
    def rhs(t, X: list or tuple) -> list:
        x, y = X
        return [y, -x ** 4 + 5 * x ** 2 - 4]

    return rhs


def fp2(a: float):
    def rhs(t, X: list or tuple) -> list:
        x, y = X
        return [y, -x ** 4 + 5 * x ** 2 - 4 - a * y]

    return rhs


def eq_quiver(rhs, limits: list or tuple, n) -> tuple:
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


def plotVectors(rhs, limits: list or tuple, n=16) -> None:
    """
    Рисуем векторное поле
    :param rhs: сама функция
    :param limits: границы ФП
    :param n: на сколько частей разбиваем ФП
    :return:
    """

    plt.close()
    xlim, ylim = limits
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    xs, ys, U, V = eq_quiver(rhs, limits, n)
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


# Консервативная система
def plotNodes_conSys(rhs, nodes: list or tuple):
    """
    Рисуем СР
    :param rhs: сама функция
    :param nodes: вида [{'x': координата по x, 'y': координата по y, 'stable': True or False}, {}, ...]
                                                                      stable: True - уст, False - не уст
    :return:
    """

    times = (0., 40.)

    for node in nodes:
        if node['stable']:
            style = 'bo'
        else:
            style = 'rx'
            vectors = saddleSeparatrices((node['x'], node['y']))
            plot(rhs, times, (node['x'] + vectors[0][0] / 100000, node['y'] + vectors[0][1] / 100000), 'y-')
            plot(rhs, times, (node['x'] + vectors[1][0] / 100000, node['y'] + vectors[1][1] / 100000), 'y-')
        plot(rhs, times, (node['x'], node['y']), style)


# Не консервативная система
def plotNodes(rhs, nodes: list or tuple):
    """
    Рисуем СР
    :param rhs: сама функция
    :param nodes: вида [{'x': координата по x, 'y': координата по y, 'stable': True or False}, {}, ...]
                                                                      stable: True - уст, False - не уст
    :return:
    """

    times = (0., 40.)

    for node in nodes:
        if node['stable']:
            style = 'bo'
        else:
            style = 'rx'
            if node['type'] == 'saddle':
                vectors = saddleSeparatrices((node['x'], node['y']))
                print(f"СР: {(node['x'], node['y'])}")
                print(f"Собственные вектора:\n{vectors}")
                plot(rhs, times, (node['x'] + vectors[0][0] / 100, node['y'] + vectors[0][1] / 100), 'y-')
                plot(rhs, times, (node['x'] + vectors[1][0] / 100, node['y'] + vectors[1][1] / 100), 'y-')
                plot(rhs, times, (node['x'] - vectors[0][0] / 100, node['y'] - vectors[0][1] / 100), 'y-')
                plot(rhs, times, (node['x'] - vectors[1][0] / 100, node['y'] - vectors[1][1] / 100), 'y-')
        plot(rhs, times, (node['x'], node['y']), style)
    print('---------------------Следующий ФП---------------------')


def saddleSeparatrices(nodes: list or tuple) -> np.array:
    matrix = jacobiMatrix(nodes)
    vectors = np.linalg.eigh(matrix)[1]  # Отсекаем собственные числа, выбираем только собственные вектора
    return vectors


def jacobiMatrix(X: list or tuple, coef=0) -> np.array:
    x, y = X
    return np.array([[0, 1], [-4 * x ** 3 + 10 * x, -coef]])


def plotX(rhx, times: list or tuple, point: list or tuple, style: str, title: str):
    """
    Рисуем траектории и СР
    :param rhs: сама функция
    :param times: время
    :param point: координаты точки вида [x, y]
    :param style: b- - линия синего цвета, bo - точка синего цв,
                  b+ - крест красного цв, bx - перевер. крест красного цв
    :param title: Название графика
    :return:
    """

    plt.close()
    plt.title(title)
    plt.xlabel('t')
    plt.ylabel('x')

    sol = solve_ivp(rhs, times, point, method='RK45', rtol=1e-12)
    xs, ys = sol.y
    ts = sol.t
    plt.plot(ts, xs, style)
    plt.show()


if __name__ == '__main__':
    """ --------------------------------------------------- lab1 --------------------------------------------------- """

    rhs = fp()
    lim = ((-2.5, 2.5), (-3., 3.))
    limP = (0., 20.)
    states = [{'x': -2., 'y': 0, 'stable': False}, {'x': -1., 'y': 0, 'stable': True},
              {'x': 1., 'y': 0, 'stable': False}, {'x': 2., 'y': 0, 'stable': True}]

    # Рисуем векторное поле
    plotVectors(rhs, lim)
    # Рисуем состояния равновесия (если седло, то ещё и сепаратрисы)
    plotNodes_conSys(rhs, states)
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

    plotX(rhs, limP, (-2.0070710678, 0.0070710678), 'r-', 'x(t) для СР=(-2, 0). Левая верхн траект')
    plotX(rhs, limP, (-2.0070710678, -0.0070710678), 'r-', 'x(t) для СР=(-2, 0). Левая нижн траектория')
    plotX(rhs, limP, (2.0070710678, 0.0070710678), 'g-', 'x(t) для СР=(-2, 0). Замкнутая правая траектория')

    """ --------------------------------------------------- lab2 --------------------------------------------------- """

    lim = ((-2.5, 2.5), (-3., 3.))
    limP = (0., 10.)
    """
    Состояния равновесия
    Иерархия:
    Номер на биф.диаграмме: список СР
    сами СР описываются словарями, в которых есть координаты по x и y, устойчивость и тип СР
    """
    states = {1: [{'x': -2., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': -1., 'y': 0, 'type': 'node', 'stable': True},
                  {'x': 1., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': 2., 'y': 0, 'type': 'node', 'stable': True}],
              2: [{'x': -2., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': -1., 'y': 0, 'type': 'node', 'stable': True},
                  {'x': 1., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': 2., 'y': 0, 'type': 'focus', 'stable': True}],
              3: [{'x': -2., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': -1., 'y': 0, 'type': 'focus', 'stable': True},
                  {'x': 1., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': 2., 'y': 0, 'type': 'focus', 'stable': True}],
              4: [{'x': -2., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': -1., 'y': 0, 'type': 'focus', 'stable': False},
                  {'x': 1., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': 2., 'y': 0, 'type': 'focus', 'stable': False}],
              5: [{'x': -2., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': -1., 'y': 0, 'type': 'node', 'stable': False},
                  {'x': 1., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': 2., 'y': 0, 'type': 'focus', 'stable': False}],
              6: [{'x': -2., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': -1., 'y': 0, 'type': 'node', 'stable': False},
                  {'x': 1., 'y': 0, 'type': 'saddle', 'stable': False},
                  {'x': 2., 'y': 0, 'type': 'node', 'stable': False}]
              }
    # Коэф. альфа
    arr_a = [[8., 'отрезок (-inf, -sqrt(48))'],
             [6., 'отрезок (-sqrt(48), -sqrt(24)'],
             [3., 'отрезок (-sqrt(24), 0)'],
             [-3., 'отрезок (0, sqrt(24))'],
             [-6., 'отрезок (sqrt(24), sqrt(48))'],
             [-8., 'отрезок (sqrt(48), inf)']]
    for i, a in enumerate(arr_a):
        # Рисуем ФП
        rhs = fp2(a[0])

        # Рисуем векторное поле
        plotVectors(rhs, lim)
        # Рисуем состояния равновесия (если седло, то ещё и сепаратрисы)
        plotNodes(rhs, states[i + 1])
        # Рисуем Бесконечные траектории
        plot(rhs, limP, (-2.2, 1.), 'r-')
        plot(rhs, limP, (-2.3, -1.5), 'r-')
        # Рисуем замкнутые траектории
        plot(rhs, limP, (-1.5, 1.), 'r-')
        plot(rhs, limP, (-1.55, -1.), 'r-')
        plot(rhs, limP, (0., 0.), 'r-')
        plot(rhs, limP, (0., -2.), 'r-')
        plot(rhs, limP, (0.8, 1.), 'r-')
        plot(rhs, limP, (0.8, -0.2), 'r-')
        plot(rhs, limP, (1.5, 1.), 'r-')
        plot(rhs, limP, (1.5, -1.), 'r-')
        plot(rhs, limP, (2.3, 0.5), 'r-')
        plot(rhs, limP, (2.3, -1), 'r-')

        plt.title(f'ФП при a = {a[0]}, {a[1]}')
        plt.show()

        time = (0., 3.)
        # Рисуем график x(t)
        plt.close()
        plt.xlabel('t')
        plt.ylabel('x')
        
        plotX(rhs, time, (0, 2.), 'r-', 'x(t) для СР=(-1, 0) т.(0, 0.2)')
        plotX(rhs, time, (2, 1), 'r-', 'x(t) для СР=(2, 0) т.(2, 1)')
