#include <stdio.h>
int global = 2;
int main () {
	int a[3];
	
	a[1] = 1;
	int b = 3;
	int f = a[0] + 1;
	b = 2;
	if(a[0] > (b+1)){
		b = 5;
	}

	int d = a[1] + 1;
	// int e = global;
	int c = a[0] + b;

	return 0;
}


