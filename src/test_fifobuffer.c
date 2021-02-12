
// c
#include <stdio.h>
// fifobuffer
#include "fifobuffer.h"

int main()
{
    FifoBuffer fb;
    if (!fifo_buffer_new(&fb, sizeof(char) * 5))
    {
        fprintf(stderr, "failed to create buffer");
        return EXIT_FAILURE;
    }
    assert(fb.size == sizeof(char) * 5);

    const char *start;
    const char *end;
    fifo_buffer_read(&fb, (void **)&start, (void **)&end);
    assert(start);
    assert(end);
    assert(start == end);

    if (!fifo_buffer_push(&fb, "h", sizeof(char) * 1))
    {
        fprintf(stderr, "failed to add 'h' to buffer");
        return EXIT_FAILURE;
    }
    assert(fb.size == sizeof(char) * 5);
    assert(fb.buffer == fb.start);
    assert(fb.buffer + 1 == fb.end);

    fifo_buffer_read(&fb, (void **)&start, (void **)&end);
    assert(start);
    assert(end);
    assert(start + 1 == end);
    assert(*start == 'h');

    if (!fifo_buffer_push(&fb, "ello", sizeof(char) * 4))
    {
        fprintf(stderr, "failed to add 'ello' to buffer");
        return EXIT_FAILURE;
    }
    assert(fb.size == sizeof(char) * 5);
    assert(fb.buffer == fb.start);
    assert(fb.buffer + 5 == fb.end);

    fifo_buffer_read(&fb, (void **)&start, (void **)&end);
    assert(start);
    assert(end);
    assert(start + 5 == end);
    assert(start[0] == 'h');
    assert(start[1] == 'e');
    assert(start[2] == 'l');
    assert(start[3] == 'l');
    assert(start[4] == 'o');

    if (!fifo_buffer_push(&fb, " world", sizeof(char) * 6))
    {
        fprintf(stderr, "failed to add ' world' to buffer");
        return EXIT_FAILURE;
    }
    assert(fb.size == sizeof(char) * 11);
    assert(fb.buffer == fb.start);
    assert(fb.buffer + 11 == fb.end);

    fifo_buffer_read(&fb, (void **)&start, (void **)&end);
    assert(start);
    assert(end);
    assert(start + 11 == end);
    assert(start[0] == 'h');
    assert(start[1] == 'e');
    assert(start[2] == 'l');
    assert(start[3] == 'l');
    assert(start[4] == 'o');
    assert(start[5] == ' ');
    assert(start[6] == 'w');
    assert(start[7] == 'o');
    assert(start[8] == 'r');
    assert(start[9] == 'l');
    assert(start[10] == 'd');

    fifo_buffer_pop(&fb, 1);
    assert(fb.size == sizeof(char) * 11);
    assert(fb.buffer + 1 == fb.start);
    assert(fb.buffer + 11 == fb.end);

    fifo_buffer_read(&fb, (void **)&start, (void **)&end);
    assert(start);
    assert(end);
    assert(start + 10 == end);
    assert(start[0] == 'e');
    assert(start[1] == 'l');
    assert(start[2] == 'l');
    assert(start[3] == 'o');
    assert(start[4] == ' ');
    assert(start[5] == 'w');
    assert(start[6] == 'o');
    assert(start[7] == 'r');
    assert(start[8] == 'l');
    assert(start[9] == 'd');

    if (!fifo_buffer_push(&fb, "X", sizeof(char) * 1))
    {
        fprintf(stderr, "failed to add 'X' to buffer");
        return EXIT_FAILURE;
    }
    assert(fb.size == sizeof(char) * 11);
    assert(fb.buffer == fb.start);
    assert(fb.buffer + 11 == fb.end);

    fifo_buffer_read(&fb, (void **)&start, (void **)&end);
    assert(start);
    assert(end);
    assert(start + 11 == end);
    assert(start[0] == 'e');
    assert(start[1] == 'l');
    assert(start[2] == 'l');
    assert(start[3] == 'o');
    assert(start[4] == ' ');
    assert(start[5] == 'w');
    assert(start[6] == 'o');
    assert(start[7] == 'r');
    assert(start[8] == 'l');
    assert(start[9] == 'd');
    assert(start[10] == 'X');

    fifo_buffer_delete(&fb);
    return EXIT_SUCCESS;
}
