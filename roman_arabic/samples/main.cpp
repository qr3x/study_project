#include <stdlib.h>  // Для cls
#include <conio.h>   // Для getch
#include "roman.h"

using namespace  std;

int menu()
{
    while (true)
    {
        cout << "Введите цифру:" << endl;
        cout << "0 - закончить работу" << endl;
        cout << "1 - римские числа в арабские" << endl;
        cout << "2 - арабские числа в римские" << endl;

        int num;
        cin >> num;

        system("cls");
        // Проверка попало ли число в наш диапазон
        if (num != 0 && num != 1 && num != 2)
        {
            cout << "Вы ввели число, которое не входит в диапазон от 0 до 2" << endl;
            continue;
        }

        return num;
    }
}

void romanToArabic()
{
    Convertor con;
    roman rom;
    arabic arab;

    cout << "Введите римское число: ";
    cin >> rom;

    system("cls");

    arab = con.toArabic(rom);
    cout << "Число в римских цифрах: " << rom << endl;
    cout << "Это число в арабских числах: " << arab << endl << endl;
}

void arabicToRoman()
{
    Convertor con;
    arabic arab; 
    roman rom;

    cout << "Введите арабское число: ";
    cin >> arab;

    system("cls");

    rom = con.toRoman(arab);
    cout << "Число в арабских цифрах: " << arab << endl;
    cout << "Это число в римских числах:  " << rom << endl << endl;
}

int main() {
    setlocale(LC_ALL, "Russian");

    cout << "Привет. Это конвертер римских чисел в арабские и наоборот" << endl;

    int num;
    while (true)
    {            
        num = menu();
        if (num == 0)
            break;
        else if (num == 1)
            romanToArabic();
        else if (num == 2)
            arabicToRoman();

        cout << "Нажмите любую клавишу, чтобы продолжить";
        getch();
        system("cls");
    }

    system("cls");
    cout << "Работа закончена" << endl;
    return 0;
}