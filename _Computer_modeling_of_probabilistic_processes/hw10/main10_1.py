import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np


def main():
    n = 10000  # кол-во экспериментов

    """ ------------------------------------------------Для кубиков------------------------------------------------ """
    # параметры бин. распределения
    p = 1 / 6   # вероятность выпадения шестерки
    n_dice = 4  # кол-во бросков

    # распределение через scipy
    x = np.arange(n_dice + 1)
    y = st.binom.pmf(x, n_dice, p)
    mean, var, skew, kurt = st.binom.stats(n_dice, p, moments='mvsk')
    print(f'n={n}, p={p}\n'
          f'np={y}\n'
          f'Мат. ожидание={mean}, Дисперсия={var}')

    plt.title(f'Биномиальное распределение, p={p}')
    plt.vlines(x, 0, y, color='b', lw=5)

    # моделирование СВ
    m = []
    r = np.random.uniform(0, 1, [n, n_dice])  # Массив из n строк(испытаний) и n_dice столбцов(броски)
    tmp = np.sum(r < p, axis=1)
    for i in x:
        m.append(np.sum(tmp == i) / n)
    plt.plot(x, y, 'ro', label='Scipy')
    plt.plot(x, m, 'gx', markersize=8, label='Отн.ч')

    plt.show()


if __name__ == '__main__':
    np.random.seed(100)
    main()
