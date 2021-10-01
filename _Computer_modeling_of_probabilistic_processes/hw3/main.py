import random
import os
import time


# Чистим экран (консоль) для разных ОС
def _cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Подсчет времени работы функции
def measure_the_time(function):
    start = time.time()

    function()

    second = int((time.time() - start))

    minute = second // 60
    second = second - minute * 60

    hour = minute // 60
    minute = minute - hour * 60

    print(f'Программа отработала за {hour} ч. {minute} мин. {second} сек.')


# рекурентный подход
def c_r(n: int, k: int) -> int:
    if k == 0 or k == n:
        return 1
    else:
        return c_r(n - 1, k - 1) + c_r(n - 1, k)


# оптимизированный подход
def c_o(n: int, k: int) -> int:
    """
    Через треугольник паскаля
    """

    def fact(number: int) -> list:
        return [i for i in range(1, number + 1)]

    def reduction(list1: list, list2: list) -> tuple:
        tmp = []  # Удаленные числа из 2 списка
        for elem in list1:
            try:
                list2.remove(elem)
                tmp.append(elem)
            except ValueError:
                # Если нет такого элемента в списке
                pass

        for elem in tmp:
            list1.remove(elem)

        return list1, list2

    def prod(list1: list) -> int:
        p = 1
        for elem in list1:
            p *= elem

        return p

    numerator = fact(n)
    denominator = fact(n - k)
    fact_k = fact(k)
    denominator.extend(fact_k)

    # Считаем числитель и знаменатель
    # Числитель - список из чисел факториала
    # Знаменатель - список (два совмещенных списка) из чисел факториалов
    numerator, denominator = reduction(numerator, denominator)

    # Считаем число сочетаний
    return prod(numerator) // prod(denominator)


class Exam(object):

    def __init__(self, n=0, questions=0, questions_ready=0):
        if n == 0:
            n = int(input('Количество эксперементов: '))
        self.n = n
        if questions == 0:
            questions = int(input('Количество вопросов: '))
        self.questions = questions
        if questions_ready == 0:
            questions_ready = int(input('Количество выученных вопросов: '))
        self.questions_ready = questions_ready

        self.m = 0

    def work(self):
        for i in range(self.n): 
            q = [num for num in range(1, self.questions + 1)]

            r1 = random.choice(q)
            q.remove(r1)
            r2 = random.choice(q)
            q.remove(r2)

            print(f'r: {r1}, {r2}')
            if r1 <= self.questions_ready and r2 < self.questions_ready:
                self.m += 1
            elif r1 <= self.questions_ready or r2 < self.questions_ready:
                r3 = random.choice(q)
                print(f'r3: {r3}')
                if r3 < self.questions_ready:
                    self.m += 1

            print(f'm = {self.m}; n = {i + 1}')

        p = self.m / self.n
        th = c_r(self.questions_ready, 2) / c_r(self.questions, 2) + \
            c_r(self.questions_ready - 1, 1) / c_r(self.questions - 2, 2)
        print(f'Посчитанная вероят. на компьютере: {p}\n'
              f'Посчитанная по числу сочетаний: {th}')


def main():
    random.seed(17)

    model = Exam()
    model.work()


if __name__ == '__main__':
    measure_the_time(main)
