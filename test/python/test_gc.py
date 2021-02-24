
# pytest
import pytest
# python
import gc
import io
import weakref
# woosh
import woosh


def test_no_cycle():
    tokenizer = woosh.tokenize(b'hello world')
    weak_tokenizer = weakref.ref(tokenizer)
    
    token = next(tokenizer)
    weak_token = weakref.ref(token)
    
    weak_type = weakref.ref(token.type)
    
    del token
    gc.collect()
    assert weak_token() is None
    assert weak_type() is not None
    
    token = next(tokenizer)
    
    del tokenizer
    gc.collect()
    assert weak_tokenizer() is None
    
    
def test_source_tokenizer_cycle():
    class CycleSource:
        def __init__(self):
            self.data = [b'', b'hello world']
        def tell(self):
            return 0
        def seek(self, index):
            pass
        def readline(self, bytes=0):
            try:
                return self.data.pop(0)
            except IndexError:
                return b''

    cycle_source = CycleSource()
    tokenizer = woosh.tokenize(cycle_source)
    cycle_source.tokenizer = tokenizer
    del cycle_source
    weak_tokenizer = weakref.ref(tokenizer)
    
    token = next(tokenizer)
    weak_token = weakref.ref(token)
    
    weak_type = weakref.ref(token.type)
    
    del token
    gc.collect()
    assert weak_token() is None
    assert weak_type() is not None
    
    token = next(tokenizer)
    
    del tokenizer
    gc.collect()
    assert weak_tokenizer() is None
    
    
def test_source_tokenizer_readline_cycle():
    class Source:
        def tell(self):
            return 0
        def seek(self, index):
            pass
            
    class CycleReadline:
        def __init__(self):
            self.data = [b'', b'hello world']
        def __call__(self, bytes=0):
            try:
                return self.data.pop(0)
            except IndexError:
                return b''
    source = Source()
    source.readline = CycleReadline()
    tokenizer = woosh.tokenize(source)
    source.readline.tokenizer = tokenizer
    del source
    weak_tokenizer = weakref.ref(tokenizer)
    
    token = next(tokenizer)
    weak_token = weakref.ref(token)
    
    weak_type = weakref.ref(token.type)
    
    del token
    gc.collect()
    assert weak_token() is None
    assert weak_type() is not None
    
    token = next(tokenizer)
    
    del tokenizer
    gc.collect()
    assert weak_tokenizer() is None
