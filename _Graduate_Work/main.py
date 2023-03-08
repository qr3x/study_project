"""
+ 1. Сделать ещё один прогон, но только по коэф. ошибки [.1, .5, 1, 10, 100, 1000]
2. Сделать графики коэф. эффективности от кол-во минут в одном промежутке
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from prettytable import PrettyTable
import os
from copy import deepcopy
import time

from tills import RegularTill, SelfServiceTill


# Чистим экран (консоль) для разных ОС
def _cls() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def get_clients(n: int) -> np.array:
    """
    >> Задаем распределение Пуассона для получение кол-во человек, пришедших в промежутки времени
    LIAMBDA - параметр лямбда для распределения Пуассона
    size=n - Сколько промежутков - такой и размер, т.е. мы создаем кол-во людей пришедших в каждый промежуток

    >> Для каждого покупателя выбираем случайное кол-во продуктов, которые он хочет купить в диапозоне
       от 1 до MAX_PRODUCTS

    >> Сопоставляем продукты к каждому покупателю
    :param n: кол-во временных промежутков
    :return: массив покупателей
    """

    customers_tmp = st.poisson.rvs(LIAMBDA, size=n)

    customers = np.array([])
    for count_cust in customers_tmp:
        products = np.array([np.random.randint(1, MAX_PRODUCTS) for j in range(count_cust)])
        products = np.array(products, dtype=float)
        moments = np.array(sorted([np.random.random() for j in range(count_cust)]))
        wait = np.zeros(count_cust, dtype=float)
        customers = np.append(customers, {'count': count_cust,
                                          'products': products,
                                          'moments': moments,
                                          'wait': wait})

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


def count(reg_tills: RegularTill, ss_tills: SelfServiceTill) -> float:
    """ Подсчитываем очереди на момент окончания времени (t, ∆ t)
    :param reg_tills: объект общих касс
    :param ss_tills: объект касс самообслуживания
    :return:
    """

    def sub(tills: RegularTill or SelfServiceTill, index: int) -> float:
        general_wait = 0

        general_intensity = tills.intensity  # Получаем интенсивность кассы
        general_moment = 0
        pops = 0

        for i, customer in enumerate(tills.queue[index]):
            product = customer['products']                                  # кол-во продуктов у покупателя
            moment = customer['moments']                                    # момент, в который пришел покупатель

            moment = moment if moment > general_moment else general_moment  # текущий момент
            intensity = general_intensity * (1 - moment)                    # текущая интенсивность

            # если интенсивность больше, чем продуктов у покупателя
            if intensity >= product:
                pops += 1                                           # счетчик удаления обслуженных клиентов
                intensity -= product                                # считаем, сколько ещё товаров можем обслужить
                general_moment = 1 - intensity / general_intensity  # высчитываем, какой сейчас момент времени

                general_wait += general_moment - moment
                # подсчет, если следующий ждет обслуживания предыдущего
                for j in range(i + 1, len(tills.queue[index])):
                    new_customer = tills.queue[index][j]  # следующий покупатель
                    new_moment = new_customer['moments']  # момент, в который пришел следующий покупатель

                    # если покупатель ждал предыдущего, то считаем время ожидания
                    if general_moment > new_moment:
                        general_wait += general_moment - new_moment
                    # если не ждал, то выходим из цикла, тк следующие его точно не ждали
                    else:
                        break

                # если последний элемент
                if pops == len(tills.queue[index]):
                    break
            # если интенсивности не хватает, чтобы обслужить этого клиента
            else:
                tills.queue[index][i]['products'] -= intensity
                for j in range(i + 1, len(tills.queue[index])):
                    general_wait += 1 - customer['moments']

        for i, customer in enumerate(tills.queue[index]):
            tills.queue[index][i]['moments'] = 0

        # убираем из очереди обслуженных людей
        for pop in range(pops - 1, -1, -1):
            tills.queue[index].pop(pop)

        return general_wait

    wait = 0
    for i in range(reg_tills.count):
        wait += sub(reg_tills, i)

    wait += sub(ss_tills, 0)

    return wait


def check_open_close_tills(reg_tills: RegularTill, ss_tills: SelfServiceTill) -> None:
    """ Проверяет кассы на очереди и решает, открывать, закрывать кассы или ничего с ними не делать
    Если в очереди 3 и больше людей, то открываем новую кассу
    :param reg_tills: объект общих касс
    :param ss_tills: объект касс самообслуживания
    """

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


def main(n: int, time_for_tills: int) -> dict:
    """ Сбор для графиков и таблиц """
    queue_reg_1 = []  # Очередь в первую кассу
    queue_reg_2 = []  # Очередь во вторую кассу
    queue_ss = []     # Общая очередь в кассы самообслуживания

    open_reg_1 = []   # Открыта ли 1ая касса
    open_reg_2 = []   # Открыта ли 2ая касса
    """ -------------------------- """

    # Создаем объекты касс
    regular_tills = RegularTill(2, time_for_tills)
    selfservice_tills = SelfServiceTill(2, time_for_tills)

    # Получаем входной поток клиентов с их заказами
    customers = get_clients(n)

    wait = 0
    for timeframe in range(len(customers)):
        # Добавляем данные для графиков и таблиц
        open_reg_1.append(regular_tills.tills[0]['open'])
        open_reg_2.append(regular_tills.tills[1]['open'])

        products = np.array([])
        for product, moment in zip(customers[timeframe]['products'], customers[timeframe]['moments']):
            products = np.append(products, product)
            till, index = queuing_strategy(regular_tills, selfservice_tills)
            till.add_customer(index, {'products': product, 'moments': moment})

        # Смотрим, стоит ли открывать или закрывать кассы
        check_open_close_tills(regular_tills, selfservice_tills)

        # queue_reg_1.append(deepcopy(regular_tills.queue[0]))
        # queue_reg_2.append(deepcopy(regular_tills.queue[1]))
        # queue_ss.append(deepcopy(selfservice_tills.queue[0]))

        wait += count(regular_tills, selfservice_tills)

        queue_reg_1.append(deepcopy(regular_tills.queue[0]))
        queue_reg_2.append(deepcopy(regular_tills.queue[1]))
        queue_ss.append(deepcopy(selfservice_tills.queue[0]))

    return {'times': [i for i in range(len(customers))],
            'products': [customers[timeframe]['products'] for timeframe in range(len(customers))],
            'moments': [customers[timeframe]['moments'] for timeframe in range(len(customers))],
            'wait': wait,
            'queue_reg_1': queue_reg_1, 'open_reg_1': open_reg_1,
            'queue_reg_2': queue_reg_2, 'open_reg_2': open_reg_2,
            'queue_ss': queue_ss}


def count_fine(coef: float or int, arr: list) -> float:
    """ Считает коэффициент штрафа
    :param coef: коэффициент ошибки
    :param arr: список с открыта/закрыта касса
    :return: коэффициент ошибки
    """

    fine = 0
    latest_value = False
    for i, elem in enumerate(arr):
        if elem is True and latest_value is False:
            fine += coef
        latest_value = elem

    return fine


if __name__ == '__main__':
    np.random.seed()

    # # Ввод с отловом ошибок
    # while True:
    #     try:
    #         n = int(input('Введите количество единиц времени: '))
    #         if n <= 0:
    #             _cls()
    #             print('Нужно ввести положительное число. Попробуйте снова')
    #             continue
    #         break
    #     except ValueError:
    #         _cls()
    #         print('Вы ввели не число. Попробуйте снова')

    # while True:
    #     try:
    #         time_for_tills = float(input('Введите кол-во минут в единице времени: '))
    #         if time_for_tills <= 0:
    #             _cls()
    #             print('Нужно ввести положительное число. Попробуйте снова')
    #             continue
    #         break
    #     except ValueError:
    #         _cls()
    #         print('Нужно ввести целое число. Попробуйте снова')

    # while True:
    #     print_info = input('Показать таблицу и графики (+ да, - нет): ')
    #     if print_info not in ['+', '-']:
    #         _cls()
    #         print('Вы ввели не + или -. Попробуйте снова')
    #         continue
    #     if print_info == '+':
    #         print_info = True
    #     else:
    #         print_info = False
    #     break

    start = time.time()

    const = 100
    arr_time_for_tills = np.arange(1, 10, 1)
    coefs_fine = [.1, .5, 1, 10, 100, 1000]
    print_info = True
    data_for_coef = {}
    for index, coef_fine in enumerate(coefs_fine):
        data_for_coef[coef_fine] = {}
        ns = []
        coefs = []
        for time_for_tills in arr_time_for_tills:
            n = int(const // time_for_tills)
            ns.append(n)
            """ -------------------------------------------Глобальные параметры------------------------------------------- """

            LIAMBDA = 3 * time_for_tills
            MAX_QUEUE = 3
            MAX_PRODUCTS = 8

            """ -------------------------------------------/Глобальные параметры------------------------------------------- """

            data = main(n, time_for_tills)

            """ --------------------------------------------------Таблица-------------------------------------------------- """
            table = PrettyTable()
            table.field_names = ['t', 'Входной поток', 'Момент, в который пришли', 'Общая очередь',
                                 'Очередь в 1ую обычную кассу', 'Открыта ли 1ая касса',
                                 'Очередь в 2ую обычную кассу', 'Открыта ли 2ая касса',
                                 'Общая очередь в кассы самообслуживания']

            count_queue_reg_1__client = []    # кол-во людей в очереди на 1ую обычную кассу
            count_queue_reg_2__client = []    # кол-во людей в очереди на 2ую обычную кассу
            count_queue_ss__client = []       # кол-во людей в очереди на кассы самообслуживания
            count_queue_reg_1__products = []  # кол-во продуктов в очереди на 1ую обычную кассу
            count_queue_reg_2__products = []  # кол-во продуктов в очереди на 2ую обычную кассу
            count_queue_ss__products = []     # кол-во продуктов в очереди на кассы самообслуживания
            for i in range(n):
                """ ---------------------------------------------Первая очередь--------------------------------------------- """

                queue_reg_1__products = []
                for client in data['queue_reg_1'][i]:
                    queue_reg_1__products.append(client['products'])

                queue_reg_1__moments = []
                for client in data['queue_reg_1'][i]:
                    queue_reg_1__moments.append(client['moments'])
                count_queue_reg_1__client.append(len(queue_reg_1__products))
                count_queue_reg_1__products.append(sum(queue_reg_1__products))

                """ ---------------------------------------------Вторая очередь--------------------------------------------- """

                queue_reg_2__products = []
                for client in data['queue_reg_2'][i]:
                    queue_reg_2__products.append(client['products'])

                queue_reg_2__moments = []
                for client in data['queue_reg_2'][i]:
                    queue_reg_2__moments.append(client['moments'])
                count_queue_reg_2__client.append(len(queue_reg_2__products))
                count_queue_reg_2__products.append(sum(queue_reg_2__products))

                """ ----------------------------------------Очередь самообслуживания---------------------------------------- """

                queue_ss__products = []
                for client in data['queue_ss'][i]:
                    queue_ss__products.append(client['products'])

                queue_ss__moments = []
                for client in data['queue_ss'][i]:
                    queue_ss__moments.append(client['moments'])
                count_queue_ss__client.append(len(queue_ss__products))
                count_queue_ss__products.append(sum(queue_ss__products))

                if print_info:
                    table.add_row([f"{data['times'][i]}t", data['products'][i], data['moments'][i],
                                   sum(queue_reg_1__products) + sum(queue_reg_2__products) + sum(queue_ss__products),
                                   f'{sum(queue_reg_1__products)} {queue_reg_1__products}', data['open_reg_1'][i],
                                   f'{sum(queue_reg_2__products)} {queue_reg_2__products}', data['open_reg_2'][i],
                                   f'{sum(queue_ss__products)} {queue_ss__products}'])
            if print_info:
                print(table)

            count_open_req_1 = 0
            count_open_req_2 = 0
            count_open_req_1_and_2 = 0
            for i in range(data['times'][-1] + 1):
                if data['open_reg_1'][i]:
                    count_open_req_1 += 1
                    if data['open_reg_2'][i]:
                        count_open_req_1_and_2 += 1
                if data['open_reg_2'][i]:
                    count_open_req_2 += 1

            # среднее время нахождения человека в очереди
            average_time = data['wait'] / sum([len(elem) for elem in data['products']]) * time_for_tills
            # средняя длина очереди
            average_len = 0.
            for i in range(data['times'][-1] + 1):
                average_len += count_queue_reg_1__client[i]
                average_len += count_queue_reg_2__client[i]
                average_len += count_queue_ss__client[i]
            average_len /= (data['times'][-1] + 1) * 3

            fine1 = count_fine(coef_fine, data['open_reg_1'])
            fine2 = count_fine(coef_fine, data['open_reg_2'])
            time_for_coef = n * time_for_tills
            coef = average_time + fine1 / time_for_coef + fine2 / time_for_coef
            coefs.append(coef)

            text = f'\n----------------------------------------------Анализ----------------------------------------------\n\n' \
                   f'Кассы:\n' \
                   f'Кол-во промежутков, когда была открыта 1ая обычная касса: {count_open_req_1}\n' \
                   f'Кол-во промежутков, когда была открыта 2ая обычная касса: {count_open_req_2}\n' \
                   f'Кол-во промежутков, когда была открыта одна касса: {count_open_req_1 - count_open_req_1_and_2 + count_open_req_2 - count_open_req_1_and_2}\n' \
                   f'Кол-во промежутков, когда были открыты все обычные кассы: {count_open_req_1_and_2}\n' \
                   f'\n' \
                   f'Максимальное кол-во покупателей на кассе:\n' \
                   f'1ая обычная касса: {max(count_queue_reg_1__client)}\n' \
                   f'2ая обычная касса: {max(count_queue_reg_2__client)}\n' \
                   f'Кассы самообслуживания: {max(count_queue_ss__client)}\n' \
                   f'\n' \
                   f'Максимальное количество продуктов на кассах:\n' \
                   f'1ая обычная касса: {max(count_queue_reg_1__products)}\n' \
                   f'2ая обычная касса: {max(count_queue_reg_2__products)}\n' \
                   f'Кассы самообслуживания: {max(count_queue_ss__products)}\n' \
                   f'\n' \
                   f'Среднее время обслуживания: {average_time}t\n' \
                   f'Средняя длина очереди на конец промежутка: {average_len}\n' \
                   f'\n' \
                   f'Эффективность (чем меньше, тем лучше): {coef}'
            print(text)

            """ --------------------------------------------------Графики-------------------------------------------------- """
            if print_info:
                x = [i for i in range(data['times'][-1] + 1)]

                plt.title('Загруженность касс (Кол-во людей)')
                plt.plot(x, [count_queue_reg_1__client[i] + count_queue_reg_2__client[i] + count_queue_ss__client[i] for i in
                             range(data['times'][-1] + 1)], 'r-', label='Общая очередь')
                plt.plot(x, count_queue_reg_1__client, 'b-', label='Очередь первой обычной кассы')
                plt.plot(x, count_queue_reg_2__client, 'g-', label='Очередь второй обычной кассы')
                plt.plot(x, count_queue_ss__client, 'y-', label='Очередь касс самообслуживания')
                plt.legend()
                plt.show()

                plt.title('Загруженность касс (Кол-во продуктов)')
                plt.plot(x, [count_queue_reg_1__products[i] + count_queue_reg_2__products[i] + count_queue_ss__products[i]
                             for i in range(data['times'][-1] + 1)], 'r-', label='Общая очередь')
                plt.plot(x, count_queue_reg_1__products, 'b-', label='Очередь первой обычной кассы')
                plt.plot(x, count_queue_reg_2__products, 'g-', label='Очередь второй обычной кассы')
                plt.plot(x, count_queue_ss__products, 'y-', label='Очередь касс самообслуживания')
                plt.legend()
                plt.show()

        """ -------------------------------------------Таблица эффективности------------------------------------------- """

        table = PrettyTable()
        table.title = 'Исходная таблица'
        table.field_names = ['№', 'Кол-во промежутков t', 'Кол-во минут в одном промежутке', 'Коэффициент эффективности']
        for i, (time_for_tills, coef, n) in enumerate(zip(arr_time_for_tills, coefs, ns)):
            table.add_row([i + 1, n, time_for_tills, coef])
        print(table)

        table.title = 'Отсортированная таблица по коэф. эффективности'
        print(table.get_string(sortby='Коэффициент эффективности'))

        """ -------------------------------------------График эффективности------------------------------------------- """

        rows = table._rows
        data_for_coef[coef_fine]['x'] = []
        data_for_coef[coef_fine]['y'] = []
        for elem in rows:
            data_for_coef[coef_fine]['x'].append(elem[2])
            data_for_coef[coef_fine]['y'].append(elem[3])

    plt.title = f'График эффективности'
    plt.xlabel('Эффективность (меньше=лучше)')
    plt.ylabel('Кол-во минут в промежутке')
    for elem in data_for_coef.keys():
        x = data_for_coef[elem]['x']
        y = data_for_coef[elem]['y']
        plt.plot(x, y, label=f'График для коэф.ошибки={elem}')
    plt.legend()
    plt.show()

    """ -------------------------------------------Время работы программы------------------------------------------- """

    second = time.time() - start
    minute = second // 60
    second -= 60 * minute
    hour = minute // 60
    minute -= 60 * hour
    print(f'\n\nПрограмма отработала за {int(hour)}ч. {int(minute)}мин. {second}сек.')
