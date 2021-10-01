#ifndef INCLUDE_ROMAN_H_
#include <iostream>

#define INCLUDE_ROMAN_H_

using namespace std;


struct roman
{
    string value;

    // Конструкторы
    roman() : value("") {};
    roman(char val)
    {
        this->value = val;
    }
    roman(string val) : value(val) {};

    // Операторы ввода-вывода
    friend istream& operator>>(istream& in, roman& rom)
    {
        char romNumbers[7] = { 'I', 'V', 'X', 'L', 'C', 'D', 'M' };

        string str;
        in >> str;

        // Проверка строки, если там есть символы кроме romNumbers, то выдаем ошибку
        for (int i = 0; i < str.size(); i++)
            for (int j = 0; j < 7; j++)
            {
                if (str[i] == romNumbers[j])
                    break;

                //  Если прошло все итерации и не брейкнулось
                // => этот символ не входит в romNumbers
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

    // Конструкторы
    arabic() : value(0) {};
    arabic(int val) : value(val) {};

    // Операторы ввода-вывода
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
    // Арабские в римские
    roman toRoman(arabic& t);    // Для арабских цифр (структуры)
    roman toRoman(int& t);       // Для int
    // Римские в арабские
    arabic toArabic(roman& t);   // Для римских цифр (структуры)
    arabic toArabic(string& t);  // Для обычной строки, в которой содержатся римские цифры
};

#endif  // INCLUDE_ROMAN_H_