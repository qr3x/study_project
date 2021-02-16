#include<map>
#include "roman.h"


arabic Convertor::toArabic(roman& t)
{
	/* Система перевода римских цифр в арабские:
	Берем поочередно пары римских цифр (сначала 1 цифра и 2, потом 2 и 3 и тд (последний символ не берем)).
	Если левая цифра меньше правой,	то вычитаем её, если больше, то прибавляем.
	В конце просто прибавляем последнюю цифру и суммируем с нашим результатом*/

	map<char, int> roman_arabic;
	roman_arabic['I'] = 1;
	roman_arabic['V'] = 5;
	roman_arabic['X'] = 10;
	roman_arabic['L'] = 50;
	roman_arabic['C'] = 100;
	roman_arabic['D'] = 500;
	roman_arabic['M'] = 1000;

	int result = 0;
	for (int i = 0; i < t.value.size() - 1; i++)
	{
		int left_symbol = roman_arabic[t.value[i]];
		if (left_symbol < roman_arabic[t.value[i + 1]])
			result -= left_symbol;
		else
			result += left_symbol;
	}
	result += roman_arabic[t.value[t.value.size() - 1]];

	return arabic(result);
}

arabic Convertor::toArabic(string& t)
{
	/* Система перевода римских цифр в арабские:
	Берем поочередно пары римских цифр (сначала 1 цифра и 2, потом 2 и 3 и тд (последний символ не берем)).
	Если левая цифра меньше правой,	то вычитаем её, если больше, то прибавляем.
	В конце просто прибавляем последнюю цифру и суммируем с нашим результатом*/

	map<char, int> roman_arabic;
	roman_arabic['I'] = 1;
	roman_arabic['V'] = 5;
	roman_arabic['X'] = 10;
	roman_arabic['L'] = 50;
	roman_arabic['C'] = 100;
	roman_arabic['D'] = 500;
	roman_arabic['M'] = 1000;

	int result = 0;
	for (int i = 0; i < t.size() - 1; i++)
	{
		int left_symbol = roman_arabic[t[i]];
		if (left_symbol < roman_arabic[t[i + 1]])
			result -= left_symbol;
		else
			result += left_symbol;
	}
	result += roman_arabic[t[t.size() - 1]];

	return arabic(result);
}


string convert(int range, int val)
{
	map<int, char> orderOfRomeNumbers;
	orderOfRomeNumbers[0] = 'I';
	orderOfRomeNumbers[1] = 'V';
	orderOfRomeNumbers[2] = 'X';
	orderOfRomeNumbers[3] = 'L';
	orderOfRomeNumbers[4] = 'C';
	orderOfRomeNumbers[5] = 'D';
	orderOfRomeNumbers[6] = 'M';

	map<char, int> roman_arabic;
	roman_arabic['I'] = 1;     // Можно использовать 3 раза
	roman_arabic['V'] = 5;     // Нельзя повторять
	roman_arabic['X'] = 10;    // Можно использовать 3 раза
	roman_arabic['L'] = 50;    // Нельзя повторять
	roman_arabic['C'] = 100;   // Можно использовать 3 раза
	roman_arabic['D'] = 500;   // Нельзя повторять
	roman_arabic['M'] = 1000;  // Можно использовать 3 раза

	string romanStr("");
	int mod;
	switch (range)
	{
	case 1:
		switch (val)
		{
		// Если мы передаем из других range (2 или 3)
		// Из toRoman 0 не сможет сюда передаться 
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
		// Если мы передаем из других range (3)
		// Из toRoman 0 не сможет сюда передаться
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
		// тк может передаться 0
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

roman Convertor::toRoman(arabic& t)
{
	/* Если число меньше 1000, тогда:
	рекурсивно заполняем строку с помощью функции convert()
	Eсли больше, тогда:
	определяем сколько M нужно подставить вначале строки, а остальные цифры вставляем
	с помощью функции convert() */

	int val = t.value;
	
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

roman Convertor::toRoman(int& t)
{
	/* Если число меньше 1000, тогда:
	рекурсивно заполняем строку с помощью функции convert()
	Eсли больше, тогда:
	определяем сколько M нужно подставить вначале строки, а остальные цифры вставляем
	с помощью функции convert() */

	int val = t;

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
