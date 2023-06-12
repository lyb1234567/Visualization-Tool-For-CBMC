#include <assert.h>

extern int multiply(int a, int b);

void check_multiply() {
    int result = multiply(2, 3);
    assert(result == 6);
}