#include <stdio.h>

void printB() {
    int x=random();
    int y=random();
    int z=x+y;
    assert(z<=10);
    printf("This is function B.\n");
}