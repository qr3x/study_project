#include <iostream>


using namespace std;


void IslandWalk(int** arr, int m, int n, int i, int j, int NumForIsl) {
	arr[i][j] = NumForIsl;
	
	// look to the right
	if (i + 1 < m) {
		// zero right
		if (arr[i + 1][j] == 0) {
			IslandWalk(arr, m, n, i + 1, j, NumForIsl);
		}
		// zero bottom right
		if (j + 1 < n)
			if (arr[i + 1][j + 1] == 0) {
				IslandWalk(arr, m, n, i + 1, j + 1, NumForIsl);
			}
	}

	// look to the bottom
	if (j + 1 < n) {
		// zero bottom
		if (arr[i][j + 1] == 0) {
			IslandWalk(arr, m, n, i, j + 1, NumForIsl);
		}
		// zero bottom left
		if(i > 0)
			if (arr[i - 1][j + 1] == 0) {
				IslandWalk(arr, m, n, i - 1, j + 1, NumForIsl);
			}
	}
	
	// look to the top
	if (j > 0) {
		// zero top
		if (arr[i][j - 1] == 0)
			IslandWalk(arr, m, n, i, j - 1, NumForIsl);
		// zero top left
		if (i > 0)
			if (arr[i - 1][j - 1] == 0)
				IslandWalk(arr, m, n, i - 1, j - 1, NumForIsl);
	}

}

int foundIslands(int** arr, int m, int n) {
	// we go through a two-dimensional array
	// met zero - look for zeros on the left, right, bottom and mark them
	int Count = 0; int NumForIsl = 2;
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			if (arr[i][j] == 0) {
				Count++;
				IslandWalk(arr, m, n, i, j, NumForIsl);
				NumForIsl += 2;
			}
		}
	}

	return Count;
}

void out(int** arr, int m, int n) {
	for (int i = 0; i < m; i++) {
		cout << '\n' << "";
		for (int j = 0; j < n; j++) {
			cout << arr[i][j] << ' ';
		}
	}
}