#include <assert.h>

double myabs (double x) 
{
float y = x;
if (x <= 0) {
  y = -x;
  }
 return y;
}

int main()
{
   double x=random();
   double y=myabs(x);
   assert(y>=0 &&(y==-x || -y==x) );
}