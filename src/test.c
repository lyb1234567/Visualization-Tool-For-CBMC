#include <time.h>
#include <stdlib.h>
#include <assert.h>
void main(void)
{
int x = 10;
srand(time(NULL));   // Initialization, should only be called once.
int y = rand();      // Returns a pseudo-random integer between 0 and RAND_MAX.
int z = x-y;
assert(z > 0);
}