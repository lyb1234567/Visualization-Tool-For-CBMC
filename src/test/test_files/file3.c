#include <stdio.h>
int random();
void printC() {
    int a=random();
    assert(a>3);
    printf("This is function C.\n");
}