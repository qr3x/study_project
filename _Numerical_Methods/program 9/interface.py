# Сторонние библиотеки
# настройка окна
from PyQt5.QtWidgets import (QMainWindow, QAction)

"""Инструменты для макета"""
# диалоговые окна
from PyQt5.QtWidgets import QMessageBox, QInputDialog
# инструменты для шаблона
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QLabel, QComboBox, QLineEdit, QWidget, QHBoxLayout,
                             QVBoxLayout, QPlainTextEdit, QFrame)
# стилистика
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Графики
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Числа с плавающей запятой
from decimal import Decimal


# Мои модули
from launcher import Analysis
from config import float_to_str


matplotlib.use('Qt5Agg')


class Window(object):

    def __init__(self, path_to_options):
        """
        Инициализируем наше окно
        :param path_to_options: путь до директории с файлами настройки
        """

        self.path_to_options = path_to_options

        # Устанавливаем окно с его настройками
        self.window = QMainWindow()
        self.window.setWindowState(Qt.WindowMaximized)
        self.window.setWindowTitle("Программа для задачи №9. Кишкин Владислав 381903-3")
        self.window.setWindowIcon(QIcon('options\\favicon.ico'))

        # Меню
        self.window.statusBar()
        menubar = self.window.menuBar()
        self.dialog_message = QMessageBox()
        self.dialog_input = QInputDialog()
        self.dialog_message.setStyleSheet('QMessageBox { font-size: 13pt;}; ')

        # Кнопка "Начать"
        self.workMenu = QAction('&Начать')
        self.workMenu.triggered.connect(self.work)

        # Кнопка "Условия задачи"
        self.conditionMenu = QAction('&Условия задачи')
        self.conditionMenu.triggered.connect(self.condition)

        # Кнопка "О методе"
        self.rkm = QAction('&О методе')
        self.rkm.triggered.connect(self.rungeKutta_method)

        menubar.addAction(self.workMenu)
        menubar.addAction(self.conditionMenu)
        menubar.addAction(self.rkm)

        # Настраиваем макет
        self.initUI()

        self.window.show()

    def initUI(self):
        """
        Строим начальный макет окна
        """

        # Порядок метода
        self.p = 3

        """-----------------------------------------Гланый блок с подблоками-----------------------------------------"""
        main = QWidget(self.window)
        mainHBox1 = QHBoxLayout()
        mainHBox2 = QHBoxLayout()
        mainHBox2.setSpacing(21)
        mainVBox = QVBoxLayout()

        """-------------------------------------------Блок с настройками---------------------------------------------"""
        option = QWidget(main)
        option.setStyleSheet('QLineEdit { border: none; }'
                             'QLabel { font-size: 10pt; };')
        option.setFixedSize(910, 530)
        optionVBox = QVBoxLayout()
        optionVBox.setSpacing(13)

        optionHBox1 = QHBoxLayout()
        optionHBox2 = QHBoxLayout()
        optionHBox3 = QHBoxLayout()
        optionHBox4 = QHBoxLayout()
        optionHBox5 = QHBoxLayout()
        optionHBox6 = QHBoxLayout()
        optionHBox7 = QHBoxLayout()
        optionHBox8 = QHBoxLayout()
        optionHBox9 = QHBoxLayout()
        optionHBox10 = QHBoxLayout()
        optionHBox11 = QHBoxLayout()
        optionHBox12 = QHBoxLayout()
        optionHBox13 = QHBoxLayout()

        # Элементы
        label_Var = QLabel('Параметры системы')
        label_Var.setStyleSheet('font-size: 9pt;')

        label_a1 = QLabel()
        label_a1.setText('a<sub>1</sub>&#160;&#160;&#160;')
        label_a1.setToolTip('Положительная постоянная a<sub>1</sub>')
        self.a1 = QLineEdit()
        self.a1.setFixedHeight(25)
        self.a1.setText('5')
        box_a1 = QHBoxLayout()
        box_a1.addWidget(label_a1)
        box_a1.addWidget(self.a1)

        label_a3 = QLabel()
        label_a3.setText('a<sub>3</sub>&#160;&#160;&#160;')
        label_a3.setToolTip('Положительная постоянная a<sub>3</sub>')
        self.a3 = QLineEdit()
        self.a3.setFixedHeight(25)
        self.a3.setText('2')
        box_a3 = QHBoxLayout()
        box_a3.addWidget(label_a3)
        box_a3.addWidget(self.a3)

        label_m = QLabel('m <sub>&#160;</sub>&#160;')
        label_m.setToolTip('Масса точки')
        self.m = QLineEdit()
        self.m.setFixedHeight(25)
        self.m.setText('10')
        box_m = QHBoxLayout()
        box_m.addWidget(label_m)
        box_m.addWidget(self.m)

        label_startVar = QLabel('Начальные условия')
        label_startVar.setStyleSheet('font-size: 9pt;')

        label_x0 = QLabel()
        label_x0.setText('x<sub>0</sub>&#160;&#160;&#160;')
        label_x0.setToolTip('Начальное время')
        self.x0 = QLineEdit()
        self.x0.setFixedHeight(25)
        self.x0.setText('0')
        box_x0 = QHBoxLayout()
        box_x0.addWidget(label_x0)
        box_x0.addWidget(self.x0)

        label_u0 = QLabel()
        label_u0.setText('u<sub>0</sub>&#160;&#160;&#160;')
        label_u0.setToolTip('Начальное скорость точки')
        self.u0 = QLineEdit()
        self.u0.setFixedHeight(25)
        self.u0.setText('100')
        box_u0 = QHBoxLayout()
        box_u0.addWidget(label_u0)
        box_u0.addWidget(self.u0)

        label_VarM = QLabel('Параметры метода')
        label_VarM.setStyleSheet('font-size: 9pt;')

        label_h = QLabel('h &#160;&#160;<sub>&#160;</sub>')
        label_h.setToolTip('Начальный шаг')
        self.h = QLineEdit()
        self.h.setFixedHeight(25)
        self.h.setText('0.0001')
        box_h = QHBoxLayout()
        box_h.addWidget(label_h)
        box_h.addWidget(self.h)

        label_control = QLabel('Контроль')
        label_control.setStyleSheet('font-size: 9pt;')

        label_n = QLabel('n    &#160;&#160;<sub>&#160;</sub>')
        label_n.setToolTip('Счетчик шагов')
        self.n = QLineEdit()
        self.n.setFixedHeight(25)
        self.n.setText('10000')
        box_n = QHBoxLayout()
        box_n.addWidget(label_n)
        box_n.addWidget(self.n)

        label_b = QLabel('b    ')
        label_b.setToolTip('Нижняя граница для скорости')
        self.b = QLineEdit()
        self.b.setFixedHeight(25)
        self.b.setText('0')
        box_b = QHBoxLayout()
        box_b.addWidget(label_b)
        box_b.addWidget(self.b)

        label_Egr = QLabel()
        label_Egr.setText('E<sub>гр</sub>  &#160;')
        label_Egr.setToolTip('Параметр контроля выхода на нижнюю границу для скорости')
        self.Egr = QLineEdit()
        self.Egr.setFixedHeight(25)
        self.Egr.setText('0.000005')
        box_Egr = QHBoxLayout()
        box_Egr.addWidget(label_Egr)
        box_Egr.addWidget(self.Egr)

        label_E = QLabel()
        label_E.setText('E    ')
        label_E.setToolTip('Параметр контроля локальной погрешности "сверху"')
        self.E = QLineEdit()
        self.E.setFixedHeight(25)
        self.E.setText('0.000005')
        box_E = QHBoxLayout()
        box_E.addWidget(label_E)
        box_E.addWidget(self.E)

        label_Emin = QLabel()
        label_Emin.setText('E<sub>min</sub>')
        label_Emin.setToolTip('Параметр контроля локальной погрешности "снизу"')
        self.Emin = QLineEdit()
        tmp = float(self.E.text()) / 2 ** (self.p + 1)
        self.Emin.setFixedHeight(25)
        self.Emin.setText(float_to_str(tmp))
        del tmp
        box_Emin = QHBoxLayout()
        box_Emin.addWidget(label_Emin)
        box_Emin.addWidget(self.Emin)

        self.combobox = QComboBox()
        self.combobox.setFixedHeight(25)
        self.combobox.addItem('Контроль погрешности "сверху" и "снизу"')
        self.combobox.addItem('Отказ от контроля погрешности "снизу"')
        self.combobox.addItem('Отказ от контроля погрешности "снизу и сверху"')

        self.comboboxV = QComboBox()
        self.comboboxV.setFixedHeight(25)
        self.comboboxV.addItem('В качестве Vn итог берем Vn')
        self.comboboxV.addItem('В качестве Vn итог берем Vn удв')
        self.comboboxV.addItem('В качестве Vn итог берем Vn кор')

        # Заполняем все горизонтальные блоки
        optionHBox1.addLayout(box_a1)
        optionHBox2.addLayout(box_a3)
        optionHBox3.addLayout(box_m)
        optionHBox4.addLayout(box_x0)
        optionHBox5.addLayout(box_u0)
        optionHBox6.addLayout(box_h)
        optionHBox7.addLayout(box_n)
        optionHBox8.addLayout(box_b)
        optionHBox9.addLayout(box_Egr)
        optionHBox10.addLayout(box_E)
        optionHBox11.addLayout(box_Emin)
        optionHBox12.addWidget(self.combobox)
        optionHBox13.addWidget(self.comboboxV)

        # Заполняем все вертикальные блоки
        optionVBox.addWidget(label_Var)
        optionVBox.addLayout(optionHBox1)
        optionVBox.addLayout(optionHBox2)
        optionVBox.addLayout(optionHBox3)
        optionVBox.addWidget(label_startVar)
        optionVBox.addLayout(optionHBox4)
        optionVBox.addLayout(optionHBox5)
        optionVBox.addWidget(label_VarM)
        optionVBox.addLayout(optionHBox6)
        optionVBox.addWidget(label_control)
        optionVBox.addLayout(optionHBox7)
        optionVBox.addLayout(optionHBox8)
        optionVBox.addLayout(optionHBox9)
        optionVBox.addLayout(optionHBox10)
        optionVBox.addLayout(optionHBox11)
        optionVBox.addLayout(optionHBox12)
        optionVBox.addLayout(optionHBox13)

        option.setLayout(optionVBox)

        """--------------------------------------------Блок со справкой----------------------------------------------"""
        reference = QWidget(main)
        referenceVBox = QVBoxLayout()

        label_at = QLabel('Справка')
        label_at.setAlignment(Qt.AlignCenter)
        self.textarea = QPlainTextEdit()
        self.textarea.setFixedSize(600, 530)
        self.textarea.setFrameStyle(QFrame.NoFrame)
        self.textarea.setReadOnly(True)

        referenceVBox.addWidget(label_at)
        referenceVBox.addWidget(self.textarea)
        reference.setLayout(referenceVBox)

        """---------------------------------------------Блок с таблицей----------------------------------------------"""
        self.table = QTableWidget(main)
        self.table.setColumnCount(9)
        self.table.setRowCount(15)
        # self.table.setFixedSize(594, 400)
        self.table.verticalHeader().setVisible(False)
        self.table.setFixedSize(900, 400)

        self.table.setFrameStyle(QFrame.NoFrame)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        header = ['N', 'Hn-1', 'Xn',
                  'Vn', 'Vn удв',
                  'S*', 'Vn итог',
                  'Ум.шага', 'Ув.шага']

        self.table.setHorizontalHeaderLabels(header)
        for i in range(9):
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
            if i in [0, 7, 8]:
                self.table.setColumnWidth(i, 5 * 9)
            elif i == 1:
                self.table.setColumnWidth(i, 10 * 9)
            else:
                self.table.setColumnWidth(i, 15 * 9)

        # Всплывающие подсказки на хедер таблицы
        hints = ['Номер шага метода', 'Шаг численного интегрирования', 'n-ое время', 'Скорость точки в момент времени xn',
                 'Скорость точки в момент времени xn (Удвоенный шаг)', 'Оценка ЛП',
                 'Скорость точки в момент времени xn (итоговое значение)',
                 'Кол-во уменьшений шага', 'Кол-во увеличений шага']
        for i, hint in enumerate(hints):
            self.table.horizontalHeaderItem(i).setToolTip(hint)

        """---------------------------------------------Блок с графиком----------------------------------------------"""

        class mlpCanvas(FigureCanvas):
            """
            Чтобы нарисовать новый график, нужно объект.plot(list, list)
            """

            def __init__(self, width=5, height=4, dpi=100):
                # Задаем размеры
                fig = Figure(figsize=(width, height), dpi=dpi)
                FigureCanvas.__init__(self, fig)
                self.ax = self.figure.add_subplot(111)
                self.ax.set_title('Зависимость скорости от времени')
                self.ax.set_xlabel('Время')
                self.ax.set_ylabel('Скорость')
                FigureCanvas.updateGeometry(self)

            def plot(self, x: list, y: list):
                self.ax.plot(x, y)
                self.draw_idle()

        self.canvas = mlpCanvas()

        mainHBox1.addWidget(option)
        mainHBox1.addWidget(reference)

        mainHBox2.addWidget(self.table)
        mainHBox2.addWidget(self.canvas)

        mainVBox.addLayout(mainHBox1)
        mainVBox.addLayout(mainHBox2)

        main.setLayout(mainVBox)

        self.window.setCentralWidget(main)

    def condition(self):
        """
        Открытие условия задачи
        """

        message = '<p><b>Вариант 4</b></p>' \
                  '<p>Свободный (горизонтальный) полет точки массы <b>m</b> под действием превоначального толчка ' \
                  'силы сопротивления среды <b>R</b> описывается уравнением</p>' \
                  '<p><b>m * du/dx = R, u(0) = u<sub>0</sub></b></p>' \
                  '<p>где <b>R = -(a<sub>1</sub> * u + a<sub>3</sub> * u<sup>3</sup>)</b>, где ' \
                  '<b>a<sub>1</sub>, a<sub>3</sub></b> - положительные постоянные, <b>u<sub>0</sub></b> - начальная ' \
                  'скорость точки, <b>u(x)</b> - скорость в момент времени <b>x</b>. Численно решая задачу Коши, ' \
                  'установите общие закономерности зависимости скорости от времени. ' \
                  'Параметры системы: <b>a<sub>1</sub>, a<sub>3</sub></b>. </p>'

        self.dialog_message.setWindowTitle('Условие задачи')
        self.dialog_message.setWindowIcon(QIcon('options\\favicon.ico'))
        self.dialog_message.setText(message)
        self.dialog_message.exec()

    def rungeKutta_method(self):
        """
        Открытие справки о методе
        :return:
        """

        message = '<p><b>Метод Рунге-Кутта явный 3-ого порядка, p = 3</b></p>' \
                  '' \
                  '<p>x<sub>0</sub>, v<sub>0</sub> = u<sub>0</sub>,</p>' \
                  '' \
                  '<p>x<sub>n+1</sub> = x<sub>n</sub> + h<sub>n</sub>,</p>' \
                  '' \
                  '<p>v<sub>n+1</sub> = v<sub>n</sub> + h<sub>n</sub>/6 * ' \
                  '(k<sub>1</sub> + 4k<sub>2</sub> + k<sub>5</sub>),</p>' \
                  '' \
                  '<p>k<sub>1</sub> = f(x<sub>n</sub>, v<sub>n</sub>),</p>' \
                  '' \
                  '<p>k<sub>2</sub> = f(x<sub>n</sub> + h<sub>n</sub>/2, ' \
                  'v<sub>n</sub> + h<sub>n</sub>/2 * k<sub>1</sub>),</p>' \
                  '' \
                  '<p>k<sub>3</sub> = f(x<sub>n</sub> + h<sub>n</sub>, ' \
                  'v<sub>n</sub> + h<sub>n</sub>(-k<sub>1</sub> + 2k<sub>2</sub>)).</p>'

        self.dialog_message.setWindowTitle('Метод')
        self.dialog_message.setWindowIcon(QIcon('options\\favicon.ico'))
        self.dialog_message.setText(message)
        self.dialog_message.exec()

    def error_input(self, message):
        """
        Сообщение об ошибке в модальном окне
        """

        self.dialog_message.setWindowTitle('Ошибка')
        self.dialog_message.setWindowIcon(QIcon('options\\favicon.ico'))
        self.dialog_message.setText(message)
        self.dialog_message.exec()

    def data_to_table(self, data: dict):
        """
        Записываем полученные данные в таблицу
        :param data: словарь с информацией
        """

        def create_item(row: int, col: int, text: str):
            item = QTableWidgetItem(str(text))
            item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, col, item)

        self.table.setRowCount(len(data['n']))

        for i, n in enumerate(data['n']):
            create_item(i, 0, n)
            create_item(i, 1, data['hn-1'][i])
            create_item(i, 2, data['xn'][i])
            create_item(i, 3, data['vn'][i])
            create_item(i, 4, data['vn_ud'][i])
            create_item(i, 5, data['S*'][i])
            create_item(i, 6, data['vn_res'][i])
            create_item(i, 7, data['step_decrease'][i])
            create_item(i, 8, data['step_increase'][i])

    def except_errors(self) -> bool:
        """
        Отлавливаем все возможные ошибки
        :return: True - есть ошибка, False - нет ошибок
        """

        error = False
        try:
            if float(self.a1.text()) <= 0:
                error = True
                self.error_input('Значение параметра a1 должно быть положительным')
            if float(self.a3.text()) <= 0:
                error = True
                self.error_input('Значение параметра a3 должно быть положительным')
            if float(self.m.text()) <= 0:
                error = True
                self.error_input('Значение параметра m должно быть положительным')
            if float(self.h.text()) <= 0:
                error = True
                self.error_input('Шаг должен быть положительным')

            try:
                if int(self.n.text()) <= 0:
                    error = True
                    self.error_input('Кол-во шагов должно быть положительным')
            except ValueError:
                error = True
                self.error_input('Кол-во шагов должно быть целым')

            if float(self.Egr.text()) < 0:
                error = True
                self.error_input('Контроль выхода за нижнюю границу для скорости должен быть неотрицательным')
            if float(self.E.text()) <= 0:
                error = True
                self.error_input('Контроль ЛП "сверху" должен быть неотрицательным')
            if float(self.Emin.text()) <= 0:
                error = True
                self.error_input('Контроль ЛП "снизу" должен быть неотрицательным')
            if float(self.Emin.text()) > float(self.E.text()):
                error = True
                self.error_input('Контроль ЛП "сверху" должен быть не меньше контроля ЛП "снизу"')
        except ValueError:  # Если нельзя перевести строку в float или int
            error = True
            self.error_input('Входные данные должны быть числами с плавающей запятой кроме n, оно должны быть целым')

        return error

    def work(self):
        error = self.except_errors()

        data = {'x0': Decimal(self.x0.text()),
                'u0': Decimal(self.u0.text()),
                'a1': Decimal(self.a1.text()),
                'a3': Decimal(self.a3.text()),
                'm': Decimal(self.m.text()),
                'h': Decimal(self.h.text()),
                'n': int(self.n.text()),
                'b': Decimal(self.b.text()),
                'Egr': Decimal(self.Egr.text()),
                'E': Decimal(self.E.text()),
                'Emin': Decimal(self.Emin.text()),
                'cb': int(self.combobox.currentIndex()),
                'cbV': int(self.comboboxV.currentIndex()),
                'p': self.p}

        if not error:
            analysis = Analysis(data)
            del data
            data = analysis.work()

            # Запишем справку
            self.textarea.appendHtml(data['message'])

            # Запишем данные в таблицу
            self.data_to_table(data)

            # Построим график
            self.canvas.plot(data['xn'], data['vn_res'])
