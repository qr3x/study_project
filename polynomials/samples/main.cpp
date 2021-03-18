#include <iostream>
#include <polynomials.h>
#include <List.h>


using namespace std;

int main() {
	try
	{
		monom mon1(1, 2, 3, 4);
		monom mon2(5, 2, 3, 4);

		cout << "mon1 = " << mon1 << endl;
		cout << "mon2 = " << mon2 << endl;
		bool b = mon1 >= mon2;
		cout << "mon1 >= mon2: " << b << endl;
		cout << "mon1 + mon2: " << mon1 + mon2 << endl;
		try
		{
			monom mon3(10, 2, 3, 5);
			cout << "mon3 = " << mon3 << endl;
			cout << "try mon1 += mon3" << endl;
			mon1 += mon3;
		}
		catch (exception& e)
		{
			cout << "caught: " << e.what() << endl;
			cout << "type: " << typeid(e).name() << endl;
		}

		cout << endl;

		polynom pol1;
		polynom pol2;
		monom mon3(10, 5);
		cout << "mon3 = " << mon3 << endl;
		pol1 += mon1 + mon2;
		pol2 += mon3 * 3;
		cout << "pol1 += mon1 + mon2: " << pol1 << endl;
		cout << "pol2 += mon2 * 3: " << pol2 << endl;
		polynom pol3;
		pol3 = pol1 + pol2;
		cout << "pol3 = pol1 + pol2: " << pol1 + pol2 << endl;
	}
	catch (exception& e)
	{
		cout << "caught: " << e.what() << endl;
		cout << "type: " << typeid(e).name() << endl;
	}

	return 0;
}