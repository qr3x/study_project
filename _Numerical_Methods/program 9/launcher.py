# Сторонние библиотеки
import numpy as np
from math import fabs
from decimal import Decimal, getcontext

# Мои модули


# 10 знаков после запятой
getcontext().prec = 10


def count_x(x: Decimal, h: Decimal) -> Decimal:
    return x + h


class Analysis(object):
    """
    Решение методом Рунге-Кутта
    """

    def __init__(self, data):
        self.data = data

        self.k1 = 0
        self.k2 = 0
        self.k3 = 0

        self.h = 0
        self.cb = 0

    def f(self, x: Decimal, u: Decimal) -> Decimal:
        R = -(self.data['a1'] * u + self.data['a3'] * u ** 3)

        return Decimal(R) / self.data['m']

    def count_k1(self, x: Decimal, v: Decimal, h: Decimal) -> Decimal:
        return self.f(x, v)

    def count_k2(self, x: Decimal, v: Decimal, h: Decimal) -> Decimal:
        tmp = h / 2
        return self.f(x + tmp, v + tmp * self.k1)

    def count_k3(self, x: Decimal, v: Decimal, h: Decimal) -> Decimal:
        return self.f(x + h, v + h * (-self.k1 + 2 * self.k2))

    def count_v(self, v: Decimal, h: Decimal) -> Decimal:
        return v + h / 6 * (self.k1 + 4 * self.k2 + self.k3)

    def create_message(self, n: int or str, x: list, v: Decimal, b: Decimal, arr_s: list,
                       step_s: list, step_p: list, h: list) -> str:
        """
        Создаем сообщение для справки
        :param n: кол-во сделанных шагов
        :param x: список из всех точек оси времени
        :param v: последнее значение точки на оси скорости
        :param b: правая граница
        :param arr_s: список всех S*
        :param step_s: список всех уменьшений шага
        :param step_p: список всех увеличений шага
        :param h: список всех шагов
        :return: Готовое сообщение для справки
        """

        message = '<p>Вариант №4</p>' \
                  '<p>Тип задачи: основная\n' \
                  '<p>Метод Рунге-Кутта порядок p=3 способ счета '

        if self.data['cbV'] == 0:
            message += '1 (Vn+1 итог = Vn+1)'
        elif self.data['cbV'] == 1:
            message += '1 (Vn+1 итог = Vn+1 удв)'
        else:
            message += '1 (Vn+1 итог = Vn+1 кор)'

        message = f'{message}</p>' \
                  f'<p>x<sub>0</sub> = {self.data["x0"]}; u<sub>0</sub> = {self.data["u0"]}</p>' \
                  f'<p>b = {self.data["b"]}; E<sub>гр</sub> = {self.data["Egr"]}</p>' \
                  f'<p>h<sub>0</sub> = {self.data["h"]}; N<sub>max</sub> = {self.data["n"]}</p>' \
                  f'<p>E = {self.data["E"]}; E<sub>min</sub> = {self.data["Emin"]}</p>' \
                  f'' \
                  f'<p>Контроль '

        if self.data['cb'] == 0:
            message += 'включен'
        elif self.data['cb'] == 1:
            message += 'включен только сверху'
        else:
            message += 'отключен'

        for i, elem in enumerate(arr_s):
            if i == 0:
                continue
            arr_s[i] = fabs(elem)
        index_hmin = min(range(len(h[1:])), key=h[1:].__getitem__) + 1
        index_hmax = max(range(len(h[1:])), key=h[1:].__getitem__) + 1

        message = f'{message}</p>' \
                  f'<p>Результат расчета:</p>' \
                  f'<p>N = {n}</p>' \
                  f'<p>b - x<sub>N</sub> = {b - x[-1]}</p>' \
                  f'<p>x<sub>N</sub> = {x[-1]}; V<sub>N итог</sub> = {v}</p>' \
                  f'<p>max|S| = {max(arr_s[1:])}</p>' \
                  f'<p>min|S| = {min(arr_s[1:])}</p>' \
                  f'<p>Всего ум. шага = {sum(step_s[1:])}</p>' \
                  f'<p>Всего ув. шага = {sum(step_p[1:])}</p>' \
                  f'<p>max h<sub>n</sub> = {h[index_hmax]} при x<sub>n+1</sub> = {x[index_hmax]}</p>' \
                  f'<p>min h<sub>n</sub> = {h[index_hmin]} при x<sub>n+1</sub> = {x[index_hmin]}</p>' \
                  f'<p>--------------------------------------------------------------------------------------------</p>'

        return message

    def work(self) -> dict:
        """
        Сам метод Рунге-Кутта 3ого порядка
        :return: dict вида {}
        """

        """ Списки, которые мы потом передадим в таблицу и графики """
        # Создаем список номера шага
        arr_n = ['0']
        # Создаем список для Hn-1. Первый элемент '---', далее сами шаги
        arr_hn_1 = ['---']
        # Список Xn
        arr_xn = [self.data['x0']]
        # Список Vn
        arr_vn = [self.data['u0']]
        # Список Vn удв (Vn с крышкой)
        arr_vn_ud = ['---']
        # Список S*
        arr_s = ['---']
        # Список Vn итог
        arr_vn_res = [self.data['u0']]
        # Список Ум. шага
        arr_step_s = ['---']
        # Список Ув. шага
        arr_step_p = ['---']

        """ Переменные """
        self.h = self.data['h']                  # Шаг
        self.cb = self.data['cb']                # Контроль погрешностей
        b_e = self.data['b'] - self.data['Egr']  # Левая граница промежутка контроля правой границы

        for n in range(1, self.data['n'] + 1):
            sub = 0   # Кол-во уменьшений шага
            plus = 0  # Кол-во увеличений шага
            while True:
                # Подсчет коэф. k для метода
                self.k1 = self.count_k1(arr_xn[-1], arr_vn_res[-1], self.h)
                self.k2 = self.count_k2(arr_xn[-1], arr_vn_res[-1], self.h)
                self.k3 = self.count_k3(arr_xn[-1], arr_vn_res[-1], self.h)

                # Подсчет X, V
                x = count_x(arr_xn[-1], self.h)
                v = self.count_v(arr_vn_res[-1], self.h)

                # Подсчет V с крышкой
                h = self.h / 2
                x1_2 = count_x(arr_xn[-1], h)
                v1_2 = self.count_v(arr_vn_res[-1], h)

                x1_2 = count_x(x1_2, h)
                v1_2 = self.count_v(v1_2, h)
                del h

                # Подсчет S*
                S = (v1_2 - v) / (2 ** self.data['p'] - 1)
                S = 2 ** self.data['p'] * S

                if self.cb == 0:    # Контроль погрешности сверху и снизу
                    if S == 0:  # Если оценка погрешности = 0, тогда ничего не делаем (иначе будет постоянно ув. шаг)
                        break
                    if self.data['Emin'] <= fabs(S) <= self.data['E']:
                        break
                    elif self.data['Emin'] > fabs(S):
                        self.h = 2 * self.h
                        plus += 1
                        break
                    else:  # |S*| > E
                        self.h = self.h / 2
                        sub += 1
                        continue
                elif self.cb == 1:  # Отказ от контроля погрешности снизу
                    if fabs(S) <= self.data['E']:
                        break
                    else:  # |S*| > E
                        self.h = self.h / 2
                        sub += 1
                        continue
                else:               # Отказ от контроля погрешности снизу и сверху
                    break
            if x > self.data['b']:  # Перепрыгнули правую границу (при больших шагах)
                break
            arr_n.append(str(n))
            arr_hn_1.append(self.h)
            arr_xn.append(x)
            arr_s.append(S)
            if v < 0 or v1_2 < 0:
                v = 0
                v1_2 = 0
                S = 0
            if self.data['cbV'] == 0:
                arr_vn_res.append(v)
            elif self.data['cbV'] == 1:
                arr_vn_res.append(v1_2)
            else:
                arr_vn_res.append(v + S)
            arr_vn.append(v)
            arr_vn_ud.append(v1_2)
            arr_step_p.append(plus)
            arr_step_s.append(sub)

            # Учет погрешности справа
            if b_e <= arr_xn[-1] <= self.data['b']:
                # Если попало в этот промежуток => (xn, vn) - последняя точка
                break

        message = self.create_message(arr_n[-1], arr_xn, arr_vn_res[-1], self.data['b'], arr_s,
                                      arr_step_s, arr_step_p, arr_hn_1)

        data = {
            'n': arr_n,
            'hn-1': arr_hn_1,
            'xn': arr_xn,
            'vn': arr_vn,
            'vn_ud': arr_vn_ud,
            'S*': arr_s,
            'vn_res': arr_vn_res,
            'step_decrease': arr_step_s,
            'step_increase': arr_step_p,
            'message': message
        }
        return data