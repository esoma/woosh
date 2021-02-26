
import data

# pytest
import pytest
# python
import io
# woosh
import woosh


def tokenize(source):
    return list(woosh.tokenize(io.BytesIO(source)))
    
    
@pytest.mark.parametrize('literal', data.VALID_STRING_LITERALS)
def test_valid_string_literal(literal):
    tokens = tokenize(literal.encode('utf-8'))
    end_line = literal.count('\n') + 1
    end_column = len(literal.split('\n')[-1])
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.STRING, literal, 1, 0, end_line, end_column),
        woosh.Token(woosh.NEWLINE, '', end_line, end_column, end_line, end_column),
        woosh.Token(woosh.EOF, '', end_line, end_column, end_line, end_column),
    ]
    assert tokens == expected

    
@pytest.mark.parametrize('literal, error', data.INVALID_STRING_LITERALS)
def test_invalid_string_literal(literal, error):
    tokens = tokenize(literal.encode('utf-8'))
    end_column = len(error.split('\n')[-1])
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, error, 1, 0, 1, end_column),
    ]
    assert tokens == expected
