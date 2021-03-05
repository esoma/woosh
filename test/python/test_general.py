
from . import data

# pytest
import pytest
# python
import io
# woosh
import woosh


def tokenize_file_like(source, continue_on_error=False):
    return list(woosh.tokenize(
        io.BytesIO(source),
        continue_on_error=continue_on_error
    ))
    
    
def tokenize_bytes(source, continue_on_error=False):
    return list(woosh.tokenize(source, continue_on_error=continue_on_error))
    
    
def test_invalid_args():
    with pytest.raises(TypeError):
        woosh.tokenize()
    
    with pytest.raises(TypeError):
        woosh.tokenize(b'', True)
        
    with pytest.raises(TypeError):
        woosh.tokenize(source=b'', continue_on_error=True)
    

@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_empty(tokenize):
    tokens = tokenize(''.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NEWLINE, '', 1, 0, 1, 0),
        woosh.Token(woosh.EOF, '', 1, 0, 1, 0),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_null_byte(tokenize):
    tokens = tokenize(b'\x00')
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, '\x00', 1, 0, 1, 1),
    ]
    assert tokens == expected

    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('newline', data.NEWLINES)
@pytest.mark.parametrize('post_whitespace', ['', ' ', '\t'])
def test_line_continuation(tokenize, newline, post_whitespace):
    tokens = tokenize(f'xx\\{post_whitespace}{newline}yy'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'xx', 1, 0, 1, 2),
        woosh.Token(woosh.NAME, 'yy', 2, 0, 2, 2),
        woosh.Token(woosh.NEWLINE, '', 2, 2, 2, 2),
        woosh.Token(woosh.EOF, '', 2, 2, 2, 2),
    ]
    assert tokens == expected

    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('literal', [
    '# hello',
    '# hello # hello',
    '# line continuation does not continue \\',
])
@pytest.mark.parametrize('newline', data.OPTIONAL_NEWLINES)
def test_comment(tokenize, literal, newline):
    tokens = tokenize(f'{literal}{newline}'.encode('utf-8'))
    end_comment = newline_end = 1, len(literal)
    if newline:
        newline_end = 2, 0
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, literal, 1, 0, *end_comment),
        woosh.Token(woosh.NEWLINE, '', *newline_end, *newline_end),
        woosh.Token(woosh.EOF, '', *newline_end, *newline_end),
    ]
    assert tokens == expected

@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_set_module_token_does_not_affect_output(tokenize):
    COMMENT = woosh.COMMENT
    DEDENT = woosh.DEDENT
    ENCODING = woosh.ENCODING
    EOF = woosh.EOF
    ERROR = woosh.ERROR
    INDENT = woosh.INDENT
    NAME = woosh.NAME
    NEWLINE = woosh.NEWLINE
    NUMBER = woosh.NUMBER
    OP = woosh.OP
    STRING = woosh.STRING
    test_type = woosh.Type('TEST', 0)
    try:
        woosh.COMMENT = test_type
        woosh.DEDENT = test_type
        woosh.ENCODING = test_type
        woosh.EOF = test_type
        woosh.ERROR = test_type
        woosh.INDENT = test_type
        woosh.NAME = test_type
        woosh.NEWLINE = test_type
        woosh.NUMBER = test_type
        woosh.OP = test_type
        woosh.STRING = test_type
        
        tokens = tokenize("""
        # comment
        'indent' name 0  
+ ☯""".encode('utf-8'), continue_on_error=True)
        assert tokens == [
            woosh.Token(ENCODING, 'utf-8', 1, 0, 1, 0),
            woosh.Token(COMMENT, '# comment', 2, 8, 2, 17),
            woosh.Token(INDENT, '        ', 3, 0, 3, 8),
            woosh.Token(STRING, "'indent'", 3, 8, 3, 16),
            woosh.Token(NAME, 'name', 3, 17, 3, 21),
            woosh.Token(NUMBER, '0', 3, 22, 3, 23),
            woosh.Token(NEWLINE, '\n', 3, 25, 4, 0),
            woosh.Token(DEDENT, '', 4, 0, 4, 0),
            woosh.Token(OP, '+', 4, 0, 4, 1),
            woosh.Token(ERROR, '☯', 4, 2, 4, 3),
            woosh.Token(NEWLINE, '', 4, 3, 4, 3),
            woosh.Token(EOF, '', 4, 3, 4, 3),
        ]
        
    finally:
        woosh.COMMENT = COMMENT
        woosh.DEDENT = DEDENT
        woosh.ENCODING = ENCODING
        woosh.EOF = EOF
        woosh.ERROR = ERROR
        woosh.INDENT = INDENT
        woosh.NAME = NAME
        woosh.NEWLINE = NEWLINE
        woosh.NUMBER = NUMBER
        woosh.OP = OP
        woosh.STRING = STRING
    