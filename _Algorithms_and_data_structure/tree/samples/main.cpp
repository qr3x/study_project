#include <iostream>
#include <string>
#include <tree.h>


int main()
{
	setlocale(LC_ALL, "Russian");

	string str = "��� ���� �� ����� ���";

	Tree tr(str);
	cout << tr.getCount("��") << endl;

	return 0;
}