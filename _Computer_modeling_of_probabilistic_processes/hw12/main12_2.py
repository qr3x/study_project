import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

from prettytable import PrettyTable


def main():
    table = PrettyTable()
    table.field_names = ['Кол-во СВ', 'Выборочное среднее', 'Дисперсия', 'Ассиметрия', 'Эксцесс']

    n = 10000                   # кол-во наблюдений
    bins = 1 + int(np.log2(n))  # кол-во интегралов по ф. Стерджеса
    a = 0                       # начало интервала
    b = 1                       # конец интервала
    n_ksi = 6                   # количество случайных величин -1 (Если должно быть 6, то ставим 7)

    ksi = [np.array([0] * n)] * bins  # массив с будущими норм. распределениями
    res = [np.array([0] * n)] * bins  # результирующий массив
    x = [np.array([0.] * bins)] * n   # массив для оси абсцисс
    y = [np.array([0.] * bins)] * n   # массив для оси ординат

    for i in range(n_ksi):
        ksi[i] = np.random.uniform(a, b, n)  # равномерное распределение numpy
        res[i] = ksi[i] + res[i - 1]
        res_h, bins_h, p = plt.hist(res[i], bins, density=True, color='gray', width=.2)

        y[i] = res_h
        mx = max(bins_h)
        mn = min(bins_h)

        x[i] = np.linspace(mn, mx, bins, endpoint=False) + (mx - mn) / bins / 2  # сместим многоугольник
        plt.title(f'{i + 1} случайных величин')
        plt.xlabel('Количество СВ')
        plt.ylabel('Относ. частота')
        plt.plot(x[i], y[i], color='red')
        plt.show()

        table.add_row([i + 1, np.mean(y[i]), np.var(y[i]), st.skew(y[i]), st.kurtosis(y[i])])
    print(table)


if __name__ == '__main__':
    np.random.seed(10)
    main()
