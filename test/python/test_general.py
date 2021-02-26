
from . import data

# pytest
import pytest
# python
import io
# woosh
import woosh


def tokenize_file_like(source):
    return list(woosh.tokenize(io.BytesIO(source)))
    
    
def tokenize_bytes(source):
    return list(woosh.tokenize(source))

    
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
def test_line_continuation(tokenize, newline):
    tokens = tokenize(f'xx\\{newline}yy'.encode('utf-8'))
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
