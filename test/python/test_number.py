
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
@pytest.mark.parametrize(
    'literal',
    data.VALID_ZERO_LITERALS +
    data.VALID_NON_ZERO_DECIMAL_LITERALS +
    data.VALID_FLOAT_LITERALS +
    data.VALID_BINARY_LITERALS +
    data.VALID_OCTAL_LITERALS +
    data.VALID_HEX_LITERALS
)
def test_valid_number_literal(tokenize, literal):
    tokens = tokenize(literal.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NUMBER, literal, 1, 0, 1, len(literal)),
        woosh.Token(woosh.NEWLINE, '', 1, len(literal), 1, len(literal)),
        woosh.Token(woosh.EOF, '', 1, len(literal), 1, len(literal)),
    ]
    assert tokens == expected

    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize(
    'literal, error',
    data.INVALID_DECIMAL_LITERALS +
    data.INVALID_FLOAT_LITERALS +
    data.INVALID_BINARY_LITERALS +
    data.INVALID_OCTAL_LITERALS +
    data.INVALID_HEX_LITERALS
)
def test_invalid_number_literal(tokenize, literal, error):
    tokens = tokenize(literal.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, error, 1, 0, 1, len(error)),
    ]
    assert tokens == expected


@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize(
    'code, number',
    data.DECIMALS_SPLIT_BY_TOKEN +
    data.FLOATS_SPLIT_BY_TOKEN +
    data.BINARIES_SPLIT_BY_TOKEN +
    data.OCTAL_SPLIT_BY_TOKEN +
    data.HEX_SPLIT_BY_TOKEN
)
def test_number_split_by_token(tokenize, code, number):
    tokens = tokenize(code.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NUMBER, number, 1, 0, 1, len(number)),
    ]
    assert tokens[:2] == expected
