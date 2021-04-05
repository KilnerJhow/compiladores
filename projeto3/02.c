#include <stdio.h>

int main () {
	int a[3] = {1, 2, 3};
	int b = 3;

	b = 4;
	a[0] = 4;

	if(a[0] > (b+1)){
		b = 5;
	}

	int c = a[0] + b;

	return 0;
}


