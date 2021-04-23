#include <iostream>
#include <string>
#include <tree.h>


int main()
{
	setlocale(LC_ALL, "Russian");

	string str = "шла саша по шоссе шла";

	Tree tr(str);
	cout << tr.getCount("по") << endl;

	return 0;
}