#include <assert.h>
#include <stdbool.h>

bool isEven(int num) {
    if(num % 2 == 0) {
        return true;
    }
    return false;
}

int main() {
    int num1 = 11;
    int num2 = 9;

    assert(isEven(num1)); // Asserting that num1 is even
    assert(isEven(num2)); // Asserting that num2 is not even

    return 0;
}