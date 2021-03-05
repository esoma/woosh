
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


# https://bugs.python.org/issue40661
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_bpo_40661(tokenize):
    tokens = tokenize('import äˆ ð£„¯ð¢·žð±‹á”€ð””ð‘©±å®ä±¬ð©¾\nð—¶½'.encode('utf-8'))
    assert(tokens == [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'import', 1, 0, 1, 6),
        woosh.Token(woosh.NAME, 'äˆ', 1, 7, 1, 9),
        woosh.Token(woosh.NAME, 'ð', 1, 10, 1, 11),
        woosh.Token(woosh.ERROR, '£', 1, 11, 1, 12),
    ])
    
    
# https://github.com/psf/black/issues/970
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_black_970(tokenize):
    tokens = tokenize('pass #\r#\n'.encode('utf-8'))
    assert(tokens == [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'pass', 1, 0, 1, 4),
        woosh.Token(woosh.COMMENT, '#\r#', 1, 5, 1, 8),
        woosh.Token(woosh.NEWLINE, '\n', 1, 8, 2, 0),
        woosh.Token(woosh.EOF, '', 2, 0, 2, 0),
    ])


# https://github.com/psf/black/issues/1012
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_black_1012(tokenize):
    tokens = tokenize('\\'.encode('utf-8'))
    assert(tokens == [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NEWLINE, '', 1, 1, 1, 1),
        woosh.Token(woosh.EOF, '', 1, 1, 1, 1),
    ])
