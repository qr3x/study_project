"""
5 вариант
Отображение Гаусса: xn+1 = liam + exp(-3(xn)^2), -1 < liam < 1
единственная неподвижная точка x=0 (сверхустойчива)
биф. вилка с одним периодом (в 1 и 3 четвертях). Динамического хаоса нет
"""

import matplotlib.pyplot as plt
import numpy as np


def biff():
    def rhs(liam=-1, border=200):
        """
        Строим график от a до a+2
        :param liam: параметр лямбда
        :param border: граница точек (построит 200 точек с шагом 0.01)
        :return: два массива координат, по x и по y
        """

        x = np.array([0])  # Лямбда
        y = np.array([0])  # результат подсчетов
        # идем 100 шагов, начиная с liam до liam+1 с шагом 0.01
        for i in range(border):
            for j in range(300):
                y1 = liam * np.exp(-3 * y[-1] ** 2)
                x = np.append(x, liam)
                y = np.append(y, y1)
            liam += .01

        return [x, y]
    return rhs


def main():
    rhs = biff()

    x, y = rhs()
    plt.xlabel('λ')
    plt.ylabel('x*')
    plt.plot(x, y, 'bo', ms=1)
    plt.show()


if __name__ == '__main__':
    main()
