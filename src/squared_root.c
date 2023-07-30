#include <assert.h>

int sqrt(int x) {
    if (x == 0 || x == 1) {
        return x;
    }

    int start = 1, end = x, ans;
    while (start <= end) {
        int mid = (start + end) / 2;

        if (mid*mid == x) {
            return mid;
        }

        if (mid*mid < x) {
            start = mid + 1;
            ans = mid;
        } else {
            end = mid - 1;
        }
    }
    return ans;
}

void main(void) {
    int x = 10;
    int result = sqrt(x);
    assert(result*result == x); // 断言失败，因为10的平方根不是整数
}
