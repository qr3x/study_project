import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

import time
import os

# Чистим экран (консоль) для разных ОС
def _cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Подсчет времени работы функции
def measure_the_time(function, d=None):
    start = time.time()

    if d is None:
        tmp = function()
    else:
        tmp = function(d)

    second = int((time.time() - start))

    minute = second // 60
    second = second - minute * 60

    hour = minute // 60
    minute = minute - hour * 60

    print(f'Программа сделала {tmp["message"]} за {hour} ч. {minute} мин. {second} сек.')

    return tmp


def main() -> dict:
    n = 10
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

    # Генерируем массивы размером n с числами от 0 до 1
    x = np.random.rand(n)
    y = np.random.rand(n)

    # Считаем количество точек попавшие в нашу 1/4 круга (делаем список для таблицы и графика)
    quantity_in_a_circle = []
    number = []
    for i in range(n):
        # Разделяем все число эксперементов на отрезки по 1000 и последний отрезок <= 1000
        if i % 1000 == 0 and i != 0 or i == n - 1:
            number.append(i)
            quantity_in_a_circle.append(sum(x[:i + 1] ** 2 + y[:i + 1] ** 2 < 1))
    quantity_in_a_circle = np.array(quantity_in_a_circle)
    number = np.array(number)

    # Считаем число Пи
    pi = 4. * quantity_in_a_circle / n

    return {'pi': pi, 'i': number, 'x': x, 'y': y, 'message': 'подсчет числа π'}

def create_graph(info: dict) -> dict:
    plt.title(f'n = {info["i"][-1] + 1}, π ≈ {info["pi"][-1]}')
    plt.xlabel('x')
    plt.xlim(0., 1.)
    plt.ylabel('y')
    plt.ylim(0., 1.)

    tmp = info['x'] ** 2 + info['y'] ** 2 < 1
    for i, elem in enumerate(tmp):
        if elem:
            color = 'red'
        else:
            color = 'blue'
        plt.scatter(info['x'][i], info['y'][i], s=1, c=color)

    return {'message': 'построение графика'}

def create_table(info: dict) -> dict:
    table = PrettyTable()
    table.field_names = ['n', 'π']
    for i, pi in zip(info['i'], info['pi']):
        table.add_row([i + 1, pi])

    print(table)

    return {'message': 'построение таблицы'}


if __name__ == '__main__':
    np.random.seed(20)

    # Ввод с отловом ошибок
    while True:
        n = input('Введите:\n'
                  '1 - вывести график\n'
                  '2 - вывести таблицу\n'
                  '3 - вывести график и таблицу\n')
        if n in ['1', '2', '3']:
            break
        _cls()
        print('Вы ввели не 1, 2 или 3. Попробуйте снова')

    data = measure_the_time(main)

    if n in ['1', '3']:
        measure_the_time(create_graph, data)
        plt.show()

    if n in ['2', '3']:
        measure_the_time(create_table, data)


