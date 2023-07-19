#include <stdio.h>
#include <stdlib.h>

void printB() {
    int x=random();
    int y=7;
    int a=random();
    int asdas=random();
    x=random()-1;
    int z=x+y;
    assert(z + x <= 10);
    printf("This is function B.\n");
}