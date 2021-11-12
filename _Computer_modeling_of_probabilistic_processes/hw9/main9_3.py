"""
Сравнения выпадения:
1. Хотя бы одной шестерки при 4 бросках одной игр. кости
2. Хотя бы раз две шестерки при 24 бросках двух игр. костей
"""

import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np


def main(n: int, n_dice: int) -> None:
    """
    :param n: количество бросков
    :param n_dice: количество игр. костей
    :return:
    """

    p = 1 / 6 ** n_dice  # вероятность выпадения n_dice шестерок(ки)

    x = np.arange(n + 1)
    y = st.binom.pmf(x, n, p)

    plt.title('Биномиальное распр')
    plt.vlines(x, 0, y, colors='b', lw=8)
    plt.plot(x, y, 'r o')
    plt.show()

    return sum(y[1:])


if __name__ == '__main__':
    arr = [{'n_experiment': 4, 'n_dice': 1}, {'n_experiment': 24, 'n_dice': 2}]
    sums = []
    for elem in arr:
        plt.close()
        sums.append(main(elem['n_experiment'], elem['n_dice']))

    print(f'Вероятность выпадения:\n'
          f'1. Хотя бы одной шестерки при 4 бросках одной игр. кости = {sums[0]}\n'
          f'2. Хотя бы раз две шестерки при 24 бросках двух игр. костей = {sums[1]}')

    if sums[0] > sums[1]:
        print('Вероятность события 1 больше вероятности события 2')
    else:
        print('Вероятность события 2 больше вероятности события 1')
