import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

import time
import os


# Чистим экран (консоль) для разных ОС
def _cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Подсчет времени работы функции
def measure_the_time(function, inter: tuple):
    start = time.time()

    function(inter)

    second = int((time.time() - start))

    minute = second // 60
    second = second - minute * 60

    hour = minute // 60
    minute = minute - hour * 60

    print(f'Программа отработала за {hour} ч. {minute} мин. {second} сек.')


def main(interval: tuple):
    a, b = interval
    n = 1000
    # Ввод с отловом ошибок
    while True:
        try:
            n = int(input('Введите количество экспериментов: '))
            if n <= 0:
                _cls()
                print('Вы ввели число меньше или равное 0, нужно положительное число. Попробуйте снова')

                continue
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')

    x = range(n)
    nu = np.array([np.random.uniform(a, b) - np.random.uniform(a, b) for i in x])  # генерация случайных чисел в (a, b)

    plt.title('Распределение')
    plt.plot(nu, x, 'o')
    plt.show()

    nusorted = sorted(nu)
    nf = np.array([i / n for i in x])
    plt.title('')
    plt.plot(nusorted, nf)
    plt.show()

    kl = 1 + int(np.log2(n))  # кол-во интегралов по ф. Стерджеса
    print(f'Количество интервалов: {kl}')

    plt.title('Гистограмма относительных частот')
    plt.xlabel('')
    plt.ylabel('Относительная частота')

    plt.hist(nu, kl, density=True)

    plt.show()

    print(f'Мат. ожидание: {np.mean(nu)}\n'
          f'Дисперсия: {np.var(nu)}')

    print("""Теория:
        f(z) = интеграл(fe(x)fn(x-z)dx) от -inf до +inf

        fe(x) = {0   , при x<0 или x>2
                {1/2 , при 0<=x<=2

        fn(y) = {0   , при y<0 или y>2
                {1/2 , при 0<=y<=2

        {0<=x<=2      =>    {0<=x<=2
        {0<=x-z<=2          {z<=x<=2+z

        1) -2<=z<=0          
        f(z) = 1/4*интеграл(dx) от 0 до 2+z = 1/4(z+2)

        2) 0<=z<=2
        f(z) = 1/4*интеграл(dx) от z до 2 = 1/4(2-z)
        """)

    print('Плотность распределения:\n'
          '       {0        , при z<-2 или z > 2\n'
          'f(z) = {1/4(z+2) , при -2<=z<=0\n'
          '       {1/4(z-2) , при 0<=z<=2')

    print('M = интеграл(z*f(z)) от -inf до +inf = интеграл(1/4(z+2)dz) от -2 до 0 + интеграл(1/4(z-2)dz) от 0 до 2 = '
          '1/2 - 1/2 = 0\n'
          'D = 1/3 + 1/3 - 0^2 = 2/3')

    """ -----------------------------------------------Метод Неймана----------------------------------------------- """
    print(""" --------------------------------------------Метод Неймана-------------------------------------------- """)

    a = -2
    b = 2

    def f1(arr_x):
        return 1/4 * (arr_x + 2)

    def f2(arr_x):
        return 1/4 * (2 - arr_x)

    x1 = np.linspace(a, b, n)
    x2 = np.linspace(a, b, n)

    w = max(max(f1(x1)), max(f2(x2)))
    ksi = np.random.uniform(0, 1, n)
    nu = np.random.uniform(0, 1, n)
    mu = w * nu
    arr = (b - a) * ksi + a

    k = []
    colors = np.array(['b'] * n)
    for i in range(n):
        if arr[i] < 0 and mu[i] <= f1(arr[i]) or arr[i] > 0 and mu[i] <= f2(arr[i]):
            k.append(arr[i])
            colors[i] = 'g'

    plt.title('Распределение')
    plt.scatter(arr, mu, color=colors, s=.5, marker='x')
    plt.show()

    # Гстограмма относ. частот
    kl = 1 + int(np.log2(n))
    ys, bin, p = plt.hist(k, kl, density=True)
    mbin = (bin[1] - bin[0]) / 2  # середина интервалов
    xs = bin + mbin

    plt.title('Гстограмма относ.ч.')
    plt.plot(xs[:-1], ys, 'r--')
    plt.show()

    # Оценка ф-ии распределения
    ys, bin, p = plt.hist(k, kl, density=True, cumulative=True)
    mbin = (bin[1] - bin[0]) / 2  # середина интервалов
    xs = bin + mbin

    plt.title('Оценка ф-ии распределения')
    plt.plot(xs[:-1], ys, 'r--')
    plt.show()

    print(f'Мат. ожидание: {np.mean(k)}\n'
          f'Дисперсия: {np.var(k)}\n'
          f'Среднекв. отклонение: {np.std(k)}')


if __name__ == '__main__':
    np.random.seed(100)
    # Ввод с отловом ошибок
    while True:
        try:
            a = int(input('Введите левую границу интервала: '))
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')
    while True:
        try:
            b = int(input('Введите правую границу интервала: '))
            if b <= a:
                _cls()
                print('b <= a. Попробуйте снова')
                continue
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')

    measure_the_time(main, (a, b))
