# Сторонние библиотеки
# настройка окна
from PyQt5.QtWidgets import (QMainWindow, QAction, QStyleOptionHeader)

"""Инструкменты для макета"""
# диалоговые окна
from PyQt5.QtWidgets import QMessageBox, QInputDialog
# инструменты для шаблона
from PyQt5.QtWidgets import (QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QComboBox, QCheckBox,
                             QLineEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QPlainTextEdit,
                             QFrame)
# стилистика
from PyQt5.QtGui import (QIcon, QFont, QColor, QLinearGradient)
from PyQt5.QtCore import Qt

import decimal

# Графики
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


# Мои модули
from launcher import Analysis


def float_to_str(number: float):
    ctx = decimal.Context()
    ctx.prec = 20

    return format(ctx.create_decimal(repr(number)), 'f')


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
        self.window.setWindowTitle("Задача Коши для ОДУ")
        self.window.setWindowIcon(QIcon('options\\favicon.ico'))

        # Меню
        self.window.statusBar()
        menubar = self.window.menuBar()
        self.dialog_message = QMessageBox()
        self.dialog_input = QInputDialog()

        # Кнопка "Начать"
        self.workMenu = QAction('&Начать')
        self.workMenu.triggered.connect(self.work)

        # Кнопка "Условия задачи"
        self.instructionMenu = QAction('&Условия задачи')
        self.instructionMenu.triggered.connect(self.open_instruction_all)

        menubar.addAction(self.workMenu)
        menubar.addAction(self.instructionMenu)

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
        option.setStyleSheet('QLineEdit { border: none; }')
        option.setFixedSize(600, 400)
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

        # Элементы
        label_startVar = QLabel('Начальные условия')

        label_x0 = QLabel()
        label_x0.setText('x<sub>0</sub>')
        label_x0.setToolTip('Начальное время')
        self.x0 = QLineEdit()
        self.x0.setFixedHeight(25)
        self.x0.setText('0')
        # self.x0.setFixedSize(260, 20)
        box_x0 = QHBoxLayout()
        box_x0.addWidget(label_x0)
        box_x0.addWidget(self.x0)

        label_u0 = QLabel()
        label_u0.setText('u<sub>0</sub>')
        label_u0.setToolTip('Начальное скорость точки')
        self.u0 = QLineEdit()
        self.u0.setFixedHeight(25)
        self.u0.setText('0')
        box_u0 = QHBoxLayout()
        box_u0.addWidget(label_u0)
        box_u0.addWidget(self.u0)

        label_a1 = QLabel()
        label_a1.setText('a<sub>1</sub>')
        label_a1.setToolTip('Положительная постоянная a<sub>1</sub>')
        self.a1 = QLineEdit()
        self.a1.setFixedHeight(25)
        self.a1.setText('1')
        box_a1 = QHBoxLayout()
        box_a1.addWidget(label_a1)
        box_a1.addWidget(self.a1)

        label_a3 = QLabel()
        label_a3.setText('a<sub>3</sub>')
        label_a3.setToolTip('Положительная постоянная a<sub>3</sub>')
        self.a3 = QLineEdit()
        self.a3.setFixedHeight(25)
        self.a3.setText('1')
        box_a3 = QHBoxLayout()
        box_a3.addWidget(label_a3)
        box_a3.addWidget(self.a3)

        label_m = QLabel('m ')
        label_m.setToolTip('Масса точки')
        self.m = QLineEdit()
        self.m.setFixedHeight(25)
        self.m.setText('1')
        box_m = QHBoxLayout()
        box_m.addWidget(label_m)
        box_m.addWidget(self.m)

        label_h = QLabel('h <sub>&#160;</sub>')
        label_h.setToolTip('Шаг')
        self.h = QLineEdit()
        self.h.setFixedHeight(25)
        self.h.setText('0.01')
        box_h = QHBoxLayout()
        box_h.addWidget(label_h)
        box_h.addWidget(self.h)

        label_n = QLabel('n <sub>&#160;</sub>')
        label_n.setToolTip('Счетчик шагов')
        self.n = QLineEdit()
        self.n.setFixedHeight(25)
        self.n.setText('10000')
        box_n = QHBoxLayout()
        box_n.addWidget(label_n)
        box_n.addWidget(self.n)

        label_control = QLabel('Контроль ЛП')

        label_Egr = QLabel()
        label_Egr.setText('E<sub>гр</sub>  &#160;')
        label_Egr.setToolTip('Параметр контроля выхода на правую границу участка интегрирования')
        self.Egr = QLineEdit()
        self.Egr.setFixedHeight(25)
        self.Egr.setText('0.000005')
        box_Egr = QHBoxLayout()
        box_Egr.addWidget(label_Egr)
        box_Egr.addWidget(self.Egr)

        label_E = QLabel()
        label_E.setText('E    ')
        label_E.setToolTip('Параметр контроля локальной поверхности "сверху"')
        self.E = QLineEdit()
        self.E.setFixedHeight(25)
        self.E.setText('0.000005')
        box_E = QHBoxLayout()
        box_E.addWidget(label_E)
        box_E.addWidget(self.E)

        label_Emin = QLabel()
        label_Emin.setText('E<sub>min</sub>')
        label_Emin.setToolTip('Параметр контроля локальной поверхности "снизу"')
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

        # Заполняем все горизонтальные блоки
        optionHBox1.addLayout(box_x0)
        optionHBox2.addLayout(box_u0)
        optionHBox3.addLayout(box_a1)
        optionHBox4.addLayout(box_a3)
        optionHBox5.addLayout(box_m)
        optionHBox6.addLayout(box_h)
        optionHBox7.addLayout(box_n)
        optionHBox8.addLayout(box_Egr)
        optionHBox9.addLayout(box_E)
        optionHBox10.addLayout(box_Emin)
        optionHBox11.addWidget(self.combobox)

        # Заполняем все вертикальные блоки
        optionVBox.addWidget(label_startVar)
        optionVBox.addLayout(optionHBox1)
        optionVBox.addLayout(optionHBox2)
        optionVBox.addLayout(optionHBox3)
        optionVBox.addLayout(optionHBox4)
        optionVBox.addLayout(optionHBox5)
        optionVBox.addLayout(optionHBox6)
        optionVBox.addLayout(optionHBox7)
        optionVBox.addWidget(label_control)
        optionVBox.addLayout(optionHBox8)
        optionVBox.addLayout(optionHBox9)
        optionVBox.addLayout(optionHBox10)
        optionVBox.addLayout(optionHBox11)

        option.setLayout(optionVBox)

        """--------------------------------------------Блок со справкой----------------------------------------------"""
        reference = QWidget(main)
        referenceVBox = QVBoxLayout()

        label_at = QLabel('Справка')
        label_at.setAlignment(Qt.AlignCenter)
        self.textarea = QPlainTextEdit()
        self.textarea.setFixedSize(600, 376)
        self.textarea.setFrameStyle(QFrame.NoFrame)
        self.textarea.setReadOnly(True)

        referenceVBox.addWidget(label_at)
        referenceVBox.addWidget(self.textarea)
        reference.setLayout(referenceVBox)

        """---------------------------------------------Блок с таблицей----------------------------------------------"""
        self.table = QTableWidget(main)
        self.table.setColumnCount(9)
        self.table.setRowCount(15)
        self.table.setFixedSize(594, 400)
        self.table.verticalHeader().hide()
        self.table.setFrameStyle(QFrame.NoFrame)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        header = ['N', 'Hn-1', 'Xn',
                  'Vn', 'Vn удв',
                  'S*', 'Vn итог',
                  'Ум.шага', 'Ув.шага']

        self.table.setHorizontalHeaderLabels(header)
        for i in range(9):
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
            self.table.setColumnWidth(i, 66)

        """---------------------------------------------Блок с графиком----------------------------------------------"""

        class mlpCanvas(FigureCanvas):
            """
            Чтобы нарисовать новый график, нужно объект.plot(list)
            """

            def __init__(self, width=5, height=4, dpi=100):
                # Задаем размеры
                fig = Figure(figsize=(width, height), dpi=dpi)
                FigureCanvas.__init__(self, fig)
                self.ax = self.figure.add_subplot(111)
                FigureCanvas.updateGeometry(self)

            def plot(self, x: list, y: list):
                self.ax.plot(x, y)

        self.canvas = mlpCanvas()
        self.canvas.plot([1, 2, 3, 4, 5], [1, 5, 2, 7, 4])

        mainHBox1.addWidget(option)
        mainHBox1.addWidget(reference)

        mainHBox2.addWidget(self.table)
        mainHBox2.addWidget(self.canvas)

        mainVBox.addLayout(mainHBox1)
        mainVBox.addLayout(mainHBox2)

        main.setLayout(mainVBox)

        self.window.setCentralWidget(main)

    def open_instruction_all(self):
        """
        Открытие общей инструкции
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

        self.dialog_message.setWindowTitle('Инструкция: Общая инструкция')
        self.dialog_message.setWindowIcon(QIcon('options\\favicon.ico'))
        self.dialog_message.setText(message)
        self.dialog_message.exec()

    def work(self):
        if float(self.a1.text()) <= 0:
            self.textarea.appendPlainText('Значение параметра a1 должно быть положительным')
        if float(self.a3.text()) <= 0:
            self.textarea.appendPlainText('Значение параметра a3 должно быть положительным')
        if float(self.m.text()) <= 0:
            self.textarea.appendPlainText('Значение параметра m должно быть положительным')
        if float(self.h.text()) <= 0:
            self.textarea.appendPlainText('Шаг должен быть положительным')
        try:
            if int(self.n.text()) <= 0:
                self.textarea.appendPlainText('Кол-во шагов должно быть положительным')
        except ValueError:
            self.textarea.appendPlainText('Кол-во шагов должно быть целым')

        if float(self.Egr.text()) < 0:
            self.textarea.appendPlainText('Контроль выхода за правую границу дожлен быть неотрицательным')
        if float(self.E.text()) <= 0:
            self.textarea.appendPlainText('Контроль ЛП "сверху" должен быть неотрицательным')
        if float(self.Emin.text()) <= 0:
            self.textarea.appendPlainText('Контроль ЛП "снизу" должен быть неотрицательным')
        if float(self.Emin.text()) > float(self.E.text()):
            self.textarea.appendPlainText('Контроль ЛП "сверху" должен быть не меньше контроля ЛП "снизу"')

        data = {'x0': self.x0.text(),
                'u0': self.u0.text(),
                'a1': self.a1.text(),
                'a3': self.a3.text(),
                'm': self.m.text(),
                'h': self.h.text(),
                'n': self.n.text(),
                'Egr': self.Egr.text(),
                'E': self.E.text(),
                'Emin': self.Emin.text(),
                'cb': self.combobox.currentIndex()}

        analysis = Analysis(data)



