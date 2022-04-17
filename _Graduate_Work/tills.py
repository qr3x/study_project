class RegularTill(object):
    """
    Обычные кассы

    max_count - максимальное количество обычных касс
    count - открыто касс в данный момент времени
    speed - количество продуктов, которые обслуживает касса за единицу времени

    queue - очереди для касс
    """

    def __init__(self, max_count: int, time: int):
        """
        :param max_count: максимальное количество обычных касс
        """
        self.max_count = max_count
        self.count = 0
        self.coefficient = 1 / 4
        self.intensity = float(time * 60 * self.coefficient)
        # self.intensity = 15.

        self.tills = []
        for number in range(max_count):
            # Если касса "open" открыта - True, закрыта - False
            self.tills.append({'open': False, 'queue': []})
        self.queue = [self.tills[i]['queue'] for i in range(self.max_count)]

    def open_till(self) -> str:
        for till in self.tills:
            # Если касса закрыта
            if not till['open']:
                self.count += 1
                till['open'] = True
                break
        else:
            return 'все кассы открыты'

    def close_till(self, index=-1) -> str:
        result = ''
        # Если выбрана касса, которую нужно закрыть - закрываем ее
        if index != -1:
            self.count -= 1
            self.tills[index]['open'] = False
            result = 'Закрыли кассу'
        # Если поступило условие, что нужно закрыть кассу, но не какую-то определенную, то ищем кассу,
        # которая открыта и где нет покупателей
        else:
            for till in self.tills:
                if till['open'] and till['queue'] == []:
                    self.count -= 1
                    till['open'] = False
                    result = 'Закрыли кассу'
                    break
            else:
                result = 'Нет касс, которые можно закрыть (На них ещё есть покупатели)'

        return result

    def add_customer(self, index: int, customer) -> None:
        self.queue[index].append(customer)


class SelfServiceTill(object):
    """
    Кассы самообслуживания

    count - количество касс самообслуживания
    speed - количество продуктов, которые обслуживает касса за единицу времени

    queue - общая очередь для всех касс
    """

    def __init__(self, count: int, time: int):
        """
        :param count: количество касс самообслуживания
        """
        self.count = count
        self.coefficient = 1 / 3
        self.intensity = float(time * 60 * self.coefficient)
        # self.intensity = 20.  # 2 кассы с интенсивностью 10

        self.queue = [[]]

    def add_customer(self, index: int, customer) -> None:
        self.queue[index].append(customer)
