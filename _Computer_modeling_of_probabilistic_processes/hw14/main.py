import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


def main():
    n = (50, 100)

    for count_n in n:
        print()
        dist = st.norm.rvs(0, 1, count_n)
        print(f'Выборочное среднее: {np.mean(dist)}\n'
              f'Дисперсия: {np.var(dist)}\n'
              f'Ассинхронность: {st.skew(dist)}\n')

        """ ----------------------------------------------Гистограмма---------------------------------------------- """
        plt.title('Гистограмма отн.част.')

        plt.hist(dist, density=True)
        plt.show()

        """ -----------------------------------------------Диаграмма----------------------------------------------- """
        plt.title('Диаграмма рассеивания')
        plt.xlabel('смещение')
        plt.ylabel('Номер броска')
        x = np.arange(count_n)
        plt.plot(dist, x, 'go')
        plt.show()

        dist_gaus = [0]
        for i in x[1:]:
            dist_gaus.append(st.norm.rvs(dist_gaus[-1], 1))

        """ ------------------------------------------------Рисунок------------------------------------------------ """
        plt.plot(dist_gaus, x, 'o--')
        plt.xlabel('смещение')
        plt.ylabel('Номер броска')
        plt.show()

        plt.hist(dist_gaus, density=True)
        print(f'Выборочное среднее: {np.mean(dist_gaus)}\n'
              f'Дисперсия: {np.var(dist_gaus)}\n'
              f'Ассинхронность: {st.skew(dist_gaus)}\n')
        plt.show()


if __name__ == '__main__':
    # np.random.seed(100)
    main()
