#include <stdlib.h>  // ��� cls
#include <conio.h>   // ��� getch
#include "roman.h"

using namespace  std;

int menu()
{
    while (true)
    {
        cout << "������� �����:" << endl;
        cout << "0 - ��������� ������" << endl;
        cout << "1 - ������� ����� � ��������" << endl;
        cout << "2 - �������� ����� � �������" << endl;

        int num;
        cin >> num;

        system("cls");
        // �������� ������ �� ����� � ��� ��������
        if (num != 0 && num != 1 && num != 2)
        {
            cout << "�� ����� �����, ������� �� ������ � �������� �� 0 �� 2" << endl;
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

    cout << "��������� �����: I, V, X, L, C, D, M - �� ���� �� 1 �� 3999" << endl;
    cout << "������� ������� �����: ";
    cin >> rom;

    system("cls");

    arab = con.toArabic(rom);
    cout << "����� � ������� ������: " << rom << endl;
    cout << "��� ����� � �������� ������: " << arab << endl << endl;
}

void arabicToRoman()
{
    Convertor con;
    arabic arab; 
    roman rom;

    cout << "������� �������� �����: ";
    cin >> arab;

    system("cls");

    rom = con.toRoman(arab);
    cout << "����� � �������� ������: " << arab << endl;
    cout << "��� ����� � ������� ������:  " << rom << endl << endl;
}

int main() {
    setlocale(LC_ALL, "Russian");

    cout << "������. ��� ��������� ������� ����� � �������� � ��������" << endl;

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

        cout << "������� ����� �������, ����� ����������";
        getch();
        system("cls");
    }

    system("cls");
    cout << "������ ���������" << endl;
    return 0;
}