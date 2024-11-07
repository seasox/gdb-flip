#include <stdio.h>

int main(void) {
	int x = 0;
	printf("Comparing x against known value... ");
	x += 17;
	x += 3;
	if (x != 20) {
		printf("failed! Expected %d, got %d\n", 20, x);
		return -1;
	}
	printf("successful.\n");
	return 0;
}

