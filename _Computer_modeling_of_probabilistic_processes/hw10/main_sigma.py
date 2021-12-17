import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

from prettytable import PrettyTable


def main():
    """ --------------------------------------------------Таблица-------------------------------------------------- """
    table = PrettyTable()
    table.field_names = ['sigma', 'число дефектов на миллион возможностей']

    for i in range(1, 7):
        sigma = 7 - i
        y = 1 - st.norm.cdf(sigma, 1.5, 1)
        table.add_row([sigma, round(y * 10 ** 6, 2)])
    print(table)

    """ --------------------------------------------------Графики-------------------------------------------------- """
    x = np.linspace(-7, 7, 100)
    plt.plot(x, st.norm.pdf(x, 0, 1))           # график стандартн. норм. распред.
    plt.plot(x, st.norm.pdf(x, 1.5, 1), 'r--')  # график норм. распред. смещенное на 1.5

    # вертикальные линии при сигма > 2
    xx = np.linspace(2, 7, 30)
    plt.vlines(xx, 0, st.norm.pdf(xx, 1.5, 1), 'r')
    plt.show()

    # для функции распределения
    plt.plot(x, st.norm.cdf(x, 1.5, 1))
    plt.vlines(2, 0, 1, 'r')
    plt.show()


if __name__ == '__main__':
    main()
