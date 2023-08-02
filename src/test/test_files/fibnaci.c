#include <assert.h>

int fibonacci(int n) {
    if (n <= 0) {
        return 0;
    } else if (n == 1) {
        return 1;
    } else {
        return fibonacci(n-1) + fibonacci(n-2);
    }
}

void main(void) {
    int result = fibonacci(10);
    assert(result < 50); // 断言失败，因为第10个斐波那契数为55
}
