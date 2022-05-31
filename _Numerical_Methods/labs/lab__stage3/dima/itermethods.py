# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np
import matplotlib.pyplot as plt
import iterMethods as imet
from prettytable import PrettyTable

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import sys



#параметры задачи
N = 100
M = 100
w = 1.98 #для МВР
w2 = 1.98 #для МВР
n_max = 10**7
eps = 10**-8
test = False #тестовая или основная


#построение сетки из массивов координат
xs = np.linspace(-1, 1, N+1)
ys = np.linspace(-1, 1, M+1)
xgrid, ygrid = np.meshgrid(xs, ys) #для рисовалки


#получение решения задачи
if test == True:
    v = np.asarray(imet.min_discrepancies_test(N, M, xs, ys, n_max, eps))
    n = v[M+1][:-N+2]
    v = v[:-1]
    
    #подсчет ε1
    u = np.zeros((M+1)*(N+1)).reshape(M+1, N+1)
    f = lambda x, y: np.exp(1-x**2-y**2)
    for j in range(M+1):
        for i in range(N+1):
            u[j][i] = f(xs[i], ys[j])

    eps1 = -1.0
    xm = -5.0
    ym = -5.0
    for j in range(M+1):
        for i in range(N+1):
            tmp = abs(v[j][i]-u[j][i])
            if tmp > eps1:
                eps1 = tmp
                xm = xs[i]
                ym = ys[j]
    
    #выведем справку для тестовой задачи
    print(f'\nДля решения тестовой задачи использованы сетка с числом разбиений по x: n = {N} и числом разбиений по y: m = {M}.\n\
Использован метод минимальных невязок,\n\
применены критерии остановки по точности ε(метода) = {eps} и по числу итераций Nmax = {n_max}.\n\
\n\
На решение схемы (СЛАУ) затрачено итераций N = {int(n[0])} и достигнута точность итерационного метода ε(N) = {n[1]}.\n\
Схема (СЛАУ) решена с невязкой ||R(N)|| = {n[2]}, для невязки СЛАУ использована норма «max».\n\
\n\
Тестовая задача решена с точностью ε1 = {eps1}.\n\
Максимальное отклонение численных решений на основной сетке и сетке с половинным шагом наблюдается\n\
в узле x = {xm:.4f}; y = {ym:.4f}.\n\
В качестве начального приближения на основной сетке использовано нулевое приближение.\n')
    
    #выведем основные данные в таблицу
    table = PrettyTable()

    table.field_names = ['\\', 'n', 'm', 'Итер.', 'ε(N)', '||R(N)||', 'ε1']
    table.add_row(['Численное решение', f'{N}', f'{M}', f'{int(n[0])}', f'{n[1]:.14f}', f'{n[2]:.10f}', f'{eps1:.10f}'])
    table.add_row(['Истинное решение', f'{N}', f'{M}', '-', '-', '-',\
                   f'(x, y) = ({xm:.4f}, {ym:.4f})'])
    print(table, '\n')

else:
    xs2 = np.linspace(-1, 1, N*2+1)
    ys2 = np.linspace(-1, 1, M*2+1)
    
    v = np.asarray(imet.min_discrepancies(N, M, xs, ys, n_max, eps))
    v2 = np.asarray(imet.min_discrepancies(N*2, M*2, xs2, ys2, n_max, eps))
    n = v[M+1][:-N+2]
    n2 = v2[M*2+1][:-N*2+2]
    v = v[:-1]
    v2 = v2[:-1]
    
    #подсчет ε2
    eps2 = -1.0
    xm = -5.0
    ym = -5.0
    for j in range(M+1):
        for i in range(N+1):
            tmp = abs(v[j][i]-v2[2*j][2*i])
            if tmp > eps2:
                eps2 = tmp
                xm = xs[i]
                ym = ys[j]
    
    #выведем справку для основной задачи
    print(f'\nДля решения основной задачи использованы сетка с числом разбиений по x: n = {N} и числом разбиений по y: m = {M}.\n\
Использован метод минимальных невязок,\n\
применены критерии остановки по точности ε(метода) = {eps} и по числу итераций Nmax = {n_max}.\n\
\n\
На решение схемы (СЛАУ) затрачено итераций N = {int(n[0])} и достигнута точность итерационного метода ε(N) = {n[1]}.\n\
Схема (СЛАУ) решена с невязкой ||R(N)|| = {n[2]}, для невязки СЛАУ использована норма «max»;\n\
\n\
Для контроля точности решения использована сетка с половинным шагом,\n\
Использован метод минимальных невязок, применены критерии остановки\n\
по точности ε(метода)2 = {eps} и по числу итераций Nmax2 = {n_max}.\n\
\n\
На решение задачи (СЛАУ) затрачено итераций N2 = {int(n2[0])} и достигнута точность итерационного метода ε(N2) = {n2[1]}.\n\
Схема (СЛАУ) на сетке с половинным шагом решена с невязкой ||R(N2)|| = {n2[2]}, использована норма «max».\n\
\n\
Основная задача решена с точностью ε2 = {eps2}.\n\
Максимальное отклонение численных решений на основной сетке и сетке с половинным шагом наблюдается\n\
в узле x = {xm:.4f}; y = {ym:.4f}.\n\
В качестве начального приближения на основной сетке использовано нулевое приближение,\n\
на сетке с половинным шагом использовано нулевое приближение.\n')
    
    #выведем основные данные в таблицу
    table = PrettyTable()

    table.field_names = ['\\', 'n', 'm', 'Итер.', 'ε(N)', '||R(N)||', 'ε2']
    table.add_row(['Большой шаг', f'{N}', f'{M}', f'{int(n[0])}', f'{n[1]:.14f}', f'{n[2]:.10f}', f'{eps2:.10f}'])
    table.add_row(['Половинный шаг', f'{N*2}', f'{M*2}', f'{int(n2[0])}', f'{n2[1]:.14f}', f'{n2[2]:.10f}',\
                   f'(x, y) = ({xm:.4f}, {ym:.4f})'])
    print(table, '\n')
    
 
#настройка фигуры
fig = plt.figure(figsize = (10, 10))
fig.suptitle('Искомая поверхность v(x, y)', fontsize=14)
ax = fig.add_subplot(1, 1, 1, projection='3d')


#нарисуем поверхность v(x,y)
ax.plot_surface(xgrid, ygrid, v, rcount = 100, ccount = 100, cmap = 'plasma')
plt.show()


#вывод таблицы значений
class Window(object):
    def setupUi(self, MainWindow, test):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(700, 30, 1220, 1035)
        if test == True:
            MainWindow.setWindowTitle("Таблицы значений v(x,y) и u(x,y) и их невязки")
        else:
            MainWindow.setWindowTitle("Таблицы значений v(x,y) и v2(x,y) и их невязки")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        
        
        self.table1 = QtWidgets.QTableWidget(self.centralwidget)
        self.table1.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.table1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table1.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.table1.setShowGrid(True)
        self.table1.setObjectName("table1")
        
        self.data_to_table1()
        
        self.table2 = QtWidgets.QTableWidget(self.centralwidget)
        self.table2.setGeometry(QtCore.QRect(0, 510, 600, 500))
        self.table2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table2.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.table2.setShowGrid(True)
        self.table2.setObjectName("table2")
        
        if test == True:
            self.data_to_table2_test()
        else:
            self.data_to_table2_main()
        
        self.table3 = QtWidgets.QTableWidget(self.centralwidget)
        self.table3.setGeometry(QtCore.QRect(610, 250, 600, 500))
        self.table3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table3.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.table3.setShowGrid(True)
        self.table3.setObjectName("table3")
        
        if test == True:
            self.data_to_table3_test()
        else:
            self.data_to_table3_main()
        
    def data_to_table1(self):
        def create_item(row: int, col: int, text: str):
            item = QtWidgets.QTableWidgetItem(str(text))
            item.setFlags(Qt.ItemIsEnabled)
            self.table1.setItem(row, col, item)

        self.table1.setRowCount(N+1)
        self.table1.setColumnCount(M+1)

        for i in range(N+1):
            header_item = QtWidgets.QTableWidgetItem(f'{i}, {xs[i]:.4f}')
            self.table1.setHorizontalHeaderItem(i, header_item)
            for j in range(M+1):
                header_item = QtWidgets.QTableWidgetItem(f'{M-j}, {ys[M-j]:.4f}')
                self.table1.setVerticalHeaderItem(j, header_item)
                create_item(j, i, str(f'{v[M-j][i]:.10f}'))
        
    def data_to_table2_main(self):
        def create_item(row: int, col: int, text: str):
            item = QtWidgets.QTableWidgetItem(str(text))
            item.setFlags(Qt.ItemIsEnabled)
            self.table2.setItem(row, col, item)

        self.table2.setRowCount(N+1)
        self.table2.setColumnCount(M+1)

        for i in range(N+1):
            header_item = QtWidgets.QTableWidgetItem(f'{i*2}, {xs[i]:.4f}')
            self.table2.setHorizontalHeaderItem(i, header_item)
            for j in range(M+1):
                header_item = QtWidgets.QTableWidgetItem(f'{(M-j)*2}, {ys[M-j]:.4f}')
                self.table2.setVerticalHeaderItem(j, header_item)
                create_item(j, i, str(f'{v2[(M-j)*2][i*2]:.10f}'))
    
    def data_to_table2_test(self):
        def create_item(row: int, col: int, text: str):
            item = QtWidgets.QTableWidgetItem(str(text))
            item.setFlags(Qt.ItemIsEnabled)
            self.table2.setItem(row, col, item)

        self.table2.setRowCount(N+1)
        self.table2.setColumnCount(M+1)

        for i in range(N+1):
            header_item = QtWidgets.QTableWidgetItem(f'{i}, {xs[i]:.4f}')
            self.table2.setHorizontalHeaderItem(i, header_item)
            for j in range(M+1):
                header_item = QtWidgets.QTableWidgetItem(f'{M-j}, {ys[M-j]:.4f}')
                self.table2.setVerticalHeaderItem(j, header_item)
                create_item(j, i, str(f'{u[M-j][i]:.10f}'))
    
    def data_to_table3_main(self):
        def create_item(row: int, col: int, text: str):
            item = QtWidgets.QTableWidgetItem(str(text))
            item.setFlags(Qt.ItemIsEnabled)
            self.table3.setItem(row, col, item)

        self.table3.setRowCount(N+1)
        self.table3.setColumnCount(M+1)

        for i in range(N+1):
            header_item = QtWidgets.QTableWidgetItem(f'{i*2}, {xs[i]:.4f}')
            self.table3.setHorizontalHeaderItem(i, header_item)
            for j in range(M+1):
                header_item = QtWidgets.QTableWidgetItem(f'{(M-j)*2}, {ys[M-j]:.4f}')
                self.table3.setVerticalHeaderItem(j, header_item)
                create_item(j, i, str(f'{v2[(M-j)*2][i*2]-v[M-j][i]:.10f}'))
                
    def data_to_table3_test(self):
        def create_item(row: int, col: int, text: str):
            item = QtWidgets.QTableWidgetItem(str(text))
            item.setFlags(Qt.ItemIsEnabled)
            self.table3.setItem(row, col, item)

        self.table3.setRowCount(N+1)
        self.table3.setColumnCount(M+1)

        for i in range(N+1):
            header_item = QtWidgets.QTableWidgetItem(f'{i}, {xs[i]:.4f}')
            self.table3.setHorizontalHeaderItem(i, header_item)
            for j in range(M+1):
                header_item = QtWidgets.QTableWidgetItem(f'{M-j}, {ys[M-j]:.4f}')
                self.table3.setVerticalHeaderItem(j, header_item)
                create_item(j, i, str(f'{u[M-j][i]-v[M-j][i]:.10f}'))


app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Window()
ui.setupUi(MainWindow, test)
MainWindow.show()

app.setQuitOnLastWindowClosed(True)
sys.exit(app.exec_())    









