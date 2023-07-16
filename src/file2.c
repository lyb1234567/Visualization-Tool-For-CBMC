#include <stdio.h>

void printB() {
    int x=random();
    int y=random();
    int a=random();
    int asdas=random();
    int z=x+y;
    assert(z + x <= 10);
    printf("This is function B.\n");
}