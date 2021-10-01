#include <iostream>
#include "height.h"


using namespace std;


int main()
{
    int tree[] = { 3, 4, 6, 5, 7, -1, 3, 3, 6, 8, 8, 8, 11, 5 };
    int len = sizeof(tree) / sizeof(tree[0]);

    cout << "Height = " << findHeight(tree, len) << endl;

    return 0;
}
