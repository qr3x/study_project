import numpy as np

p = 0.3
p1 = 0.1
p2 = 0.4
p3 = 1 - (p1 + p2)
k = 3

n = 20000
m = 0

for i in range(n):
    l1 = 0
    l2 = 0
    l3 = 0
    for j in range(k):
        rr = np.random.uniform(0., 1.)
        if rr <= p:
            l = np.random.uniform(0., 1.)
            if l <= p1:
                l1 += 1
            elif l <= p3:
                l2 += 1
            else:
                l3 += 1
    if l1 >= 1 or l2 >= 2 or l3 == 3:
        m += 1
    print(f'{l1} {l2} {l3} => m = {m}')

pp = round(m / n, 3)
print(f'Экспериментов: {n}')
print(f'Относ. частота: {pp}')

ph1 = 3 * p * (1 - p) ** 2
ph2 = 3 * p ** 2 * (1 - p)
ph3 = p ** 3

pah1 = p1
pah2 = p1 ** 2 + 2 * p1 * p2 + p2 ** 2 + 2 * p1 * p3
pah3 = 1 - 3 * p3 ** 2 * p2
print(f'Теорит.: {round(ph1 * pah1 + ph2 * pah2 + ph3 * pah3, 4)}')
