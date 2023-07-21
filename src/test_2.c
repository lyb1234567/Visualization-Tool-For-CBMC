#include <assert.h>
#include <stddef.h>

// Verify boundary conditions with assertions
void test_array(int *array, int size) {
    assert(size > 0);  // This assertion will fail
}

// Verify function post-conditions with assertions
void increment(int *value) {
    (*value)--;  // Decrease the value to make the next assertion fail
    assert(*value > 0);
}

// Use assertions to check for null pointers
void increment_ptr(int *value) {
    value = NULL;  // Set the value to NULL to make the next assertion fail
    assert(value != NULL);
}

// Verify loop invariants
void zero_array(int *array, int size) {
    for(int i = 0; i < size; i++) {
        array[i] = 1;  // Set the value to 1 to make the next assertion fail
        assert(array[i+1] == 0);
    }
}

int main() {
    int value = 1;
    increment(&value);

    int *value_ptr = &value;
    increment_ptr(value_ptr);

    int size = 0;  // Set the size to 0 to make the assertion in test_array fail
    int array[size];
    test_array(array, size);

    size = 10;
    zero_array(array, size);
    return 0;
}
