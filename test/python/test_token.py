
# pytest
import pytest
# woosh
import woosh

    
def tokenize(source):
    return list(woosh.tokenize(source))
    

@pytest.mark.parametrize('source, type', [
    (b'hello', woosh.NAME),
    (b'"hello"', woosh.STRING),
    (b'123', woosh.NUMBER),
    (b'>', woosh.OP),
])
def test_type(source, type):
    token = tokenize(source)[1]
    assert token.type == type
    
@pytest.mark.parametrize('source, value', [
    (b'hello', 'hello'),
    (b'"hello"', '"hello"'),
    (b'123', '123'),
    (b'>', '>'),
])
def test_value(source, value):
    token = tokenize(source)[1]
    assert token.value == value
    

@pytest.mark.parametrize('source, start_line', [
    (b'hello', 1),
    (b'\nhello', 2),
    (b'\n\nhello', 3),
    (b'"""\n"""', 1),
])
def test_start_line(source, start_line):
    token = tokenize(source)[1]
    assert token.start_line == start_line
    
    
@pytest.mark.parametrize('source, start_column', [
    (b'hello', 0),
    (b' hello', 1),
    (b'  hello', 2),
])
def test_start_column(source, start_column):
    tokens = tokenize(source)
    token = tokens[1]
    if token.type == woosh.INDENT:
        token = tokens[2]
    assert token.start_column == start_column
    
    
@pytest.mark.parametrize('source, end_line', [
    (b'hello', 1),
    (b'\nhello', 2),
    (b'\n\nhello', 3),
    (b'"""\n"""', 2),
])
def test_end_line(source, end_line):
    token = tokenize(source)[1]
    assert token.end_line == end_line
    
    
@pytest.mark.parametrize('source, end_column', [
    (b'hello', 5),
    (b' hello', 6),
    (b'  hello', 7),
])
def test_end_column(source, end_column):
    tokens = tokenize(source)
    token = tokens[1]
    if token.type == woosh.INDENT:
        token = tokens[2]
    assert token.end_column == end_column
    
    
def test_invalid_attribute():
    token = tokenize(b'hello')
    with pytest.raises(AttributeError):
        token.not_an_attribute
