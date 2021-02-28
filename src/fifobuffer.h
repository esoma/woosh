#ifndef WOOSH_FIFOBUFFER_H
#define WOOSH_FIFOBUFFER_H

// The FifoBuffer is a First-In First-Out object container. It may contain
// data of arbitrary size (as far as memory permits). Data may be added to the
// end of the buffer and data may be removed from the start of the buffer. The
// entire contents of the buffer is readable at any time and data is always
// stored continguously.
//
// FifoBuffer is designed to contain only homogeneous objects. Though with some
// cleverness could be used for objects of differing sizes.
//
// Setup and teardown is pretty basic:
//
//      FifoBuffer buffer;
//      if (!fifo_buffer_new(&buffer, 0))
//      {
//          // out of memory error
//          return 0;
//      }
//      // do stuff
//      fifo_buffer_delete(&buffer);
//
// Objects may be added to the buffer with the fifo_buffer_push function.
// Objects are *copied* into the buffer.
//
//      int data = 10;
//      if (!fifo_buffer_push(&buffer, &data, sizeof(int)))
//      {
//          // out of memory error
//          return 0;
//      }
//
// Objects may be read from the buffer with the fifo_buffer_read function.
//
//      int *start;
//      int *end;
//      fifo_buffer_read(&buffer, &start, &end);
//      for (; start < end; start++)
//      {
//          printf("%i\n", *start);
//      }
//
// Objects may be removed from the start of the buffer with fifo_buffer_pop.
//
//      fifo_buffer_pop(&buffer, sizeof(int));
//      printf("empty: %i\n", fifo_buffer_is_empty(&buffer));
//

// c
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct FifoBuffer
{
    // where we'll actually store data
    char *buffer;
    // how large the buffer is
    size_t size;
    // the start/end of valid data in the buffer
    // note that `end` is not inclusive so start == end means no data
    char *start;
    char *end;
} FifoBuffer;

int fifo_buffer_new(FifoBuffer *, size_t);

void *fifo_buffer_push(FifoBuffer *, void *, size_t);
void fifo_buffer_read(FifoBuffer *, void **, void **);
int fifo_buffer_is_empty(FifoBuffer *);
void fifo_buffer_pop(FifoBuffer *, size_t);

void fifo_buffer_delete(FifoBuffer *);

#endif
