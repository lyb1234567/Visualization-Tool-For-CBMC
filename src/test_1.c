#include <stdio.h>
int puts(const char *s)
{
}

int main(int argc, char **argv)
{
  puts(argv[2]);
  return 0;
}