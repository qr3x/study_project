#ifndef INCLUDE_ROMAN_H_
#include <iostream>

#define INCLUDE_ROMAN_H_

using namespace std;


struct roman
{
    string value;

    // ������������
    roman() : value("") {};
    roman(char val)
    {
        this->value = val;
    }
    roman(string val) : value(val) {};

    // ��������� �����-������
    friend istream& operator>>(istream& in, roman& rom)
    {
        char romNumbers[7] = { 'I', 'V', 'X', 'L', 'C', 'D', 'M' };

        string str;
        in >> str;

        // �������� ������, ���� ��� ���� ������� ����� romNumbers, �� ������ ������
        for (int i = 0; i < str.size(); i++)
            for (int j = 0; j < 7; j++)
            {
                if (str[i] == romNumbers[j])
                    break;

                //  ���� ������ ��� �������� � �� �����������
                // => ���� ������ �� ������ � romNumbers
                if (j == 6)
                    throw logic_error("Invalid roman numbers: the string includes other symbols");
            }

        rom.value = str;

        return in;
    }
    friend ostream& operator<<(ostream& out, const roman& rom)
    {
        out << rom.value;

        return out;
    }

};

struct arabic
{
    int value;

    // ������������
    arabic() : value(0) {};
    arabic(int val) : value(val) {};

    // ��������� �����-������
    friend istream& operator>>(istream& in, arabic& rom)
    {
        int val;
        in >> val;
        rom.value = val;

        return in;
    }
    friend ostream& operator<<(ostream& out, const arabic& rom)
    {
        out << rom.value;

        return out;
    }
};


class Convertor
{
public:
    // �������� � �������
    roman toRoman(arabic& t);    // ��� �������� ���� (���������)
    roman toRoman(int& t);       // ��� int
    // ������� � ��������
    arabic toArabic(roman& t);   // ��� ������� ���� (���������)
    arabic toArabic(string& t);  // ��� ������� ������, � ������� ���������� ������� �����
};

#endif  // INCLUDE_ROMAN_H_