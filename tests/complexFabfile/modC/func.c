#include <stdio.h>
#include "func.h"
#include "common.h"

int fib(int x)
{
    if( x == 0 )
        return 0;
    else if( x == 1 )
        return 1;

    return fib(x-1) + fib(x-2);
}

void out_func(void)
{
    printf("%s", FUNC_H_LOG_STR);
}
