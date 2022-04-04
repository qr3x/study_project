""" Задача:
На автоматическую телефонную станцию поступает поток вызовов с
интенсивностью λ. С.в. η — число вызовов за t минут, имеет распределение Пуассона со средним λt
---------------------------------------------------------------------------------------------------------
Распределение Пуассона:
P(η(t)=η) = λ^η/η! * exp(-λ)
"""
from math import exp, factorial, fabs, inf
import matplotlib.pyplot as plt
import numpy as np

import os
from prettytable import PrettyTable


# Чистим экран (консоль) для разных ОС
def _cls() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def print_title(title: str) -> None:
    print('\n')
    print('=====================================================================================================' \
          '=================================================')
    print(' ' * (150 // 2 - len(title) // 2), title, sep='')
    print('=====================================================================================================' \
          '=================================================')
    print('\n')


def count_poisson(liambda: float, n: int) -> float:
    return liambda ** n / factorial(n) * exp(-liambda)


def stage1(N: int, liambda: float, print_info=False) -> tuple:
    """
    :param N: количество экспериментов
    :param liambda: интенсивность
    :param print_info: выводить информацию или нет
    :return: массив св
    """

    print_title('1 ЭТАП')

    """ --------------------------------------------------Подсчет-------------------------------------------------- """

    arr = []
    U = np.random.uniform(0, 1, N)
    for i in range(N):
        u = U[i]

        p = exp(-liambda)
        p_tmp = p
        index = 0
        while u >= p:
            index += 1
            p_tmp = p_tmp * liambda / index
            p += p_tmp
        del p_tmp

        n = index

        if print_info:
            print('-------------------------------------')
            print(f'Эксперимент №{i + 1}:')

            content = f"""
    Интенсивность: λ={liambda}
    Значение случайной величины U: u={u}
    Число вызовов за t минут: η={n}
            """
            print(content)

        arr.append(n)

    dict_for_table = {}
    for elem in arr:
        try:
            dict_for_table[elem] = [elem, dict_for_table[elem][1] + 1, (dict_for_table[elem][1] + 1) / N]
        except KeyError:
            dict_for_table[elem] = [elem, 1, 1 / N]

    """ --------------------------------------------------Таблица-------------------------------------------------- """

    yi = ['yi']
    ni = ['ni']
    ni_n = ['ni/n']
    tmp = sorted(dict_for_table)
    yi.extend(tmp)
    ni.extend([dict_for_table[elem][1] for elem in tmp])
    ni_n.extend([dict_for_table[elem][2] for elem in tmp])
    del tmp

    table = PrettyTable()
    table.title = 'Значения СВ и их частоты'
    table.field_names = yi
    table.add_rows([
        ni,
        ni_n
    ])
    print(table)

    return arr, dict_for_table


def stage2(N: int, data: list, dict_for_table: dict, liambda: float):
    """
    :param N: количество экспериментов
    :param data: массив св
    :param dict_for_table: словарь из 1 этапа
    :param liambda: интенсивность
    :return:
    """

    print_title('2 ЭТАП')

    """ --------------------------------------------------Подсчет-------------------------------------------------- """

    en = 0  # мат. ожидание
    x = 0   # выборочное среднее
    for yi in dict_for_table.keys():
        ni = dict_for_table[yi][1]
        ni_n = dict_for_table[yi][2]
        en += yi * ni_n
        x += yi * ni
    x /= N
    en_x = fabs(en - x)  # разница мат. ожидания и выборочного среднего

    dn = 0  # дисперсия
    s2 = 0  # выборочная дисперсия
    for yi in dict_for_table.keys():
        ni = dict_for_table[yi][1]
        ni_n = dict_for_table[yi][2]
        dn += (yi - en) ** 2 * ni_n
        s2 += (yi - x) ** 2 * ni
    s2 /= N
    dn_s2 = fabs(dn - s2)  # разница дисперсии и выборочной дисперсии

    # выборочная медиана
    if N in [1, 2]:
        if N == 1:
            me = data[0]
        else:
            me = data[1]
    else:
        if N % 2 == 1:
            me = data[N // 2 + 1]
        else:
            me = (data[N // 2] + data[N // 2 + 1]) / 2
    r = data[-1] - data[0]  # размах выборки

    """ --------------------------------------------------График-------------------------------------------------- """

    # Вычисляем точки выборочной функции распределения
    y_tmp = []
    x_tmp = []
    y_tmp_theory = []
    sum_p = 0
    for x_i in sorted(dict_for_table):
        sum_p += dict_for_table[x_i][2]
        y_tmp.append(round(sum_p, 5))
        x_tmp.append(x_i)
    del x_i

    # Вычисляем точки теоритической функции распределения
    sum_p_theory = 0
    for i in range(max(x_tmp) + 2):
        sum_p_theory += P[i]
        y_tmp_theory.append(sum_p_theory)
    del sum_p_theory

    # Ищем D
    y_tmp2 = []
    for i in range(len(y_tmp_theory) - 1):
        x_index = 0
        while i > x_tmp[x_index]:
            x_index += 1
            if x_index + 1 == len(x_tmp):
                break
        y_tmp2.append(y_tmp[x_index])
    y_tmp2.append(1.0)

    tmp = []
    for i in range(len(y_tmp2)):
        fn_ = y_tmp2[i]
        fn = y_tmp_theory[i]
        tmp.append(fabs(fn_ - fn))
    D = max(tmp)

    print(f'Выборка: {x_tmp}')
    print(f'Значения по оси Y для выборочной ф. распределения: {y_tmp2}')
    print(f'Значения по оси Y для теоритической ф. распределения: {y_tmp_theory}')
    print(f'Массив разности функций распределений: {tmp}')

    length = len(y_tmp2)
    for i in range(length):
        if i == 0:
            plt.plot([0, i], [0, 0], 'b-', label='График выбор Fη(x)')
            plt.plot([0, i], [0, 0], 'r-', label='График теоритической Fη(x)')
        plt.plot([i, i + 1], [y_tmp2[i], y_tmp2[i]], 'b-')
        plt.plot([i, i + 1], [y_tmp_theory[i], y_tmp_theory[i]], 'r-')
    plt.title(f'Графики Fη(x). D=max|^Fη(x) - Fη(x)| = {D} для x={tmp.index(D)}')
    plt.legend()
    plt.show()

    """ --------------------------------------------------Таблицы-------------------------------------------------- """

    table = PrettyTable()
    table.title = 'Числовые характеристики'
    table.field_names = ['Чем посчитано', 'Eη', 'x', '|Eη − x|', 'Dη', 'S^2', '|Dη − S^2|', 'Me', 'R']
    table.add_row(['Мной', en, x, en_x, dn, s2, dn_s2, me, r])
    table.add_row(['Numpy и стандартными способами*', liambda, np.mean(data), fabs(liambda - np.mean(data)), liambda, np.var(data),
                   fabs(liambda-np.var(data)), np.median(data), data[-1] - data[0]])
    print(table)
    print('*Стандартными способами - для пуассоновского распределения мат. ожидание и дисперсия равны лямбде')

    yj = ['yj']
    pj = ['P({η=yj})']
    nj_n = ['nj/n']

    tmp = sorted(dict_for_table)
    yj.extend(tmp)
    pj.extend([P[elem] for elem in tmp])
    nj_n.extend([dict_for_table[elem][2] for elem in tmp])

    table = PrettyTable()
    table.title = 'Теоритические вероятности'
    table.field_names = yj
    table.add_rows([
        pj,
        nj_n
    ])
    print(table)
    print('max|nj/n - P({η=yj})| =', max([fabs(nj_tmp - pj_tmp) for nj_tmp, pj_tmp in zip(nj_n[1:], pj[1:])]))


def stage3(print_info=False) -> None:
    """
    :param print_info: выводить информацию или нет
    :return: None
    """
    print_title('3 ЭТАП')

    # Ввод k
    while True:
        try:
            k = int(input('Введите количество интервалов: k = '))
            if k <= 0:
                _cls()
                print('k должна быть положительной. Попробуйте снова')
                continue
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')

    # Ввод границ z
    zs = [-inf]
    for i in range(k - 1):
        while True:
            try:
                z = float(input(f'Введите границу: z_{i + 1} = '))
                if z <= zs[i]:
                    _cls()
                    print(f'Граница z_{i + 1} должна быть больше предыдущей ({zs[i]}). Попробуйте снова')
                    continue
                if z == -inf or z == inf:
                    _cls()
                    print(f'Граница z_{i + 1} должна быть в интервале (-inf, inf). Попробуйте снова')
                    continue
                zs.append(z)
                break
            except ValueError:
                _cls()
                print('Вы ввели не число. Попробуйте снова')
    zs.append(inf)
    print('Границы:', zs)

    qs = []
    for j in range(1, len(zs)):
        q = 0
        for elem in sorted(P):
            if zs[j - 1] <= elem < zs[j]:
                q += P[elem]
        qs.append(q)
    if print_info:
        content = """
    Информация (Вероятности С.В. η):\n"""
        for elem in sorted(P):
            content += f'     {elem}: {P[elem]}\n'
        print(content)

    intervals = ['Интервалы']
    intervals.extend([f'[{zs[j - 1]}, {zs[j]})' for j in range(1, len(zs))])
    qk = ['qk']
    qk.extend(qs)
    table = PrettyTable()
    table.title = 'Отображение гипотезы в виде теоретических вероятностей'
    table.field_names = intervals
    table.add_row(qk)
    print(table)
    del intervals


if __name__ == '__main__':
    np.random.seed(123)

    # GLOBAL variables
    P = {}
    N = 100000
    liambda = 1

    while True:
        try:
            N = int(input('Введите количество экспериментов: N = '))
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')
    while True:
        try:
            liambda = float(input('Введите интенсивность: λ = '))
            if liambda <= 0:
                _cls()
                print('λ должна быть положительной. Попробуйте снова')
                continue
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')

    array, dict_for_table = stage1(N, liambda, False)

    array.sort()
    # Сохраняем массив вероятностей, чтобы не высчитывать их каждый раз
    # for elem in sorted(dict_for_table):
    #     P[elem] = count_poisson(liambda, elem)
    for elem in range(max(sorted(dict_for_table)) + 2):
        P[elem] = count_poisson(liambda, elem)

    stage2(N, array, dict_for_table, liambda)

    stage3(True)
