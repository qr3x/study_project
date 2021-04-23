#include <stdlib.h>  // Для cls
#include <conio.h>   // Для getch
#include "islands.h"


using namespace  std;


int main() {
    Matrix<int> mat(5);
    cout << mat;

 /*   setlocale(LC_ALL, "Russian");

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
    return 0;*/
}