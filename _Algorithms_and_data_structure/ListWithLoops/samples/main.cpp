#include "List.h"

using namespace std;


int main()
{
    Node* n1 = new Node(1);
    Node* n2 = new Node(5);
    Node* n3 = new Node(10);

    List L;
    L.add(n2);
    L.add(n1);
    L.add(n3);
    L.add(n2);


    for (int i = 0; i < 3; i++)
    {
        int result;
        if (i == 0)
            result = L.isLoop1();
        else if (i == 1)
            result = L.isLoop2();
        else
            result = L.isLoop3();
        string res_str;
        if (result != 0)
            res_str = "yes";
        else
            res_str = "no";
        cout << "Is loops" << i + 1 << ": " << res_str << endl;
    }
    

    return 0;
}