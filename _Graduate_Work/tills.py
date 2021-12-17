class RegularTill(object):
    """
    Обычные кассы

    max_count - максимальное количество обычных касс
    count     - открыто касс в данный момент времени
    speed     - количество продуктов, которые обслуживает касса за единицу времени

    queue     - очереди для касс
    """

    def __init__(self, max_count: int):
        """
        :param max_count: максимальное количество обычных касс
        """
        self.max_count = max_count
        self.count = 0
        self.intensity = 10

        self.tills = []
        for number in range(max_count):
            # Если касса "open" открыта - True, закрыта - False
            self.tills.append({'open': False, 'queue': []})
        self.queue = [self.tills[i]['queue'] for i in range(self.max_count)]

    def open_till(self) -> None:
        for till in self.tills:
            # Если касса закрыта
            if not till['open']:
                self.count += 1
                till['open'] = True
                break
        else:
            print('все кассы открыты')

    def close_till(self, index=-1) -> None:
        # Если выбрана касса, которую нужно закрыть - закрываем ее
        if index != -1:
            self.count -= 1
            self.tills[index]['open'] = False
            print('Закрыли кассу')
        # Если поступило условие, что нужно закрыть кассу, но не какую-то определенную, то ищем кассу,
        # которая открыта и где нет покупателей
        else:
            for till in self.tills:
                if till['open'] and till['queue'] == []:
                    self.count -= 1
                    till['open'] = False
                    print('Закрыли кассу')
            print('Нет касс, которые можно закрыть (На них ещё есть покупатели)')

    def add_customer(self, index: int, customer) -> None:
        self.queue[index].append(customer)


class SelfServiceTill(object):
    """
    Кассы самообслуживания

    count     - количество касс самообслуживания
    speed     - количество продуктов, которые обслуживает касса за единицу времени

    queue - общая очередь для всех касс
    """

    def __init__(self, count: int):
        """
        :param count: количество касс самообслуживания
        """
        self.count = count
        self.intensity = 14  # 2 кассы с интенсивность 7

        self.queue = [[]]

    def add_customer(self, index: int, customer) -> None:
        self.queue[index].append(customer)