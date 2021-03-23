#include <stdio.h>
int unum = 1;

float half (float x) {
	return x / 2;
}

int scalar (int a, int b) {
	int array[10];
	for (int i = 0; i < 10; i++) {
		if (a < b) a -= b;
		array[i] = a;
	}
	/***********
	 * comment *
	 ***********/
	if (a > b) {
		a /= b - unum * 2.5 - (4 <= a - b);
	} else if (a < b) {
		b += a / -unum + (8 >= b * a);
	} else {
		b = a;
	}

	return half(a * a + b + (b - a) * b);
}

void main(){
    int kkkk[3] = {1, "12", 1.0};
}