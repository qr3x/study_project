"""
Задача 9_1 для суммы 6
"""

import matplotlib.pyplot as plt
import numpy as np


def main():
    n = 10000     # кол-во наблюдений n + 1
    step = 20     # столбцов диаграммы
    a = 0         # начало инт
    b = 1         # конец инт
    n_vals = 12   # СВ

    f = [0] * n_vals  # массив св
    z = [0] * n_vals  # результирующий
    x2 = [0] * step   # массив m графиков
    z2 = [0] * step   # массив m графиков

    for i in range(1, n_vals):
        f[i] = np.random.uniform(a, b, n)                                       # равномерное распределение
        z[i] = f[i] + z[i - 1]                                                  # сумма св
        y, bin, p = plt.hist(z[i], step, density=True, color='gray', width=.1)  # гистограмма
        mbin = (bin[1] - bin[0]) / 2                                            # середина интервала
        hbin = bin + mbin                                                       # сдвинули интервалы на пол интервала

        print(f'для кол-ва СВ={i}:\n'
              f'Мат. ожидание={np.mean(z[i])}\n'
              f'Дисперсия={np.var(z[i])}\n'
              f'------------------------------')

        plt.title(f'Гистограмма отн. частот. Кол-во СВ={i}')
        plt.plot(hbin[:-1], y, 'r')
        plt.show()

        x2[i] = hbin[:-1]
        z2[i] = y
    for i in range(1, n_vals):
        plt.plot(x2[i], z2[i])
    plt.show()


if __name__ == '__main__':
    np.random.seed(100)
    main()
