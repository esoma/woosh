
import data

# pytest
import pytest
# python
import gc
import io
import weakref
# woosh
import woosh


def tokenize(source):
    return list(woosh.tokenize(io.BytesIO(source)))


def test_gc_weakref():
    tokenizer = woosh.tokenize(io.BytesIO(b'hello world'))
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

    
def test_empty() -> None:
    tokens = tokenize(''.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NEWLINE, '', 1, 0, 1, 0),
        woosh.Token(woosh.EOF, '', 1, 0, 1, 0),
    ]
    assert tokens == expected
    
    
def test_null_byte() -> None:
    tokens = tokenize(b'\x00')
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, '\x00', 1, 0, 1, 1),
    ]
    assert tokens == expected

@pytest.mark.parametrize('newline', data.NEWLINES)
def test_line_continuation(newline) -> None:
    tokens = tokenize(f'xx\\{newline}yy'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'xx', 1, 0, 1, 2),
        woosh.Token(woosh.NAME, 'yy', 2, 0, 2, 2),
        woosh.Token(woosh.NEWLINE, '', 2, 2, 2, 2),
        woosh.Token(woosh.EOF, '', 2, 2, 2, 2),
    ]
    assert tokens == expected

@pytest.mark.parametrize('literal', [
    '# hello',
    '# hello # hello',
    '# line continuation does not continue \\',
])
@pytest.mark.parametrize('newline', data.OPTIONAL_NEWLINES)
def test_comment(literal: str, newline: str) -> None:
    tokens = tokenize(f'{literal}{newline}'.encode('utf-8'))
    end_comment = newline_end = 1, len(literal)
    if newline:
        newline_end = 2, 0
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, literal, 1, 0, *end_comment),
        woosh.Token(woosh.NEWLINE, newline, *end_comment, *newline_end),
        woosh.Token(woosh.EOF, '', *newline_end, *newline_end),
    ]
    assert tokens == expected
