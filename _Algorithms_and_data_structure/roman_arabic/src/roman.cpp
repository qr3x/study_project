#include<map>
#include "roman.h"

arabic functionalToArabic(string& str)
{
	/* ������� �������� ������� ���� � ��������:
	����� ���������� ���� ������� ���� (������� 1 ����� � 2, ����� 2 � 3 � �� (��������� ������ �� �����)).
	���� ����� ����� ������ ������,	�� �������� �, ���� ������, �� ����������.
	� ����� ������ ���������� ��������� ����� � ��������� � ����� ����������� */

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
	/* ���������� ��� ������� (�����, ����� ������� ����� ����������� 3 ����,
	� ������� �� ����� �����������:
	1. I, V, X - 1, 5, 10
	2. X, L, C - 10, 50, 100
	3. C, D, M - 100, 500, 1000
	*/
	/*
	:int range: ������� 1, 2 ��� 3
	:int val: ��������, � ������� ������ �������� (����� �� 1 �� 3999)
	:return: ������� ������ ��� ������ val
	*/

	string romanStr("");
	int mod;
	switch (range)
	{
	case 1:
		switch (val)
		{
		// ����� ��� �������� �� ��������� ������,
		// �� ����� ���������� 0 � ������, ���� val = 100
		// �� functionalToRoman 0 �� ����� ���� ����������
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
		// ����� ��� �������� �� ��������� ������,
		// �� ����� ���������� 0 � ������, ���� val = 1000
		// �� functionalToRoman 0 �� ����� ���� ����������
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
		// �����, ���� ���������� ���� ����� ������� 1000, ��� �������� �� ��������� ������,
		// �� ����� ���������� 0 � �������, ���� val = 2000, ��� 3000, ��� 4000
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
	/* ���� ����� ������ 1000, �����:
	���������� ��������� ������ � ������� ������� convert()
	E��� ������, �����:
	���������� ������� M ����� ���������� ������� ������, � ��������� ����� ���������
	� ������� ������� convert() */

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
