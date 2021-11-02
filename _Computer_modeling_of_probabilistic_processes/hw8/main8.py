import matplotlib.pyplot as plt
import numpy as np
import time
import os


# Чистим экран (консоль) для разных ОС
def _cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Подсчет времени работы функции
def measure_the_time(function) -> list:
    start = time.time()

    p = function()

    second = int((time.time() - start))

    minute = second // 60
    second = second - minute * 60

    hour = minute // 60
    minute = minute - hour * 60

    print(f'Программа отработала за {hour} ч. {minute} мин. {second} сек.')

    return p

def main():
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

    x = np.linspace(0, 2, n)
    f1 = 2 * np.exp(-2 * x)
    F1 = 1 - np.exp(-2 * x)
    plt.title('Исх. плотность распределения, функция распределения F')
    plt.plot(x, F1)
    plt.plot(x, f1)
    plt.legend(['F(x)', 'f(x)'])
    plt.show()

    nu = np.random.uniform(0, 1, n)
    ksi = - 1 / 2 * np.log(1 - nu)
    kl = 1 + int(np.log2(n))
    plt.hist(ksi, kl, density=True, alpha=0.5)

    # Оценка ф-ии распределения
    z = np.sort(ksi)
    nf = np.linspace(0, 1, n)
    plt.title('Функция распределения, гист. относ. частот')
    plt.plot(z, nf, 'k')
    plt.plot(x, F1)
    plt.hist(ksi, kl, density=True, cumulative=True, color='green', alpha=0.4)
    plt.show()

    pp = 8                    # число точек на печать
    m = np.mean(ksi)          # среднее
    median = np.median(ksi)   # медиана
    var = np.var(ksi)         # дисперсия
    print(f'Первые {pp} значений выборки\n'
          f'{z[:pp]}')
    print(f'Размах выборки: {z[-1] - z[1]}\n'  # Максимальное - минимальное
          f'Мат. ожидание: {m}\n'
          f'Медиана: {median}\n'
          f'Дисперсия: {var}')


if __name__ == '__main__':
    np.random.seed(19)
    np.set_printoptions(precision=3)

    measure_the_time(main)


