#include <stdio.h>
#include "func.h"
#include "common.h"

int main()
{
    int magic_f = get_magic();
    int magic = MAGIC;
    printf("%d == %d\n", magic_f, magic);
}
