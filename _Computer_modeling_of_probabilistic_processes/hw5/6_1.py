import numpy as np
import matplotlib.pyplot as plt
from math import fabs

import os
import time


# Чистим экран (консоль) для разных ОС
def _cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Подсчет времени работы функции
def measure_the_time(function) -> tuple:
    start = time.time()

    p, err = function()

    second = int((time.time() - start))

    minute = second // 60
    second = second - minute * 60

    hour = minute // 60
    minute = minute - hour * 60

    print(f'Программа отработала за {hour} ч. {minute} мин. {second} сек.')

    return p, err


def main() -> tuple:
    n = 100     # число экспериментов
    n_dice = 3  # кол-во игральных костей
    n_six = 2   # число выпадения шестерки

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

    while True:
        try:
            n_dice = int(input('Введите количество игральных костей: '))
            if n_dice <= 0:
                _cls()
                print('Вы ввели число меньше или равное 0, нужно положительное число. Попробуйте снова')

                continue
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')

    while True:
        try:
            n_six = int(input('Количество выпадения шестерок (хотя бы): '))
            if n_six < 0:
                _cls()
                print('Вы ввели число меньше 0, нужно положительное число или 0. Попробуйте снова')

                continue
            if n_six > n_dice:
                _cls()
                print('Вы ввели количество выпадения больше количества самих костей. Попробуйте снова')

                continue
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')

    # двумерный массив из результатов экспериментов
    results = np.random.randint(1, 7, size=(n, n_dice))
    print(f'\nРезультаты экспериментов:\n{results}')

    # если выпало 6 - пишем True, не 6 - False
    results_bool = results == 6
    print(f'\nЕсли выпало 6 - True, не 6 - False:\n{results_bool}')

    # кол-во шестерок в одном эксперементе (проходимся по всем эксперементам)
    count_6 = np.sum(results_bool, axis=1)
    print(f'\nКоличество шестерок в эксперентах:\n{count_6}')

    # получаем массив подходящих экспериментов
    n_succ = count_6 >= n_six
    print(f'Массив подходящих экспериментов: {n_succ}')

    # благоприятствующие исходы
    m_arr = []
    tmp = 0
    for elem in n_succ:
        if elem:
            tmp += 1
        m_arr.append(tmp)
    del tmp
    m = np.sum(n_succ)
    print(f'\nБлагоприятствующие исходы: {m}\n'
          f'Всего экспериментов: {n}')

    # вероятность
    p_arr = []
    for i, elem in enumerate(m_arr):
        p_arr.append(round(elem / (i + 1), 3))
    p = m / n
    th = round(3 * (1/6) ** 2 * 5/6 + (1/6) ** 3, 3)
    print(f'\n'
          f'Вероятность, посчитанная с помощью программы: {round(p, 3)}\n'
          f'Теорит. вероятность: {th}')

    err_arr = []
    for i, elem in enumerate(p_arr):
        err_arr.append(fabs(round(elem, 3) - th))

    """ Теор решение задачи 
    3 кости => всего исходов 6^3, не благоприятствующих 5^4 (когда на всех выпадает что угодно, но не 6)
    => P = (6^4 - 5^4) / 6^4 или 1 - 5^4 / 6^4
    => P = 3 * (1/6)^2 * 5/6 + (1/6)^3
    """

    return p_arr, err_arr


if __name__ == '__main__':
    np.random.seed(20)
    P, error = measure_the_time(main)

    plt.title('Зависимость вероятности от количества экспериментов')
    plt.xlabel('Количество экспериментов')
    plt.ylabel('Вероятность')

    plt.plot([i for i in range(1, len(P) + 1)], P)
    plt.plot([i for i in range(1, len(P) + 1)], error)
    plt.show()
