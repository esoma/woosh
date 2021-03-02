
// c
#include <stdio.h>
// lifobuffer
#include "lifobuffer.h"

int main()
{
    fprintf(stderr, "test_lifobuffer...");
    
    int input;
    const int *output;

    LifoBuffer lb;
    if (!lifo_buffer_new(&lb, sizeof(int)))
    {
        fprintf(stderr, "failed to create buffer\n");
        return EXIT_FAILURE;
    }
    assert(lb.size == sizeof(int));

    input = 100;
    if (!lifo_buffer_push(&lb, &input, sizeof(int)))
    {
        fprintf(stderr, "failed to add 100 to buffer\n");
        return EXIT_FAILURE;
    }
    assert(lb.size == sizeof(int));
    assert(lb.buffer + sizeof(int) == lb.top);

    lifo_buffer_peek(&lb, (const void **)&output, sizeof(int), 0);
    assert(*output == 100);

    input = 99;
    if (!lifo_buffer_push(&lb, &input, sizeof(int)))
    {
        fprintf(stderr, "failed to add 99 to buffer\n");
        return EXIT_FAILURE;
    }
    assert(lb.size == sizeof(int) * 2);
    assert(lb.buffer + sizeof(int) * 2 == lb.top);

    lifo_buffer_peek(&lb, (const void **)&output, sizeof(int), 0);
    assert(*output == 99);

    lifo_buffer_pop(&lb, sizeof(int));
    assert(lb.size == sizeof(int) * 2);
    assert(lb.buffer + sizeof(int) == lb.top);

    lifo_buffer_peek(&lb, (const void **)&output, sizeof(int), 0);
    assert(*output == 100);

    lifo_buffer_delete(&lb);
    
    fprintf(stderr, "passed\n");
    return EXIT_SUCCESS;
}
