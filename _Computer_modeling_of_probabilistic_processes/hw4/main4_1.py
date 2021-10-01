import numpy as np

np.random.seed(20)
sh = (1, 0)  #
n = 10000    # число эксперементов
k = 2        # число попаданий
p1 = 0.6     # вероятность попадания 1ого
p2 = 0.7     # 2ого
p3 = 0.8     # 3ого

q1 = 1 - p1  # вероятность непопадания 1ого
q2 = 1 - p2  # 2ого
q3 = 1 - p3  # 3ого

m = 0

for i in range(n):
    r1 = np.random.choice(sh, p=[p1, 1 - p1])
    r2 = np.random.choice(sh, p=[p2, 1 - p2])
    r3 = np.random.choice(sh, p=[p3, 1 - p3])

    r = r1 + r2 + r3
    if r == k:
        m += 1

    print(f'r1: {r1}; r2: {r2}, r3: {r3} => r: {r}')

p = m / n
print(f'Попадания: {k}; вероятность: {round(p, 3)}; n: {n}')
print(f'Теоритическая вероятность: {round(p1 * p2 * q3 + p1 * q2 * p3 + q1 * p2 * p3, 3)}')
