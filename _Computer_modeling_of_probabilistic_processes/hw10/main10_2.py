import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np


def main():
    N = 10000

    liam = 1
    p = 0.01
    n = int(liam / p)

    k = 9

    # моделирование СВ
    m = []
    for i in np.arange(N):
        r = np.random.uniform(0, 1, n)
        m.append(np.sum(r < p))
    m, bin, = np.histogram(m, k + 1)

    x = np.arange(k + 1)
    m = m / N
    plt.plot(x, m)
    print(f'n={n}, p={p}\n'
          f'm={m}, sum(m)={np.sum(m)}')

    y = st.poisson.pmf(x, liam)
    plt.plot(x, y, 'ro')
    plt.vlines(x, 0, y, color='b', lw=8)
    plt.title(f'Пуассон. Лямбда={liam}')
    plt.show()


if __name__ == '__main__':
    np.random.seed(100)
    main()
