
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
        
    
@pytest.mark.parametrize('type', [
    woosh.COMMENT,
    woosh.DEDENT,
    woosh.ENCODING,
    woosh.EOF,
    woosh.ERROR,
    woosh.INDENT,
    woosh.NAME,
    woosh.NEWLINE,
    woosh.NUMBER,
    woosh.OP,
    woosh.STRING,
])
@pytest.mark.parametrize('value', [
    '',
    'hello',
    '"hello"',
    '\'hello\'',
])
@pytest.mark.parametrize('start_line', [0, 1, 100])
@pytest.mark.parametrize('start_column', [0, 1, 100])
@pytest.mark.parametrize('end_line', [0, 1, 100])
@pytest.mark.parametrize('end_column', [0, 1, 100])
def test_repr(type, value, start_line, start_column, end_line, end_column):
    token = woosh.Token(
        type, value,
        start_line, start_column,
        end_line, end_column
    )
    expected_repr = (
        f'<Token {type!r} {value!r} '
        f'{start_line!r}:{start_column!r}-{end_line!r}:{end_column!r}>'
    )
    assert repr(token) == expected_repr

    
def test_new_token():
    with pytest.raises(TypeError) as exinfo:
        woosh.Token(None, '', 0, 0, 0, 0)
    assert exinfo.value.args[0] == f'type must be woosh.Type'
    
    with pytest.raises(TypeError) as exinfo:
        woosh.Token(woosh.OP, None, 0, 0, 0, 0)
    assert exinfo.value.args[0] == f'value must be str'
    
    with pytest.raises(TypeError) as exinfo:
        woosh.Token(woosh.OP, '', None, 0, 0, 0)
    assert exinfo.value.args[0] == f'start_line must be int'
    
    with pytest.raises(TypeError) as exinfo:
        woosh.Token(woosh.OP, '', 0, None, 0, 0)
    assert exinfo.value.args[0] == f'start_column must be int'
    
    with pytest.raises(TypeError) as exinfo:
        woosh.Token(woosh.OP, '', 0, 0, None, 0)
    assert exinfo.value.args[0] == f'end_line must be int'
    
    with pytest.raises(TypeError) as exinfo:
        woosh.Token(woosh.OP, '', 0, 0, 0, None)
    assert exinfo.value.args[0] == f'end_column must be int'

    
def test_cannot_subclass_token():
    with pytest.raises(TypeError):
        class MyToken(woosh.Token):
            pass
            

def test_equality():
    a = woosh.Token(woosh.OP, '>', 0, 1, 2, 3)
    b = woosh.Token(woosh.OP, '>', 0, 1, 2, 3)
    assert a == b
    assert not (a != b)

    b = woosh.Token(woosh.EOF, '>', 0, 1, 2, 3)
    assert not (a == b)
    assert a != b
    
    b = woosh.Token(woosh.OP, '<', 0, 1, 2, 3)
    assert not (a == b)
    assert a != b
    
    b = woosh.Token(woosh.OP, '>', 100, 1, 2, 3)
    assert not (a == b)
    assert a != b
    
    b = woosh.Token(woosh.OP, '>', 0, 100, 2, 3)
    assert not (a == b)
    assert a != b
    
    b = woosh.Token(woosh.OP, '>', 0, 1, 100, 3)
    assert not (a == b)
    assert a != b
    
    b = woosh.Token(woosh.OP, '>', 0, 1, 2, 100)
    assert not (a == b)
    assert a != b


def test_non_equality_operators():
    a = woosh.Token(woosh.OP, '>', 0, 1, 2, 3)
    b = woosh.Token(woosh.OP, '>', 0, 1, 2, 3)
    
    with pytest.raises(TypeError):
        a > b
    with pytest.raises(TypeError):
        a >= b
    with pytest.raises(TypeError):
        a < b
    with pytest.raises(TypeError):
        a <= b
