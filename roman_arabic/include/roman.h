#ifndef INCLUDE_ROMAN_H_
#include <iostream>

#define INCLUDE_ROMAN_H_

using namespace std;


struct roman {
    string value;
public:
    roman() : value("") {};
    roman(char val)
    {
        this->value = val;
    }
    roman(string val) : value(val) {};
};

struct arabic {
    int value;
public:
    arabic() : value(0) {};
    arabic(int val) : value(val) {};
};


class Convertor {
public:
    // Арабские в римские
    roman toRoman(arabic& t);    // Для арабских цифр (структуры)
    roman toRoman(int& t);       // Для int
    // Римские в арабские
    arabic toArabic(roman& t);   // Для римских цифр (структуры)
    arabic toArabic(string& t);  // Для обычной строки, в которой содержатся римские цифры

    //bool check(roman &t);      // IIII - IV

    // оператор ввода-вывода, либо print

};

#endif  // INCLUDE_ROMAN_H_