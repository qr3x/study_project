import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

from prettytable import PrettyTable


def main():
    k = 6    # попаданий

    m = np.arange(k + 1)
    Nk = np.array([5, 19, 26, 26, 21, 13, 8])  # Феллер
    n = sum(Nk)                                # Число квадратов
    sn = sum(m * Nk)                           # Число бактерий

    liambda = sn / n
    plt.plot(m, Nk, color='r')

    plt.title(f'Пуассон, λ = {liambda}')
    y = st.poisson.pmf(m, liambda) * n
    plt.plot(m, y, 'ro')
    plt.vlines(m, 0, y, colors='b', lw=8)
    plt.show()

    Nk = list(Nk)
    Nk.insert(0, 'Nk')
    table = PrettyTable()
    table.field_names = ['k', 0, 1, 2, 3, 4, 5, 6]
    table.add_row(Nk)
    y = list(y)
    for i, elem in enumerate(y):
        y[i] = round(elem, 2)
    print(y)
    y.insert(0, 'p(k, λ)')
    table.add_row(y)

    print(table)


if __name__ == '__main__':
    main()
