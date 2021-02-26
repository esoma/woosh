
# pytest
import pytest
# woosh
import woosh


@pytest.mark.parametrize('bad_source', [
    None,
    'hello world',
    5,
])
def test_incorrect_type(bad_source):
    with pytest.raises(TypeError):
        list(woosh.tokenize(bad_source))


def test_no_tell():
    class InvalidSource:
        def readline(self, size=-1):
            return b''
        def seek(self, value):
            pass
    with pytest.raises(TypeError):
        list(woosh.tokenize(InvalidSource()))
    

@pytest.mark.parametrize('error', [
    Exception('test'),
    AttributeError('test'),
    ValueError('test'),
])
def test_tell_error(error):
    class InvalidSource:
        def tell(self):
            raise error
        def readline(self, size=-1):
            return b''    
        def seek(self, value):
            pass
    with pytest.raises(type(error)) as exinfo:
        list(woosh.tokenize(InvalidSource()))
    assert exinfo.value is error
    

def test_no_readline():
    class InvalidSource:
        def tell(self):
            return 0 
        def seek(self, value):
            pass
    with pytest.raises(TypeError):
        list(woosh.tokenize(InvalidSource()))
        
        
@pytest.mark.parametrize('error', [
    Exception('test'),
    AttributeError('test'),
    ValueError('test'),
])
def test_readline_error(error):
    class InvalidSource:
        def tell(self):
            return 0
        def readline(self, size=-1):
            raise error    
        def seek(self, value):
            pass
    with pytest.raises(type(error)) as exinfo:
        list(woosh.tokenize(InvalidSource()))
    assert exinfo.value is error
    
    
@pytest.mark.parametrize('invalid', [
    'None',
    123,
    object(),
])
def test_readline_incorrect_type(invalid):
    class InvalidSource:
        def tell(self):
            return 0
        def readline(self, size=-1):
            return invalid
        def seek(self, value):
            pass
    with pytest.raises(TypeError) as exinfo:
        list(woosh.tokenize(InvalidSource()))
    
    
@pytest.mark.parametrize('weird', [
    '123',
    None,
    1,
    object()
])
def test_weird_readline(weird):
    class InvalidSource:
        def __init__(self):
            self.q = [b'123', weird]
        def tell(self):
            return 0
        def readline(self, size=-1):
            return self.q.pop(0)
        def seek(self, value):
            pass
    with pytest.raises(TypeError) as exinfo:
        list(woosh.tokenize(InvalidSource()))

    
def test_no_seek():
    class InvalidSource:
        def tell(self):
            return 0 
        def readline(self, size=-1):
            return b''    
    with pytest.raises(TypeError):
        list(woosh.tokenize(InvalidSource()))
        
        
@pytest.mark.parametrize('error', [
    Exception('test'),
    AttributeError('test'),
    ValueError('test'),
])
def test_seek_error(error):
    class InvalidSource:
        def tell(self):
            return 0
        def readline(self, size=-1):
            return b''    
        def seek(self, value):
            raise error
    with pytest.raises(type(error)) as exinfo:
        list(woosh.tokenize(InvalidSource()))
    assert exinfo.value is error
