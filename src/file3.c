#include <stdio.h>
int random();
void printC() {
    int a=random();
    __CPROVER_assume(a>4);
    assert(a>3);
    printf("This is function C.\n");
}