"""
Булочник и Пуанкаре
"""

import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np


def main():
    n = 800            # наблюдения
    n_bread = 200      # кол-во произведеных булочек в день
    weight = 1.        # вес булочки
    underweight = .05  # недовес
    sigma = .05
    bbs = 15           # кол-во столбцов гистограммы
    bbs = 1 + int(np.log2(n))  # кол-во интегралов по ф. Стерджеса

    # Честный булочник
    br1 = st.norm.rvs(loc=weight, scale=sigma, size=n)

    # Нечестный булочник
    br2 = st.norm.rvs(loc=(weight-underweight), scale=sigma, size=n)

    plt.title('Честный булочник')
    plt.xlabel('Вес, кг')
    plt.ylabel('Относ. частота')
    plt.hist(br1, bbs, density=True)

    x = np.linspace(.8, 1.2, 100)
    plt.plot(x, st.norm.pdf(x, 1, sigma), color='g')

    plt.show()

    plt.title('Нечестный булочник')
    plt.xlabel('Вес, кг')
    plt.ylabel('Относ. частота')
    plt.hist(br2, bbs, density=True)

    plt.plot(x, st.norm.pdf(x, 1, sigma), color='g')

    plt.show()

    print(f'Средний вес честного: {np.mean(br1)}, асимметрия:{st.skew(br1)}')
    print(f'Средний вес нечестного: {np.mean(br2)}, асимметрия:{st.skew(br2)}')


if __name__ == '__main__':
    np.random.seed()
    main()
