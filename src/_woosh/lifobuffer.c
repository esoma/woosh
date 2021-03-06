
// woosh
#include "lifobuffer.h"


// initialize the buffer structure, must be called before any other operations
//
// size_hint is the approximate average size of the buffer, note that this isn't
// a hard limit, just a hint to reduce memory allocations
//
// returns truthy on sucess and 0 on OOM error
int
lifo_buffer_new(LifoBuffer *buffer, size_t size_hint)
{
    assert(buffer);
    if (size_hint == 0){ size_hint = 1; }
    buffer->buffer = malloc(size_hint);
    if (!buffer->buffer){ return 0; }
    buffer->size = size_hint;
    buffer->top = buffer->buffer;
    return 1;
}

// push the data onto the end of the buffer
//
// source is a pointer to the data and size is how many bytes to copy
//
// returns 0 on OOM error or a pointer to the copied data on success
int
lifo_buffer_push(LifoBuffer *buffer, const void *source, size_t size)
{
    assert(buffer);
    assert(buffer->top);
    // if there isn't enough space remaining for the data we want to push onto
    // the buffer then we'll need to resize it
    size_t remaining_size = buffer->size - (buffer->top - buffer->buffer);
    if (remaining_size < size)
    {
        size_t target_size = buffer->size + size;
        char *new_buffer = realloc(buffer->buffer, target_size);
        if (!new_buffer){ return 0; }
        if (new_buffer != buffer->buffer)
        {
            buffer->top = new_buffer + (buffer->top - buffer->buffer);
            buffer->buffer = new_buffer;
        }
        buffer->size = target_size;
    }
    void *result = memmove(buffer->top, source, size);
    if (!result){ return 0; }
    buffer->top += size;
    return 1;
}

// returns truthy if the buffer is empty or falsey if it is not
int
lifo_buffer_is_empty(LifoBuffer *buffer)
{
    assert(buffer);
    return buffer->top == buffer->buffer;
}

// sets destination to the location of the object at the top of the stack with
// the given size in the buffer
//
// offset can be used to peek below the top of the stack (offset of 1 would be
// the second to last item on the stack)
//
// note that the address returned by this function is no longer valid between
// pushes (it may be, but is not guarenteed to)
//
// destination is set to 0 if no object exists at the position requested
void
lifo_buffer_peek(
    LifoBuffer *buffer,
    const void **destination,
    size_t size,
    size_t offset
)
{
    assert(buffer);
    assert(buffer->top >= buffer->buffer);
    assert(destination);
    assert(size);
    offset *= size;
    if ((size_t)(buffer->top - buffer->buffer) >= size + offset)
    {
        *destination = buffer->top - (size + offset);
    }
    else
    {
        *destination = 0;
    }
}

// returns the number of items in the stack, assuming all items have the same
// size
size_t
lifo_buffer_count(LifoBuffer *buffer, size_t size)
{
    assert(buffer);
    assert(size);
    return (buffer->top - buffer->buffer) / size;
}

// remove the top item from the stack
void
lifo_buffer_pop(LifoBuffer *buffer, size_t size)
{
    assert(buffer);
    assert(size);
    assert(buffer->top - buffer->buffer >= size);
    buffer->top -= size;
}

// deallocates the stack
void
lifo_buffer_delete(LifoBuffer *buffer)
{
    assert(buffer);
    if (buffer->buffer)
    {
        free(buffer->buffer);
        buffer->buffer = 0;
    }
    buffer->top = 0;
}
