
import data

# pytest
import pytest
# python
import io
import textwrap
# woosh
import woosh


def tokenize_file_like(source):
    return list(woosh.tokenize(io.BytesIO(source)))
    

def tokenize_bytes(source):
    return list(woosh.tokenize(source))
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('indent', [
    ' ',
    '  ',
    '    ',
    '\t',
    '    \t',
])
@pytest.mark.parametrize('newline', data.NEWLINES)
def test_indentation(tokenize, indent, newline):
    tokens = tokenize(textwrap.dedent(f"""
    zero
    {indent}one
    {indent}{indent}two
    {indent}{indent}{indent}three

    {indent}{indent}{indent}continue_three

    {indent}{indent}back_to_two
    back_to_zero
    """).replace('\n', newline).encode('utf-8'))
    indent_two = indent * 2
    indent_three = indent * 3
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'zero', 2, 0, 2, 4),
        woosh.Token(woosh.NEWLINE, newline, 2, 4, 3, 0),
        woosh.Token(woosh.INDENT, indent, 3, 0, 3, len(indent)),
        woosh.Token(woosh.NAME, 'one', 3, len(indent), 3, len(indent) + 3),
        woosh.Token(woosh.NEWLINE, newline, 3, len(indent) + 3, 4, 0),
        woosh.Token(woosh.INDENT, indent_two, 4, 0, 4, len(indent_two)),
        woosh.Token(woosh.NAME, 'two', 4, len(indent_two), 4, len(indent_two) + 3),
        woosh.Token(woosh.NEWLINE, newline, 4, len(indent_two) + 3, 5, 0),
        woosh.Token(woosh.INDENT, indent_three, 5, 0, 5, len(indent_three)),
        woosh.Token(woosh.NAME, 'three', 5, len(indent_three), 5, len(indent_three) + 5),
        woosh.Token(woosh.NEWLINE, newline, 5, len(indent_three) + 5, 6, 0),
        woosh.Token(woosh.NAME, 'continue_three', 7, len(indent_three), 7, len(indent_three) + 14),
        woosh.Token(woosh.NEWLINE, newline, 7, len(indent_three) + 14, 8, 0),
        woosh.Token(woosh.DEDENT, indent_two, 9, 0, 9, len(indent_two)),
        woosh.Token(woosh.NAME, 'back_to_two', 9, len(indent_two), 9, len(indent_two) + 11),
        woosh.Token(woosh.NEWLINE, newline, 9, len(indent_two) + 11, 10, 0),
        woosh.Token(woosh.DEDENT, '', 10, 0, 10, 0),
        woosh.Token(woosh.DEDENT, '', 10, 0, 10, 0),
        woosh.Token(woosh.NAME, 'back_to_zero', 10, 0, 10, 12),
        woosh.Token(woosh.NEWLINE, newline, 10, 12, 11, 0),
        woosh.Token(woosh.EOF, '', 11, 0, 11, 0),
    ]
    assert tokens == expected
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('indent', [
    ' ',
    '  ',
    '    ',
    '\t',
    '    \t',
])
@pytest.mark.parametrize('newline', data.NEWLINES)
def test_indentation_continuation(tokenize, indent, newline) -> None:
    tokens = tokenize(textwrap.dedent(f"""
    one\\
    {indent}two
    """).replace('\n', newline).encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'one', 2, 0, 2, 3),
        woosh.Token(woosh.NAME, 'two', 3, len(indent), 3, len(indent) + 3),
        woosh.Token(woosh.NEWLINE, newline, 3, len(indent) + 3, 4, 0),
        woosh.Token(woosh.EOF, '', 4, 0, 4, 0),
    ]
    assert tokens == expected


@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('indent', [
    ' ',
    '  ',
    '    ',
    '\t',
    '    \t',
])
@pytest.mark.parametrize('newline', data.NEWLINES)
@pytest.mark.parametrize('open, close', [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
])
def test_indentation_groups(tokenize, indent, newline, open, close):
    tokens = tokenize(textwrap.dedent(f"""
    {open}
    {indent}foo
    {close}
    """).replace('\n', newline).encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.OP, open, 2, 0, 2, 1),
        woosh.Token(woosh.NAME, 'foo', 3, len(indent), 3, len(indent) + 3),
        woosh.Token(woosh.OP, close, 4, 0, 4, 1),
        woosh.Token(woosh.NEWLINE, newline, 4, 1, 5, 0),
        woosh.Token(woosh.EOF, '', 5, 0, 5, 0),
    ]
    assert tokens == expected


@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('indent', [
    ' ',
    '  ',
    '    ',
    '\t',
    '    \t',
])
@pytest.mark.parametrize('newline', data.NEWLINES)
def test_indentation_reset(tokenize, indent, newline):
    tokens = tokenize(textwrap.dedent(f"""
    zero
    {indent}one
    {indent}{indent}two
    {indent}{indent}{indent}three

    """).replace('\n', newline).encode('utf-8'))
    indent_two = indent * 2
    indent_three = indent * 3
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NAME, 'zero', 2, 0, 2, 4),
        woosh.Token(woosh.NEWLINE, newline, 2, 4, 3, 0),
        woosh.Token(woosh.INDENT, indent, 3, 0, 3, len(indent)),
        woosh.Token(woosh.NAME, 'one', 3, len(indent), 3, len(indent) + 3),
        woosh.Token(woosh.NEWLINE, newline, 3, len(indent) + 3, 4, 0),
        woosh.Token(woosh.INDENT, indent_two, 4, 0, 4, len(indent_two)),
        woosh.Token(woosh.NAME, 'two', 4, len(indent_two), 4, len(indent_two) + 3),
        woosh.Token(woosh.NEWLINE, newline, 4, len(indent_two) + 3, 5, 0),
        woosh.Token(woosh.INDENT, indent_three, 5, 0, 5, len(indent_three)),
        woosh.Token(woosh.NAME, 'three', 5, len(indent_three), 5, len(indent_three) + 5),
        woosh.Token(woosh.NEWLINE, newline, 5, len(indent_three) + 5, 6, 0),
        woosh.Token(woosh.DEDENT, '', 7, 0, 7, 0),
        woosh.Token(woosh.DEDENT, '', 7, 0, 7, 0),
        woosh.Token(woosh.DEDENT, '', 7, 0, 7, 0),
        woosh.Token(woosh.EOF, '', 7, 0, 7, 0),
    ]
    assert tokens == expected


@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_tab_size(tokenize):
    tokens = tokenize(textwrap.dedent(f"""
            spaces
    \ttab
    """).encode('utf-8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.INDENT, '        ', 2, 0, 2, 8),
        woosh.Token(woosh.NAME, 'spaces', 2, 8, 2, 14),
        woosh.Token(woosh.NEWLINE, '\n', 2, 14, 3, 0),
        woosh.Token(woosh.NAME, 'tab', 3, 1, 3, 4),
        woosh.Token(woosh.NEWLINE, '\n', 3, 4, 4, 0),
        woosh.Token(woosh.DEDENT, '', 4, 0, 4, 0),
        woosh.Token(woosh.EOF, '', 4, 0, 4, 0),
    ]
    assert tokens == expected
