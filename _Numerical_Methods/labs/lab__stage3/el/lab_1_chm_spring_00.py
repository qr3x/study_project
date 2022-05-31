from array import *
import enum
import math
from numpy import arange
from pylab import plot,xlabel,ylabel,show
from prettytable import PrettyTable
import numpy as np
import pandas as pd
from sympy import *

#U*(x,y)
def utest(x, y):
 return (np.exp(1-x**2-y**2))

#f(x,y)
def funct(x, y):
 return (np.abs((np.sin(np.pi*x*y))**3))

#f*(x,y)
def f_star(x,y):
 return (4*(utest(x,y))*(x*x+y*y-1))



#Граничные условия для основной задачи
#-----------------------------------------------------
# mu1(y) и mu2(y), в нашем случае они равны
def mu1_2(x, y):
 return (1-y*y) # mu1_2(y) = 1 - y^2

## mu3(x) и mu4(x), в нашем случае они равны 
def mu3_4(x, y):
 return (abs(np.sin(np.pi*x))) # mu3_4(x)=|sin(pi*x)|
#------------------------------------------------------

def lambda_1(h, k, n, m):
	return (4.0 / (h * h)) * np.sin(np.pi /(2 * n))*np.sin(np.pi/(2 * n)) + (4.0 /(k * k)) * np.sin(np.pi / (2*m))* np.sin(np.pi/(2 * m))


def lambda_n(h, k, n, m):
	#return (4.0 /(h * h)) * np.sin(np.pi*(n - 1) / (2 * n))* np.sin(np.pi * (n - 1) /(2 * n)) + (4.0 / (k * k)) * np.sin(np.pi * (m - 1) /(2 * m))* np.sin(np.pi * (m - 1) / (2 * m))
    return (4.0 /(h * h)) * np.cos((np.pi)/ (2*n))*np.cos((np.pi)/(2*n)) + (4.0 / (k*k)) * np.cos((np.pi)/(2*m))*np.cos((np.pi)/(2*m))

def tau(S, k_chebyshev, h, k, n, m):
	s = S % k_chebyshev
	return 2.0 / ((lambda_1(h, k, n, m) + lambda_n(h, k, n, m)) + ((lambda_n(h, k, n, m) - lambda_1(h, k, n, m)) * np.cos((np.pi * (2 * s - 1)) / (2 * k_chebyshev))))
	
def tau_MPI(h, k, n, m):
    return 2. / (lambda_1(h, k, n, m) + lambda_n(h, k, n, m))


print("\n")
print("Применение итерационного метода верхней релаксации для решения разностных схем на примере задачи Дирихле для уравнения Пуассона")
print("\n")
print("u=exp(1-x^2-y^2). Границы: a=-1, b=1, c=-1, d=1")
print("Pазмер таблицы")
m = int (input("m = "))
n = int (input("n = "))
Nmax = int(input("Mаксимальное число шагов= "))
epsilon=float(input("Точность метода = "))
Task = int (input("Выберите тестовую (1) или основную (2) задачу: "))
print("Chose the method:")
print("1) Метод верхней релаксации  \n2) Метод Чебышева \n3) Метод простой итерации ")
Pick_Method = int (input("Method: "))
data=PrettyTable()
result_test=PrettyTable()
result_test.field_names=["Число шагов, затраченных на решение", "Достигнутая точность метода","Общая погрешность решения", "Норма невязки(евклидова)", "Норма общей погрешности", "Максимальное отклонение в узле [x,y]:"]
result_main=PrettyTable()
result_main.field_names=["Число шагов, затраченных на решение", "Достигнутая точность метода для V","Достигнутая точность метода для V_2", "Невязка", "Максимальная разность двух приближений","Максимальное отклонение в узле [x,y]:"]


def solve_test(n, m, Nmax, epsilon):
    #Here we will set the parameters
    S = 0  #number of iterations
    V = []
    U = []
    R = [] #Невязка
    Z = [] #Общая погрешность
    eps_max = 0.0
    eps_cur = 0.0
    a = -1.0
    b = 1.0
    c = -1.0
    d = 1.0
    h = (b - a) / n
    k = (d - c) / m
    h2 = 1 / (h*h)
    k2 = 1 / (k*k)
    A = -2*(h2 + k2)
    v_old = 0
    v_new = 0
    ind_x=0
    ind_y=0
    flag = 0

    #Here we will print the first table
    if Pick_Method == 1:
        #l = 2 * (math.asin(math.pi / (2 * n))) ** 2
        #w= 2 / (1 + (l * (2 - l)) ** (1 / 2))
        w=float(input("Введите фактор релаксации в интервале (0,2) = " ))
        data.field_names=["Число разбиений по х", "Число разбиений по у","Максимальное число шагов","Точность метода","Начальное приближение","Параметр ω"]
        data.add_row([n,m,Nmax,epsilon,"нулевое",w])
    if Pick_Method == 2 or Pick_Method == 3:
        data.field_names=["Число разбиений по х", "Число разбиений по у","Максимальное число шагов","Точность метода","Начальное приближение"]
        data.add_row([n,m,Nmax,epsilon,"нулевое"])
    print(data)


    


    #Создание и заполнение матрицы U нулями и затем значениями   
    for p in range(0, m+1):
        U.append([])
        for z in range(0, n+1):
            U[p].append(0)
    
    for i in range(0, m+1):
        for j in range(0, n+1):    
            U[i][j] = utest(a + j * h, c + i * k)
    

    #Создание и заполнение матрицы V нулями
    for p in range(0, m+1):
        V.append([])
        for z in range(0, n+1):
            V[p].append(0)

    #Пользуясь имеющимися граничными условиями, заполняем матрицу V значениями
    for p in range(0, n + 1):
        V[0][p] = utest(a, c+p*k)
    for p in range(0, n + 1):
        V[m][p] = utest(b, c + p * k)
    for r in range(0, m + 1):
        V[r][0] = utest(a + r * h, c)
    for r in range(0, m + 1):
        V[r][n] = utest(a + r * h, d)


    #Создание и заполнение матрицы R(невязок) нулями
    for p in range(0, m+1):
        R.append([])
        for z in range(0, n+1):
            R[p].append(0)

    #Создание и заполнение матрицы Z(Общая погрешность) нулями
    print("\n")
    for p in range(0, m+1):
        Z.append([])
        for z in range(0, n+1):
            Z[p].append(0)

    
    #Реализация методов для тестовой задачи
    while (flag == 0):
        eps_max = 0 
        if(S==1 or S==2): 
            print("Значения на ", S, " итерации:")
            print("\n")
            tab_ = pd.DataFrame(V)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.float_format', '{:.11f}'.format)
            pd.options.display.expand_frame_repr = False
            print(tab_)
            print("\n")
        
        for i in range (1,m):
          for j in range (1,n):
                R[i][j] = A * V[i][j] + (h2 * (V[i][j + 1] + V[i][j - 1]) + k2 * (V[i + 1][j] + V[i - 1][j])) - f_star(a + h*j, c + k*i)
        
        
        for i in range(1, m):
            for j in range(1, n):
                v_old = V[i][j]
                if Pick_Method == 1: #МВР
                    v_new = -w*(h2*(V[i + 1][j] + V[i - 1][j]) + k2 * (V[i][j + 1] + V[i][j - 1])) 
                    v_new = v_new + (1-w)*A*V[i][j] + w*f_star(a + h*j, c + k*i) 
                    v_new = v_new / A

                if Pick_Method == 2: #Чебышев
                     v_new = v_old + tau(S,7,h,k,n,m)*R[i][j]
					
                    
                if Pick_Method == 3: #МПИ
                    v_new=v_old + tau_MPI(h,k,n,m)*R[i][j]

                eps_cur = abs(v_old - v_new) 
                if(eps_cur > eps_max):
                    eps_max = eps_cur #eps_max - достигнутая точность метода
                V[i][j] = v_new 
        S = S + 1 
        if(eps_max < epsilon or S >= Nmax):
            flag = 1

    print("\n") 
    print("Значение на ",S," итерации")
    

    # Вывод
    tab = pd.DataFrame(V)
    tab.to_csv("Table_Lab_1.csv", index=False)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.float_format', '{:.11f}'.format)
    pd.options.display.expand_frame_repr = False
    print(tab)
    print("\n")

    maxeps = 0
    cureps = 0
    res=0

    for i in range(0, m+1):
        for j in range(0, n+1):
            Z[i][j]=V[i][j]-U[i][j]
    for i in range(0,m+1):
        for j in range(0,n+1):
            res=res+Z[i][j]*Z[i][j]
                
    Z_inf = math.sqrt(res) #норма общей погрешности

    #общая погрешность решения
    for i in range(0, m + 1):
        for j in range(0, n + 1):
            U[i][j] = utest(a + j * h, c + i * k)
            cureps = abs(U[i][j] - V[i][j])
            if(cureps >= maxeps):
                maxeps = cureps
               
    Difmax = 0
    for i in range(0, m+1):
        for j in range (0, n+1):
            Dif1 = abs(U[i][j] - V[i][j])
            if (Dif1 > Difmax):
                Difmax = Dif1
                ind_x = j
                ind_y = i

    max_x = a + ind_x*h
    max_y = c + ind_y*k
    punto = []
    punto.append(max_x)
    punto.append(max_y)
    
    #Невязка, погрешность метода
    nev = 0
    for i in range(0,m+1):
        for j in range(0,n+1):
            nev = nev+R[i][j]*R[i][j]
    nev=math.sqrt(nev) #норма невязки(евклидова)

    result_test.add_row([S,eps_max,maxeps,nev,Z_inf,punto])
    return result_test

def solver(n, m, Nmax, epsilon):
    #Here we will set the parameters
    S = 0  #number if iterations
    V = [] #создаем матрицу для обычной сетки
    V_2=[] #создаем матрицу для удвоенной сетки
    R = [] #Невязка
    R_2 = []
    eps_max = 0.0
    eps_cur = 0.0
    a = -1.0
    b = 1.0
    c = -1.0
    d = 1.0
    h1 = (b - a) / (2*n) #шаг по x для удвоенной сетки
    k1 = (d - c) / (2*m) #шаг по y для удвоенной сетки
    h1_2 = 1/(h1*h1)
    k1_2 = 1/(k1*k1)
    h = (b - a) / n #шаг по x для обычной сетки
    k = (d - c) / m #шаг по y для обычной сетки
    h2 = 1 / (h*h)
    k2 = 1 / (k*k)
    A = -2*(h2 + k2)
    A_2 = -2*(h1_2+k1_2)
    v_old = 0
    v_new = 0
    flag = 0

    #Here we will print the first table
    if Pick_Method == 1:
        #l = 2 * (math.asin(math.pi / (2 * n))) ** 2
        #w= 2 / (1 + (l * (2 - l)) ** (1 / 2))
        w=float(input("Введите фактор релаксации в интервале (0,2) = " ))
        data.field_names=["Число разбиений по х", "Число разбиений по у","Максимальное число шагов","Точность метода","Начальное приближение","Параметр ω"]
        data.add_row([n,m,Nmax,epsilon,"нулевое",w])
    if Pick_Method == 2 or Pick_Method == 3:
        data.field_names=["Число разбиений по х", "Число разбиений по у","Максимальное число шагов","Точность метода","Начальное приближение"]
        data.add_row([n,m,Nmax,epsilon,"нулевое"])
    print(data)

    #Создание и заполнение матрицы V нулями
    for p in range(0, m+1):
        V.append([])
        for i in range(0, n+1):
            V[p].append(0)
    


    #Пользуясь имеющимися граничными условиями, заполняем матрицу V значениями
    for p in range(0, n + 1):
        V[0][p] = mu1_2(a + p * h, c)
    for p in range(0, n + 1):
        V[m][p] = mu1_2(a + p * h, d)
    for r in range(0, m + 1):
        V[r][0] = mu3_4(a, c + r * k)
    for r in range(0, m + 1):
        V[r][n] = mu3_4(b, c + r * k)

    
    #Создание и заполнение матрицы V_2 нулями
    for p in range(0, 2*(m+1)):
        V_2.append([])
        for i in range(0, 2*(n+1)):
            V_2[p].append(0)

    
    #Пользуясь имеющимися граничными условиями, заполняем матрицу V_2 значениями
    for p in range(0, 2*(n + 1)):
        V_2[0][p] = mu1_2(a + p * h1, c)
    for p in range(0, 2*(n + 1)):
        V_2[m][p] = mu1_2(a + p * h1, d)
    for r in range(0, 2*(m + 1)):
        V_2[r][0] = mu3_4(a, c + r * k1)
    for r in range(0, 2*(m + 1)):
        V_2[r][n] = mu3_4(b, c + r * k1)


    #Создание и заполнение матрицы R(невязок) нулями
    for p in range(0, m+1):
        R.append([])
        for i in range(0, n+1):
            R[p].append(0)

    for p in range(0, 2*(m+1)):
        R_2.append([])
        for i in range(0, 2*(n+1)):
            R_2[p].append(0)

    #Реализация метода для обычной сетки
    while (flag == 0):
        eps_max = 0

        for i in range (1,m):
          for j in range (1,n):
                R[i][j] = A * V[i][j] + (h2 * (V[i][j + 1] + V[i][j - 1]) + k2 * (V[i + 1][j] + V[i - 1][j])) - funct(a + h*j, c + k*i)

        for i in range(1, m):
            for j in range(1, n):
                v_old = V[i][j]
                if Pick_Method == 1: #МВР
                    v_new = -w*(h2*(V[i + 1][j] + V[i - 1][j]) + k2 * (V[i][j + 1] + V[i][j - 1])) 
                    v_new = v_new + (1-w)*A*V[i][j] + w*funct(a + h*j, c + k*i)
                    v_new = v_new / A
                     
                if Pick_Method == 2: #Чебышев
                    v_new = v_old + tau(S,7,h,k,n,m)*R[i][j]
					
                    
                if Pick_Method == 3: #МПИ
                    v_new=v_old+tau_MPI(h,k,n,m)*R[i][j]

                eps_cur = abs(v_old - v_new) 

                if(eps_cur > eps_max):
                    eps_max = eps_cur
                V[i][j] = v_new 

        S = S + 1 
        if(eps_max < epsilon or S >= Nmax):
            flag = 1
    
    #Реализация метода для удвоенной сетки
    flag = 0
    while (flag == 0):
        eps_max2 = 0

        for i in range (1,m):
          for j in range (1,n):
                R_2[i][j] = A_2 * V_2[i][j] + (h1_2 * (V_2[i][j + 1] + V_2[i][j - 1]) + k1_2 * (V_2[i + 1][j] + V_2[i - 1][j])) - funct(a + h1*j, c + k1*i) 
        D=0
        for i in range(1, 2*m):
            for j in range(1, 2*n):
                v_old = V_2[i][j]
                if Pick_Method == 1: #МВР
                    v_new = -w*(h1_2*(V_2[i + 1][j] + V_2[i - 1][j]) + k1_2 * (V_2[i][j + 1] + V_2[i][j - 1])) 
                    v_new = v_new + (1-w)*A_2*V_2[i][j] + w*funct(a + h1*j, c + k1*i) 
                    v_new = v_new / A_2
                     
                if Pick_Method == 2: #Чебышев
                    v_new = v_old + tau(D,7,h1,k1,2*n,2*m)*R_2[i][j]					
                    
                if Pick_Method == 3: #МПИ
                    v_new=v_old+tau_MPI(h1,k1,2*n,2*m)*R_2[i][j]
                    
                eps_cur = abs(v_old - v_new) 
                if(eps_cur > eps_max2):
                    eps_max2 = eps_cur
                V_2[i][j] = v_new 
        D+=1
        
        if(eps_max2 < epsilon or S >= Nmax):
            flag = 1

    print("\n")       
    print("Значение на ",S," итерации")


    # Вывод
    tab = pd.DataFrame(V)
    tab.to_csv("Table_Lab_2.csv", index=False)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.float_format', '{:.11f}'.format)
    pd.options.display.expand_frame_repr = False
    print(tab)
    print("\n")

    #Max V-V_2
    Dif = 0
    for i in range(0, n+1):
        for j in range(0, m+1):
            if Dif < abs(V[i][j] - V_2[2*i][2*j]):
                Dif = abs(V[i][j] - V_2[2*i][2*j])
    
    Difmax = 0
    for i in range(0, m+1):
        for j in range (0, n+1):
            Dif1 = abs(V[i][j] - V_2[2*i][2*j])
            if (Dif1 > Difmax):
                Difmax = Dif1
                ind_x = j
                ind_y = i

    max_x = a + ind_x*h
    max_y = c + ind_y*k
    punto = []
    punto.append(max_x)
    punto.append(max_y)
    

    nev = 0
    for i in range(0,m+1):
        for j in range(0,n+1):
            nev = nev+R[i][j]*R[i][j]
    nev=math.sqrt(nev)
    result_main.add_row([S,eps_max, eps_max2,nev,Dif, punto])
    return result_main

if Task == 1: 
    solve_test(n, m, Nmax, epsilon)
    print("\n")
    print(result_test)
    print("\n")
else: 
    solver(n, m, Nmax, epsilon)
    print("\n")
    print(result_main)
    print("\n")