#include "islands.h"
#include <conio.h>
using namespace std;

int main() {
	int m, n;
	cout << "Enter row and columns: ";
	cin >> m >> n;

	int** arr = new int* [m];
	for (int i = 0; i < m; i++) {
		// create our island using random or typing
		arr[i] = new int[n];
		for (int j = 0; j < n; j++) {
			arr[i][j] = rand() % 2 + 0; 
			// or
			// cin >> arr[i][j];
		}
		// if using typing (cin)
		// cout << endl;
	}

	// output ours island before and after foundIslands()
	cout << "before foundIslands():" << endl;
	out(arr, m, n);

	int result = foundIslands(arr, m, n);

	cout << endl << endl << "after foundIslands():";
	out(arr, m, n);

	cout << endl << endl << "result: " << result;

	return 0;
}