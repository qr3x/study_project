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

    int result = L.isCircle();
    cout << "Count loops: " << result << endl;

    return 0;
}