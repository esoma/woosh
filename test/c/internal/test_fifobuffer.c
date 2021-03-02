
// c
#include <stdio.h>
// fifobuffer
#include "fifobuffer.h"

int main()
{
    fprintf(stderr, "test_fifobuffer...");
    
    FifoBuffer fb;
    if (!fifo_buffer_new(&fb, sizeof(char) * 5))
    {
        fprintf(stderr, "failed to create buffer\n");
        return EXIT_FAILURE;
    }
    assert(fb.size == sizeof(char) * 5);

    const char *start;
    const char *end;
    fifo_buffer_read(&fb, (void **)&start, (void **)&end);
    assert(start);
    assert(end);
    assert(start == end);
    
    assert(fifo_buffer_is_empty(&fb));

    if (!fifo_buffer_push(&fb, "h", sizeof(char) * 1))
    {
        fprintf(stderr, "failed to add 'h' to buffer\n");
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
    
    assert(!fifo_buffer_is_empty(&fb));

    if (!fifo_buffer_push(&fb, "ello", sizeof(char) * 4))
    {
        fprintf(stderr, "failed to add 'ello' to buffer\n");
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
    
    assert(!fifo_buffer_is_empty(&fb));

    if (!fifo_buffer_push(&fb, " world", sizeof(char) * 6))
    {
        fprintf(stderr, "failed to add ' world' to buffer\n");
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
    
    assert(!fifo_buffer_is_empty(&fb));

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
    
    assert(!fifo_buffer_is_empty(&fb));

    if (!fifo_buffer_push(&fb, "X", sizeof(char) * 1))
    {
        fprintf(stderr, "failed to add 'X' to buffer\n");
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
    
    assert(!fifo_buffer_is_empty(&fb));

    fifo_buffer_delete(&fb);
    
    // this test part of the test specifically manipulates some of the inner
    // workings of the fifo buffer to cover a specific and pretty unusual
    // scenario
    
    // in this case we're going to have a buffer with an initial size of 3
    // chars, so 3 items can fit in the buffer
    if (!fifo_buffer_new(&fb, sizeof(char) * 3))
    {
        fprintf(stderr, "failed to create buffer\n");
        return EXIT_FAILURE;
    }
    
    // we'll fill the buffer so that all three items are in it
    // internally our buffer should look (something) like this: a b c
    if (!fifo_buffer_push(&fb, "abc", sizeof(char) * 3))
    {
        fprintf(stderr, "failed to add 'abc' to buffer\n");
        return EXIT_FAILURE;
    }
    
    // then we'll pop the first two items out, internally our buffer should
    // look (something) like this: _ _ c
    fifo_buffer_pop(&fb, 2);
    
    // now we'll add one character to the buffer
    // the internal buffer is large enough to hold the character, but it must
    // be kept sequential, so it will be changed to: c d _
    //
    // this should cover a specific branch internally that will move c, rather
    // than copy it because it doesn't overlap in the buffer
    if (!fifo_buffer_push(&fb, "d", sizeof(char) * 1))
    {
        fprintf(stderr, "failed to add 'd' to buffer\n");
        return EXIT_FAILURE;
    }
    
    // done with this specific internal case
    fifo_buffer_delete(&fb);
    
    fprintf(stderr, "passed\n");
    return EXIT_SUCCESS;
}
