"""
+ 1. Покупатели приходят в любой промежут (0t, 0.1t и тд). Задать лямбда,
+ 2. Стратегия отркрывания, закрывания касс (допустим когда 3 человек в очереди, открывать новую кассу)
+ 3. Поварьировать интенсивность касс
+ 4. почитать методичку. Пункт 1.2

сделать так, чтобы покупатель мог приходить в любой промежуток, а не только под начало периодов 0t, 1t и тп
чтобы он пришел, допустим в 6.3, тогда касса его обслужит за интенсивность делаеное на что-то (в общем чтобы была связь
между интенсивностью и оставшимся временем)
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from prettytable import PrettyTable
import os
from copy import deepcopy

from tills import RegularTill, SelfServiceTill


# Чистим экран (консоль) для разных ОС
def _cls() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def get_clients(n: int) -> np.array:
    """
    >> Задаем распределение Пуассона для получение кол-во человек, пришедших в промежутки времени
    LIAMBDA - параметр лямбда для распределения Пуассона
    size=n + 1 - Сколько промежутков - такой и размер, т.е. мы создаем кол-во людей пришедших в каждый промежуток

    >> Для каждого покупателя выбираем случайное кол-во продуктов, которые он хочет купить в диапозоне
       от 1 до MAX_PRODUCTS

    >> Сопоставляем продукты к каждому покупателю
    :param n: кол-во временных промежутков
    :return:
    """

    customers_tmp = st.poisson.rvs(LIAMBDA, size=n)
    products = np.array([np.random.randint(1, MAX_PRODUCTS) for i in range(sum(customers_tmp))])

    customers = np.array([])
    for i, count_cust in enumerate(customers_tmp):
        tmp = sum(customers_tmp[:i])  # Находим диапозон, который нужно взять из products
        customers = np.append(customers, {'count': count_cust, 'products': products[tmp:tmp+count_cust]})

    return customers


def queuing_strategy(reg_tills: RegularTill, ss_tils: SelfServiceTill) -> tuple:
    """ Стратегия организации очередей
    Покупатель идет на кассу, где меньше людей
    :param reg_tills: объект общих касс
    :param ss_tils: объект касс самобслуживания
    :return: активную (обычную или самообслуживания) кассу и индекс очереди (номер кассы). Примеры:
    (RegularTill, 0) если на первой обычной кассе меньше людей
    (RegularTill, 1) если на второй обычной кассе меньше людей
    (SelfServiceTill, 0) если на кассы самообслуживания меньше людей
    """

    # если все обычные кассы закрыты => покупатель идет на кассы самообслуживания
    if reg_tills.count == 0:
        return ss_tils, 0

    # находим наименьшее количество людей в очередях на обычные кассыч
    min_reg_length = -1
    index = -1
    for i, till in enumerate(reg_tills.tills):
        # если касса открыта, то сравниваем с минимальным значением очереди
        if till['open']:
            length = len(till['queue'])
            if min_reg_length > length or min_reg_length == -1:
                min_reg_length = length
                index = i

    # все обычные кассы закрыты
    if min_reg_length == -1:
        return ss_tils, 0

    ss_length = len(ss_tils.queue[0])  # считаем кол-во людей в очереди к кассам самообслуживания

    # покупатель идет на кассу, где меньше людей. Если людей одинаково, то на обычную кассу, так как там быстрее обсужат
    if min_reg_length <= ss_length:
        return reg_tills, index
    return ss_tils, 0


def count(reg_tills: RegularTill, ss_tills: SelfServiceTill) -> None:
    """ Подсчитываем очереди на момент окончания времени (t, ∆ t)
    :param reg_tills: объект общих касс
    :param ss_tills: объект касс самобслуживания
    """

    def sub(tills: RegularTill or SelfServiceTill, index: int) -> None:
        intensity = tills.intensity  # Получаем интенсивность кассы
        pops = 0
        length = len(tills.queue[index])
        for i in range(length):
            if intensity >= tills.queue[index][i]:  # если интенсивность больше, чем продуктов у покупателя
                intensity -= tills.queue[index][i]
                pops += 1  # Счетчик удаления обслуженных клиентов
                # Если это был последний клиент и интенсивность больше, чем товаров,
                # то просто убираем клиента из очереди, тк обслужили
                if length == pops:
                    for pop in range(pops - 1, -1, -1):
                        tills.queue[index].pop(pop)
                    break
            else:
                # если интенсивности не хватает, чтобы обслужить этого клиента,
                # то удаляем из очереди тех, кого обслужили, а этого дообслужат в следующий промежуток времени
                tills.queue[index][i] -= intensity
                for pop in range(pops - 1, -1, -1):
                    tills.queue[index].pop(pop)
                break

    for i in range(reg_tills.count):
        sub(reg_tills, i)

    sub(ss_tills, 0)


def check_open_close_tills(reg_tills: RegularTill, ss_tills: SelfServiceTill) -> None:
    """ Проверяет кассы на очереди и решает, открывать, закрывать кассы или ничего с ними не делать
    Если в очереди 3 и больше людей, то открываем новую кассу
    :param reg_tills: объект общих касс
    :param ss_tills: объект касс самобслуживания
    """

    # Общ интенсивность = кол-во обычных касс * на их интенсивность + кол-во касс самообслуживания * на их интенсивность
    general_intensity = reg_tills.count * reg_tills.intensity + ss_tills.count + ss_tills.intensity

    # Смотрим на обычные кассы
    for queue in reg_tills.queue:
        # Если в какой-то очереди людей больше, чем макс. число людей в очереди => открываем обычную кассу
        if len(queue) >= MAX_QUEUE:
            reg_tills.open_till()
            break
    # Если во всех обычных кассах людей меньше, чем макс. число людей
    else:
        # Если в очереди для касс самообслуживания людей больше максимального количества => открываем обычную кассу
        if len(ss_tills.queue[0]) >= MAX_QUEUE:
            reg_tills.open_till()
        # Если во всех кассах (и обычных, и самообсулижвания) людей меньше максимального значения => закрываем об. кассу
        else:
            reg_tills.close_till()


def main(n: int) -> dict:
    """ Сбор для графиков и таблиц """
    queue_reg_1 = []
    queue_reg_2 = []
    queue_ss = []

    open_reg_1 = []
    open_reg_2 = []
    """ -------------------------- """

    # Создаем объекты касс
    regular_tills = RegularTill(2)
    selfservice_tills = SelfServiceTill(2)

    # Получаем входной поток клиентов с их заказами
    customers = get_clients(n)

    print(customers)
    for timeframe in range(len(customers)):
        # Добавляем данные для графиков и таблиц

        open_reg_1.append(regular_tills.tills[0]['open'])
        open_reg_2.append(regular_tills.tills[1]['open'])

        products = np.array([])
        for i, product in enumerate(customers[timeframe]['products']):
            products = np.append(products, product)
            till, index = queuing_strategy(regular_tills, selfservice_tills)
            till.add_customer(index, product)
        print(regular_tills.queue)
        print(selfservice_tills.queue)

        # Смотрим стоит ли открывать или закрывать кассы
        check_open_close_tills(regular_tills, selfservice_tills)

        queue_reg_1.append(deepcopy(regular_tills.queue[0]))
        queue_reg_2.append(deepcopy(regular_tills.queue[1]))
        queue_ss.append(deepcopy(selfservice_tills.queue[0]))

        count(regular_tills, selfservice_tills)

    return {'times': [i for i in range(len(customers))],
            'products': [customers[timeframe]['products'] for timeframe in range(len(customers))],
            'queue_reg_1': queue_reg_1, 'open_reg_1': open_reg_1,
            'queue_reg_2': queue_reg_2, 'open_reg_2': open_reg_2,
            'queue_ss': queue_ss}


if __name__ == '__main__':
    np.random.seed()

    LIAMBDA = 3
    MAX_QUEUE = 3
    MAX_PRODUCTS = 10

    # Ввод с отловом ошибок
    while True:
        try:
            n = int(input('Введите количество единиц времени: '))
            break
        except ValueError:
            _cls()
            print('Вы ввели не число. Попробуйте снова')

    data = main(n)
    table = PrettyTable()
    table.field_names = ['t', 'Входной поток', 'Общая очередь', 'Очередь в 1ую обычную кассу', 'Открыта ли 1ая касса',
                         'Очередь в 2ую обычную кассу', 'Открыта ли 2ая касса', 'Общая очередь в кассы самообслуживания']

    for i in range(data['times'][-1] + 1):
        queue_reg_1 = data['queue_reg_1'][i]
        queue_reg_2 = data['queue_reg_2'][i]
        queue_ss = data['queue_ss'][i]
        table.add_row([f"{data['times'][i]}t", data['products'][i], sum(queue_reg_1) + sum(queue_reg_2) + sum(queue_ss),
                       f'{sum(queue_reg_1)} {queue_reg_1}', data['open_reg_1'][i],
                       f'{sum(queue_reg_2)} {queue_reg_2}', data['open_reg_2'][i],
                       f'{sum(queue_ss)} {queue_ss}'])
    print(table)
