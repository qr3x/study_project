import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

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
    nu = np.array([np.random.uniform(a, b) + np.random.uniform(a, b) for i in x])  # генерация случайных чисел в (a, b)

    plt.plot(nu, x, 'o')
    plt.show()

    nusorted = sorted(nu)
    nf = np.array([i / n for i in x])
    plt.plot(nusorted, nf)
    plt.show()

    kl = 1 + int(np.log2(n))  # кол-во интегралов по ф. Стерджеса
    print(f'Количество интервалов: {kl}')

    plt.title('Гистограмма относительных частот')
    plt.xlabel('')
    plt.ylabel('Относительная частота')

    plt.hist(nu, kl, density=True)

    plt.show()


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

    a = 0
    b = 2
    measure_the_time(main, (a, b))
