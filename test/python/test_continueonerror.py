
from . import data

# pytest
import pytest
# python
import io
# woosh
import woosh


def tokenize_file_like(source):
    return list(woosh.tokenize(io.BytesIO(source), continue_on_error=True))
    

def tokenize_bytes(source):
    return list(woosh.tokenize(source, continue_on_error=True))
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('quote', data.ONELINE_STRING_QUOTES)
def test_unterminated_one_line_string(tokenize, quote):
    tokens = tokenize(f'{quote}hello\nx'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, f'{quote}hello', 1, 0, 1, 6),
        woosh.Token(woosh.NAME, f'x', 2, 0, 2, 1),
        woosh.Token(woosh.NEWLINE, '', 2, 1, 2, 1),
        woosh.Token(woosh.EOF, '', 2, 1, 2, 1),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('quote', data.STRING_QUOTES)
def test_unterminated_string(tokenize, quote):
    tokens = tokenize(f'{quote}hello'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, f'{quote}hello', 1, 0, 1, len(quote) + 5),
        woosh.Token(woosh.NEWLINE, '', 1, len(quote) + 5, 1, len(quote) + 5),
        woosh.Token(woosh.EOF, '', 1, len(quote) + 5, 1, len(quote) + 5),
    ]
    assert tokens == expected
    

@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('quote', data.STRING_QUOTES)
def test_byte_string_unicode_character(tokenize, quote):
    tokens = tokenize(f'b{quote}abcü123{quote}'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, f'b{quote}abc', 1, 0, 1, len(quote) + 4),
        woosh.Token(woosh.NAME, 'ü123', 1, len(quote) + 4, 1, len(quote) + 8),
        woosh.Token(woosh.ERROR, quote, 1, len(quote) + 8, 1, len(quote) * 2 + 8),
        woosh.Token(woosh.NEWLINE, '', 1, len(quote) * 2 + 8, 1, len(quote) * 2 + 8),
        woosh.Token(woosh.EOF, '', 1, len(quote) * 2 + 8, 1, len(quote) * 2 + 8),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_name_non_starter(tokenize):
    tokens = tokenize(f'yin☯yang'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'yin', 1, 0, 1, 3),
        woosh.Token(woosh.ERROR, '☯', 1, 3, 1, 4),
        woosh.Token(woosh.NAME, 'yang', 1, 4, 1, 8),
        woosh.Token(woosh.NEWLINE, '', 1, 8, 1, 8),
        woosh.Token(woosh.EOF, '', 1, 8, 1, 8),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('sigil',
    data.BINARY_SIGILS +
    data.OCTAL_SIGILS +
    data.HEX_SIGILS
)
def test_incomplete_sigil_number(tokenize, sigil):
    tokens = tokenize(f'hello 0{sigil} world'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'hello', 1, 0, 1, 5),
        woosh.Token(woosh.ERROR, f'0{sigil}', 1, 6, 1, 7 + len(sigil)),
        woosh.Token(woosh.NAME, 'world', 1, 8 + len(sigil), 1, 13 + len(sigil)),
        woosh.Token(woosh.NEWLINE, '', 1, 13 + len(sigil), 1, 13 + len(sigil)),
        woosh.Token(woosh.EOF, '', 1, 13 + len(sigil), 1, 13 + len(sigil)),
    ]
    assert tokens == expected

    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('number',
    [f'0{sigil}0'
     for sigil in data.BINARY_SIGILS + data.OCTAL_SIGILS + data.HEX_SIGILS] +
    ['0', '10']
)
def test_incomplete_sigil_number(tokenize, number):
    tokens = tokenize(f'hello {number}_ world'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'hello', 1, 0, 1, 5),
        woosh.Token(woosh.ERROR, f'{number}_', 1, 6, 1, 7 + len(number)),
        woosh.Token(woosh.NAME, 'world', 1, 8 + len(number), 1, 13 + len(number)),
        woosh.Token(woosh.NEWLINE, '', 1, 13 + len(number), 1, 13 + len(number)),
        woosh.Token(woosh.EOF, '', 1, 13 + len(number), 1, 13 + len(number)),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_double_zero(tokenize):
    tokens = tokenize(f'hello 00123 world'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'hello', 1, 0, 1, 5),
        woosh.Token(woosh.ERROR, '00', 1, 6, 1, 8),
        woosh.Token(woosh.NUMBER, '123', 1, 8, 1, 11),
        woosh.Token(woosh.NAME, 'world', 1, 12, 1, 17),
        woosh.Token(woosh.NEWLINE, '', 1, 17, 1, 17),
        woosh.Token(woosh.EOF, '', 1, 17, 1, 17),
    ]
    assert tokens == expected
    

@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('open,close,expected', [
    ('(', ']', ')'), ('(', '}', ')'),
    ('[', ')', ']'), ('[', '}', ']'),
    ('{', ')', '}'), ('{', ']', '}'),
])
def test_mismatched_group(tokenize, open, close, expected):
    tokens = tokenize(f'hello {open}{open}middle{close} world'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'hello', 1, 0, 1, 5),
        woosh.Token(woosh.OP, open, 1, 6, 1, 7),
        woosh.Token(woosh.OP, open, 1, 7, 1, 8),
        woosh.Token(woosh.NAME, 'middle', 1, 8, 1, 14),
        woosh.Token(woosh.ERROR, close, 1, 14, 1, 15),
        woosh.Token(woosh.NAME, 'world', 1, 16, 1, 21),
        woosh.Token(woosh.ERROR, f'unexpected end of file, expected \'{expected}\'', 1, 21, 1, 21),
        woosh.Token(woosh.ERROR, f'unexpected end of file, expected \'{expected}\'', 1, 21, 1, 21),
        woosh.Token(woosh.NEWLINE, '', 1, 21, 1, 21),
        woosh.Token(woosh.EOF, '', 1, 21, 1, 21),
    ]
    assert tokens == expected

    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_mismatched_dedent(tokenize):
    tokens = tokenize(f'''
    indent
  dedent
    '''.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.INDENT, '    ', 2, 0, 2, 4),
        woosh.Token(woosh.NAME, 'indent', 2, 4, 2, 10),
        woosh.Token(woosh.NEWLINE, '\n', 2, 10, 3, 0),
        woosh.Token(woosh.ERROR, '  ', 3, 0, 3, 2),
        woosh.Token(woosh.NAME, 'dedent', 3, 2, 3, 8),
        woosh.Token(woosh.NEWLINE, '\n', 3, 8, 4, 0),
        woosh.Token(woosh.DEDENT, '', 4, 4, 4, 4),
        woosh.Token(woosh.EOF, '', 4, 4, 4, 4),
    ]
    assert tokens == expected
