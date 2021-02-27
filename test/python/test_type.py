
# pytest
import pytest
# python
import weakref
# woosh
import woosh


def test_weakref():
    type = woosh.Type('A', 100)
    weak_type = weakref.ref(type)
    del type
    assert weak_type() is None
    
    
@pytest.mark.parametrize('type, name', [
    (woosh.COMMENT, 'COMMENT'),
    (woosh.DEDENT, 'DEDENT'),
    (woosh.ENCODING, 'ENCODING'),
    (woosh.EOF, 'EOF'),
    (woosh.ERROR, 'ERROR'),
    (woosh.INDENT, 'INDENT'),
    (woosh.NAME, 'NAME'),
    (woosh.NEWLINE, 'NEWLINE'),
    (woosh.NUMBER, 'NUMBER'),
    (woosh.OP, 'OP'),
    (woosh.STRING, 'STRING'),
])
def test_name(type, name):
    assert type.name == name
    
    
@pytest.mark.parametrize('type, value', [
    (woosh.COMMENT, 7),
    (woosh.DEDENT, 3),
    (woosh.ENCODING, 10),
    (woosh.EOF, 8),
    (woosh.ERROR, 9),
    (woosh.INDENT, 2),
    (woosh.NAME, 4),
    (woosh.NEWLINE, 0),
    (woosh.NUMBER, 5),
    (woosh.OP, 1),
    (woosh.STRING, 6),
])
def test_value(type, value):
    assert type.value == value

    
@pytest.mark.parametrize('type, name', [
    (woosh.COMMENT, 'COMMENT'),
    (woosh.DEDENT, 'DEDENT'),
    (woosh.ENCODING, 'ENCODING'),
    (woosh.EOF, 'EOF'),
    (woosh.ERROR, 'ERROR'),
    (woosh.INDENT, 'INDENT'),
    (woosh.NAME, 'NAME'),
    (woosh.NEWLINE, 'NEWLINE'),
    (woosh.NUMBER, 'NUMBER'),
    (woosh.OP, 'OP'),
    (woosh.STRING, 'STRING'),
])
def test_repr(type, name):
    assert repr(type) == name

    
def test_new():
    with pytest.raises(TypeError):
        woosh.Type()
        
    with pytest.raises(TypeError):
        woosh.Type('A', 100, None)
        
    with pytest.raises(TypeError):
        woosh.Type(name='A', value=100)

    with pytest.raises(TypeError) as exinfo:
        woosh.Type(None, 100)
    assert exinfo.value.args[0] == f'name must be str'
    
    with pytest.raises(TypeError) as exinfo:
        woosh.Type('A', None)
    assert exinfo.value.args[0] == f'value must be int'
    
    with pytest.raises(ValueError) as exinfo:
        woosh.Type('A', -1)
    assert exinfo.value.args[0] == f'value must be between 0 and 255'
    
    with pytest.raises(ValueError) as exinfo:
        woosh.Type('A', 256)
    assert exinfo.value.args[0] == f'value must be between 0 and 255'
    
    
def test_cannot_subclass():
    with pytest.raises(TypeError):
        class MyType(woosh.Type):
            pass

            
def test_equality():
    a = woosh.Type('A', 0)
    b = woosh.Type('B', 0)
    assert a == b
    assert not (a != b)

    b = woosh.Type('A', 1)
    assert not (a == b)
    assert a != b

    
def test_non_equality_operators():
    a = woosh.Type('A', 0)
    b = woosh.Type('B', 0)
    
    with pytest.raises(TypeError):
        a > b
    with pytest.raises(TypeError):
        a >= b
    with pytest.raises(TypeError):
        a < b
    with pytest.raises(TypeError):
        a <= b
