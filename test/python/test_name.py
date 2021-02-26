
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
@pytest.mark.parametrize('literal', data.VALID_NAME_LITERALS)
def test_valid_name_literal(tokenize, literal):
    tokens = tokenize(literal.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, literal, 1, 0, 1, len(literal)),
        woosh.Token(woosh.NEWLINE, '', 1, len(literal), 1, len(literal)),
        woosh.Token(woosh.EOF, '', 1, len(literal), 1, len(literal)),
    ]
    assert tokens == expected


@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize(
    'literal, error',
    data.INVALID_NAME_LITERALS
)
def test_invalid_name_literal(tokenize, literal, error):
    tokens = tokenize(literal.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, error, 1, 0, 1, len(error)),
    ]
    assert tokens == expected


@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('code, name', data.NAMES_SPLIT_BY_TOKEN)
def test_name_split_by_token(tokenize, code, name):
    tokens = tokenize(code.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, name, 1, 0, 1, len(name)),
    ]
    assert tokens[:2] == expected
