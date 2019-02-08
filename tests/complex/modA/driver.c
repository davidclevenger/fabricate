#include <stdio.h>
#include "func.h"
#include "common.h"


int main()
{
    printf("fib(6) == %d\n", fib(6));
out(FUNC_H_LOG_STR);
printf("<equals>\n");
out_func();

}   
