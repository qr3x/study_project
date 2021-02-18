#include<map>
#include "roman.h"

arabic functionalToArabic(string& str)
{
	/* Система перевода римских цифр в арабские:
	Берем поочередно пары римских цифр (сначала 1 цифра и 2, потом 2 и 3 и тд (последний символ не берем)).
	Если левая цифра меньше правой,	то вычитаем её, если больше, то прибавляем.
	В конце просто прибавляем последнюю цифру и суммируем с нашим результатом */

	map<char, int> roman_arabic;
	roman_arabic['I'] = 1;
	roman_arabic['V'] = 5;
	roman_arabic['X'] = 10;
	roman_arabic['L'] = 50;
	roman_arabic['C'] = 100;
	roman_arabic['D'] = 500;
	roman_arabic['M'] = 1000;

	int result = 0;
	for (int i = 0; i < str.size() - 1; i++)
	{
		int left_symbol = roman_arabic[str[i]];
		if (left_symbol < roman_arabic[str[i + 1]])
			result -= left_symbol;
		else
			result += left_symbol;
	}
	result += roman_arabic[str[str.size() - 1]];

	return arabic(result);
}

arabic Convertor::toArabic(roman& t)
{
	string str = t.value;	

	return functionalToArabic(str);
}

arabic Convertor::toArabic(string& str)
{
	return functionalToArabic(str);
}


string convert(int range, int val)
{
	/* Используем три области (такие, чтобы крайние могли повторяться 3 раза,
	а средние не могли повторяться:
	1. I, V, X - 1, 5, 10
	2. X, L, C - 10, 50, 100
	3. C, D, M - 100, 500, 1000
	*/
	/*
	:int range: область 1, 2 или 3
	:int val: значение, с которым сейчас работаем (число от 1 до 3999)
	:return: готовая строка для нашего val
	*/

	string romanStr("");
	int mod;
	switch (range)
	{
	case 1:
		switch (val)
		{
		// Чтобы при передача не возникало ошибок,
		// тк может передаться 0 в случае, если val = 100
		// Из functionalToRoman 0 не может сюда передаться
		case 0:
			romanStr += "";
			break;
		case 1:
			romanStr += "I";
			break;
		case 2:
			romanStr += "II";
			break;
		case 3:
			romanStr += "III";
			break;
		case 4:
			romanStr += "IV";
			break;
		case 5:
			romanStr += "V";
			break;
		case 6:
			romanStr += "VI";
			break;
		case 7:
			romanStr += "VII";
			break;
		case 8:
			romanStr += "VIII";
			break;
		case 9:
			romanStr += "IX";
			break;
		case 10:
			romanStr += "X";
			break;
		}
		break;
	case 2:
		mod = val / 10;
		switch (mod)
		{
		// Чтобы при передача не возникало ошибок,
		// тк может передаться 0 в случае, если val = 1000
		// Из functionalToRoman 0 не может сюда передаться
		case 0:
			romanStr += "";
			break;
		case 1:
			romanStr += "X";
			break;
		case 2:
			romanStr += "XX";
			break;
		case 3:
			romanStr += "XXX";
			break;
		case 4:
			romanStr += "XL";
			break;
		case 5:
			romanStr += "L";
			break;
		case 6:
			romanStr += "LX";
			break;
		case 7:
			romanStr += "LXX";
			break;
		case 8:
			romanStr += "LXXX";
			break;
		case 9:
			romanStr += "XC";
			break;
		case 10:
			romanStr += "C";
			break;
		}
		romanStr += convert(1, val % 10);
		break;
	case 3:
		mod = val / 100;
		switch (mod)
		{
		// Чтобы, если изначально было число большее 1000, при передача не возникало ошибок,
		// тк может передаться 0 в случаях, если val = 2000, или 3000, или 4000
		case 0:
			romanStr += "";
			break;
		case 1:
			romanStr = "C";
			break;
		case 2:
			romanStr = "CC";
			break;
		case 3:
			romanStr = "CCC";
			break;
		case 4:
			romanStr = "CD";
			break;
		case 5:
			romanStr = "D";
			break;
		case 6:
			romanStr = "DC";
			break;
		case 7:
			romanStr = "DCC";
			break;
		case 8:
			romanStr = "DCCC";
			break;
		case 9:
			romanStr = "CM";
			break;
		case 10:
			romanStr = "M";
			break;
		}
		romanStr += convert(2, val % 100);
		break;
	}

	return romanStr;
}

roman functionalToRoman(int val)
{
	/* Если число меньше 1000, тогда:
	рекурсивно заполняем строку с помощью функции convert()
	Eсли больше, тогда:
	определяем сколько M нужно подставить вначале строки, а остальные цифры вставляем
	с помощью функции convert() */

	if (val <= 0 || val > 3999)
		throw logic_error("Invalid number: the number should be > 0 and < 3900");

	if (val <= 10)
		return roman(convert(1, val));
	else if (val <= 100)
		return roman(convert(2, val));
	else if (val <= 1000)
		return roman(convert(3, val));

	string beginStr("");
	if (val < 2000)
		beginStr += "M";
	else if (val < 3000)
		beginStr += "MM";
	else if (val < 4000)
		beginStr += "MMM";
	beginStr += convert(3, val % 1000);

	return roman(beginStr);
}

roman Convertor::toRoman(arabic& t)
{
	int val = t.value;

	return functionalToRoman(val);
}

roman Convertor::toRoman(int& val)
{
	return functionalToRoman(val);
}
