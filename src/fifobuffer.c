
// woosh
#include "fifobuffer.h"

// initialize the buffer structure, must be called before any other operations
//
// size_hint is the approximate average size of the buffer, note that this 
// isn't a hard limit, just a hint to reduce memory allocations
//
// returns truthy on sucess and 0 on OOM error
int
fifo_buffer_new(FifoBuffer *buffer, size_t size_hint)
{
    assert(buffer);
    if (size_hint == 0){ size_hint = 1; }
    buffer->buffer = malloc(size_hint);
    if (!buffer->buffer)
    {
        // LCOV_EXCL_START
        buffer->size = 0;
        buffer->start = 0;
        buffer->end = 0;
        return 0;
        // LCOV_EXCL_STOP
    }
    buffer->size = size_hint;
    buffer->start = buffer->buffer;
    buffer->end = buffer->buffer;
    return 1;
}

// push the data onto the end of the buffer
//
// source is a pointer to the data and size is how many bytes to copy
//
// returns 0 on OOM error or a pointer to the copied data on success
void *
fifo_buffer_push(FifoBuffer *buffer, void *source, size_t size)
{
    assert(buffer);
    assert(buffer->buffer);
    assert(buffer->size);
    assert(buffer->start);
    assert(buffer->end);
    assert(source);
    assert(size);
    // check if there is space at `end` to store the data
    size_t post_size = buffer->size - (buffer->end - buffer->buffer);
    if (post_size < size)
    {
        // not enough space for the data at `end`, but there may be space 
        // before `start` we can use, so we need to check if the unused space
        // in the buffer has enough room
        size_t used_size = buffer->end - buffer->start;
        size_t unused_size = buffer->size - used_size;
        if (unused_size >= size)
        {
            // there is enough room in the entire buffer for our data, we'll
            // shift the data in the buffer to the start of the buffer
            if (buffer->start >= buffer->buffer + used_size)
            {
                void *result = memcpy(buffer->buffer, buffer->start, used_size);
                if (result != buffer->buffer){ return 0; }
            }
            else
            {
                void *result = memmove(buffer->buffer, buffer->start, used_size);
                if (result != buffer->buffer){ return 0; }
            }
            buffer->start = buffer->buffer;
            buffer->end = buffer->start + used_size;
        }
        else
        {
            // not enough room in the buffer, we'll need to just make the 
            // buffer bigger
            // TODO: some sort of heuristic/growth rate rather than getting 
            //       just enough memory
            size_t target_size = (buffer->end - buffer->buffer) + size;
            char *new_buffer = realloc(buffer->buffer, target_size);
            if (!new_buffer){ return 0; }
            if (new_buffer != buffer->buffer)
            {
                buffer->start = new_buffer + (buffer->start - buffer->buffer);
                buffer->end = new_buffer + (buffer->end - buffer->buffer);
                buffer->buffer = new_buffer;
            }
            buffer->size = target_size;
        }
    }
    // by this point we should have enough space at the end for the the data
    // we need to store
    post_size = buffer->size - (buffer->end - buffer->buffer);
    assert(post_size >= size);
    void *result = memcpy(buffer->end, source, size);
    if (!result){ return 0; }
    void *pushed_data = buffer->end;
    buffer->end += size;
    return pushed_data;
}

// returns a start and end pointer describing a range over the buffer that can
// be read from
//
// note that these pointers are only valid between any given fifo_buffer_push
// call
void
fifo_buffer_read(FifoBuffer *buffer, void **start, void **end)
{
    assert(buffer);
    assert(start);
    assert(end);
    *start = buffer->start;
    *end = buffer->end;
}

// returns truthy if the buffer is empty or falsey if it is not
int
fifo_buffer_is_empty(FifoBuffer *buffer)
{
    return buffer->start == buffer->end;
}

// removes `size` bytes worth of data from the front of the buffer
//
// note that there is no error checking, the buffer must contain at least 
// `size` amount of data
void
fifo_buffer_pop(FifoBuffer *buffer, size_t size)
{
    assert(buffer);
    buffer->start += size;
    assert(buffer->start <= buffer->end);
    // if the buffer is empty then we can reset the view to the start of the
    // buffer to save a potential memmove
    if (buffer->start == buffer->end && buffer->start != buffer->buffer)
    {
        buffer->start = buffer->buffer;
        buffer->end = buffer->buffer;
    }
}

// deallocate the buffer structure
//
// should be called for every buffer structure that is initialized
//
// may be called on a buffer that is already deleted
void
fifo_buffer_delete(FifoBuffer *buffer)
{
    assert(buffer);
    if (buffer->buffer)
    {
        free(buffer->buffer);
        buffer->buffer = 0;
    }
    buffer->size = 0;
    buffer->start = 0;
    buffer->end = 0;
}
