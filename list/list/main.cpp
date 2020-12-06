#include <iostream>

#include "list.h"

using namespace std;


int main()
{
    List<int> list;
    list.Add(5);
    list.Add(7);
    list.Add(4);
    list.Add(3);
    list.Add(1);
    list.Add(9);

    cout << "List: ";
    list.Print();
    cout << "Count list = " << list.GetCount() << endl << endl;

    cout << "Second node in list: " << list[1] << endl;
    list.Delete(1);
    cout << "Deleted second node in list" << endl;
    cout << "Second node in list: " << list[1] << endl;
    cout << "List: ";
    list.Print();
    cout << "Count list = " << list.GetCount() << endl << endl;

    list.Clear();
    list.Print();
    cout << "Count = " << list.GetCount() << endl;

    // throw error
    //cout << "Second node in list: " << list[2] << endl;

    return 0;
}