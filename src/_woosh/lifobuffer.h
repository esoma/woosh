#ifndef WOOSH_LIFOBUFFER_H
#define WOOSH_LIFOBUFFER_H

// The LifoBuffer is a stack. It may contain data of arbitrary size (as far as
// memory permits). Data may be added to the top of the stack and removed from
// the top of the stack. The data of the entire stack is visible at any time.
//
// LifoBuffer is designed to contain only homogeneous objects. Though with some
// cleverness could be used for objects of differing sizes.
//
// Setup and teardown is pretty basic:
//
//      LifoBuffer buffer;
//      if (!lifo_buffer_new(&buffer, 0))
//      {
//          // out of memory error
//          return 0;
//      }
//      // do stuff
//      lifo_buffer_delete(&buffer);
//
// Objects may be added to the buffer with the lifo_buffer_push function.
// Objects are *copied* into the buffer.
//
//      int data = 10;
//      if (!lifo_buffer_push(&buffer, &data, sizeof(int)))
//      {
//          // out of memory error
//          return 0;
//      }
//
// Objects may be read from the buffer with the lifo_buffer_peek function.
//
//      for (size_t i = 0; i < lifo_buffer_count(&buffer); i++)
//      {
//          int *data;
//          lifo_buffer_peek(&buffer, &data, sizeof(int), i);
//          printf("%i\n", *data);
//      }
//
// Objects may be removed from the top of the buffer with lifo_buffer_pop.
//
//      lifo_buffer_pop(&buffer, sizeof(int));
//      printf("empty: %i\n", lifo_buffer_is_empty(&buffer));
//

// c
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct LifoBuffer
{
    // where we'll actually store data
    char *buffer;
    // how large the buffer is
    size_t size;
    // the non-inclusive end of the buffer where data is stored (so
    // top == buffer) means the buffer is empty
    char *top;
} LifoBuffer;

int lifo_buffer_new(LifoBuffer *, size_t);

int lifo_buffer_push(LifoBuffer *, const void *, size_t );
int lifo_buffer_is_empty(LifoBuffer *buffer);
void lifo_buffer_peek(LifoBuffer *, const void **, size_t, size_t);
size_t lifo_buffer_count(LifoBuffer *, size_t);
void lifo_buffer_pop(LifoBuffer *, size_t);

void lifo_buffer_delete(LifoBuffer *);

#endif
