"""
Homework №1: написать программу для вычисления чисел Фибоначчи с использованием рекуррентной ф-ии
"""

import matplotlib.pyplot as plt
import time
import os


"""
Task №2_1
"""

# Чистим экран (консоль) для разных ОС
def _cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# Подсчет времени работы функции
def measure_the_time(function, number: int):
    start = time.time()

    count_time, name = function(number)

    second = int((time.time() - start))

    minute = second // 60
    second = second - minute * 60

    hour = minute // 60
    minute = minute - hour * 60

    print(f'Программа для {name} отработала за {hour} ч. {minute} мин. {second} сек.')

    return count_time


# Рекурсивное нахождение чисел Фибоначчи
def fib_r(numbers: int):
    name = 'рекурсивной функции'

    def fibonacci(number: int) -> int:
        if number == 0:
            return 0
        elif number == 1:
            return 1
        else:
            return fibonacci(number - 2) + fibonacci(number - 1)

    fib = [0, 1]

    count_time = [0.0, 0.0]
    if numbers == 1:
        fib.pop()
    else:
        for i in range(2, numbers):
            start = time.time()
            fib.append(fibonacci(i))
            count_time.append(time.time() - start)

    print(f'{numbers} чисел Фибоначчи для {name}: {fib}')

    return count_time, name


# Итерационное нахождение чисел Фибоначчи
def fib_i(numbers):
    name = 'итерационной функции'

    fib = [0, 1]
    count_time = [0.0, 0.0]
    for i in range(2, numbers):
        start = time.time()
        fib.append(fib[-2] + fib[-1])
        count_time.append(time.time() - start)
    print(f'{numbers} чисел Фибоначчи для {name}: {fib}')

    return count_time, name


if __name__ == '__main__':
    # Отлавливаем ошибку
    while True:
        try:
            numbers_f = int(input('Сколько чисел Фибоначчи нужно (min = 1): '))

            if numbers_f < 1:
                _cls()
                print('вы ввели число меньше 1. Попробуйте снова')
            else:
                break
        except ValueError:
            _cls()
            print('вы ввели не число. Попробуйте снова')

    fib_rec = measure_the_time(fib_r, numbers_f)
    fib_it = measure_the_time(fib_i, numbers_f)

    plt.title('Время затраченное на нахождения чисел Фибоначчи')
    plt.xlabel('Кол-во чисел')
    plt.ylabel('Время')
    tmp = [i + 1 for i in range(numbers_f)]
    plt.plot(tmp, fib_rec)
    plt.plot(tmp, fib_it)
    del tmp
    plt.show()
