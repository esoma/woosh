
# pytest
import pytest
# python
import io
# woosh
import woosh


def tokenize(source):
    return list(woosh.tokenize(io.BytesIO(source)))


@pytest.mark.parametrize('literal', [
    '+', '+=',
    '-', '-=', '->',
    '*', '*=',
    '**', '**=',
    '/', '/=',
    '//', '//=',
    '@', '@=',
    '%', '%=',
    '|', '|=',
    '^', '^=',
    '&', '&=',
    '.', '...',
    '=', '==',
    '~',
    '!=',
    ',',
    ':',
    ';',
])
def test_valid_operator(literal):
    tokens = tokenize(literal.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, literal, 1, 0, 1, len(literal)),
        woosh.Token(woosh.NEWLINE, '', 1, len(literal), 1, len(literal)),
        woosh.Token(woosh.EOF, '', 1, len(literal), 1, len(literal)),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('literal, expected', [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
])
def test_valid_operator_groups(literal: str, expected: str) -> None:
    tokens = tokenize(literal.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, literal, 1, 0, 1, len(literal)),
        woosh.Token(woosh.ERROR, f"unexpected end of file, expected '{expected}'", 1, len(literal), 1, len(literal)),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('literal', ['?', '!', '$', ')', ']', '}'])
def test_invalid_operator(literal: str) -> None:
    tokens = tokenize(literal.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.ERROR, literal, 1, 0, 1, len(literal)),
    ]
    assert tokens == expected
    
    
def test_two_dots() -> None:
    tokens = tokenize(b'..')
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, '.', 1, 0, 1, 1),
        woosh.Token(woosh.OP, '.', 1, 1, 1, 2),
        woosh.Token(woosh.NEWLINE, '', 1, 2, 1, 2),
        woosh.Token(woosh.EOF, '', 1, 2, 1, 2),
    ]
    assert tokens == expected
    
def test_four_dots() -> None:
    tokens = tokenize(b'....')
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, '...', 1, 0, 1, 3),
        woosh.Token(woosh.OP, '.', 1, 3, 1, 4),
        woosh.Token(woosh.NEWLINE, '', 1, 4, 1, 4),
        woosh.Token(woosh.EOF, '', 1, 4, 1, 4),
    ]
    assert tokens == expected
    
@pytest.mark.parametrize('character', ['*', '/', '='])
def test_double_and_one_operator(character: str) -> None:
    tokens = tokenize((character * 3).encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, character * 2, 1, 0, 1, 2),
        woosh.Token(woosh.OP, character, 1, 2, 1, 3),
        woosh.Token(woosh.NEWLINE, '', 1, 3, 1, 3),
        woosh.Token(woosh.EOF, '', 1, 3, 1, 3),
    ]
    assert tokens == expected


@pytest.mark.parametrize('open, close', [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
])
def test_balanced_open_close(open: str, close: str) -> None:
    tokens = tokenize(f'{open}{close}'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, open, 1, 0, 1, 1),
        woosh.Token(woosh.OP, close, 1, 1, 1, 2),
        woosh.Token(woosh.NEWLINE, '', 1, 2, 1, 2),
        woosh.Token(woosh.EOF, '', 1, 2, 1, 2),
    ]
    assert tokens == expected


@pytest.mark.parametrize('open, close', [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
])
def test_exceed_cpython_group_depth(open: str, close: str) -> None:
    # cpython has a maximum group nesting of 200, make sure we can exceed that
    MAX_GROUPS = 200 + 1
    tokens = tokenize((
        (open * MAX_GROUPS) +
        (close * MAX_GROUPS)
    ).encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        *(
            woosh.Token(woosh.OP, open, 1, i, 1, i + 1)
            for i in range(MAX_GROUPS)
        ),
        *(
            woosh.Token(woosh.OP, close, 1, i, 1, i + 1)
            for i in range(MAX_GROUPS, MAX_GROUPS * 2)
        ),
        woosh.Token(woosh.NEWLINE, '', 1, MAX_GROUPS * 2, 1, MAX_GROUPS * 2),
        woosh.Token(woosh.EOF, '', 1, MAX_GROUPS * 2, 1, MAX_GROUPS * 2),
    ]
    assert tokens == expected


@pytest.mark.parametrize('open,close', [
    ('(', ']'), ('(', '}'),
    ('[', ')'), ('[', '}'),
    ('{', ')'), ('{', ']'),
])
def test_different_open_close(open: str, close: str) -> None:
    tokens = tokenize(f'{open}{close}'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, open, 1, 0, 1, 1),
        woosh.Token(woosh.ERROR, close, 1, 1, 1, 2),
    ]
    assert tokens == expected
