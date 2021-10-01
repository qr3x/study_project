import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st


np.random.seed(20)

elements = ((0, 12), (3, 7))
for elem in elements:
    n = 100      # число точек
    a = elem[0]  # начало интервала
    b = elem[1]  # конец интервала
    x = range(n)

    z = [np.random.uniform(a, b) for i in x]  # генерация случайных чисел в [a, b)
    plt.plot(z, x, 'o')  # рисуем график
    plt.show()

    kl = 1 + int(np.log2(n))  # кол-во интегралов по ф. Стерджеса
    print(f'Количество интервалов: {kl}')

    # гистограмма относительных частот
    plt.hist(z, kl)
    plt.show()
    plt.hist(z, kl, density=True)  # гистограмма относительных частот

    # плотность распределения
    fit = st.uniform.pdf(z, a, b - a) # распределение scipy
    plt.plot(z, fit, color='pink')
    plt.show()

    f = st.uniform.cdf(z, a, b - a)
    plt.plot(z, f, color='red')

    # оценка
    z1 = sorted(z)
    nf = [i / n for i in x]
    plt.plot(z1, nf)
    plt.show()

