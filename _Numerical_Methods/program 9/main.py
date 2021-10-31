"""
                                                             ____
     ____   _____ ____   ____ _ _____ ____ _ ____ ___      / __ \
   / __ \ / ___// __ \ / __ `// ___// __ `// __ `__ \    / /_/ /
  / /_/ // /   / /_/ // /_/ // /   / /_/ // / / / / /    \__, /
 / .___//_/    \____/ \__, //_/    \__,_//_/ /_/ /_/   /____/
/_/                  /____/


@author: Vladislav Kishkin
"""

# Сторонние библиотеки
import os
import sys
from PyQt5.QtWidgets import QApplication

# Мои модули
from interface import Window


def _cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_dir(name) -> str:
    """
    :param name: название директории
    :return: путь до созданной директории
    """

    from config import path_to_dir

    # Если нет папки, куда будут складироваться файлы для программы
    arr = os.listdir(path='.')
    path = '{}\\{}'.format(path_to_dir, name)
    if name not in arr:
        os.mkdir(path)

    return path


def main():
    _cls()
    path_to_options = check_dir('options')

    app = QApplication([])
    window = Window(path_to_options)

    # Ожидание событий и последующий выход из приложения
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
