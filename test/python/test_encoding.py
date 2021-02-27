
# pytest
import pytest
# python
import io
# woosh
import woosh


UTF8_BOM = b'\xEF\xBB\xBF'


def tokenize_file_like(source):
    return list(woosh.tokenize(io.BytesIO(source)))
    
    
def tokenize_bytes(source):
    return list(woosh.tokenize(source))
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('structure', [
    '# coding={encoding}',
    '# -*- coding: {encoding} -*-',
    '# vim: set fileencoding={encoding} :'
])
@pytest.mark.parametrize('encoding', [
    'ascii',
    'ASCII',
    'utf-8',
    'UTF-8',
    'utf8',
    'UTF8',
    'latin-1',
    'LATIN-1',
    'iso-8859-15',
    'ISO-8859-15',
])
@pytest.mark.parametrize('newline', ['\n', '\r\n'])
def test_encoding_comment(tokenize, structure, encoding, newline):
    comment = structure.format(encoding=encoding)
    # encoding is on first line with no following line
    tokens = tokenize(comment.encode('utf8'))
    expected = [
        woosh.Token(woosh.ENCODING, encoding, 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, comment, 1, 0, 1, len(comment)),
        woosh.Token(woosh.NEWLINE, '', 1, len(comment), 1, len(comment)),
        woosh.Token(woosh.EOF, '', 1, len(comment), 1, len(comment)),
    ]
    assert tokens == expected
    # encoding is on first line with following empty line
    tokens = tokenize(f'{comment}{newline}'.encode('utf8'))
    expected = [
        woosh.Token(woosh.ENCODING, encoding, 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, comment, 1, 0, 1, len(comment)),
        woosh.Token(woosh.NEWLINE, '', 2, 0, 2, 0),
        woosh.Token(woosh.EOF, '', 2, 0, 2, 0),
    ]
    assert tokens == expected
    # encoding is on second line with no following line
    tokens = tokenize(f'{newline}{comment}'.encode('utf8'))
    expected = [
        woosh.Token(woosh.ENCODING, encoding, 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, comment, 2, 0, 2, len(comment)),
        woosh.Token(woosh.NEWLINE, '', 2, len(comment), 2, len(comment)),
        woosh.Token(woosh.EOF, '', 2, len(comment), 2, len(comment)),
    ]
    assert tokens == expected
    # encoding is on second line with following empty line
    tokens = tokenize(f'{newline}{comment}{newline}'.encode('utf8'))
    expected = [
        woosh.Token(woosh.ENCODING, encoding, 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, comment, 2, 0, 2, len(comment)),
        woosh.Token(woosh.NEWLINE, '', 3, 0, 3, 0),
        woosh.Token(woosh.EOF, '', 3, 0, 3, 0),
    ]
    assert tokens == expected
    # encoding is on third line
    tokens = tokenize(f'{newline}{newline}{comment}'.encode('utf8'))
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, comment, 3, 0, 3, len(comment)),
        woosh.Token(woosh.NEWLINE, '', 3, len(comment), 3, len(comment)),
        woosh.Token(woosh.EOF, '', 3, len(comment), 3, len(comment)),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_invalid_encoding_comment(tokenize):
    tokens = tokenize('# coding=invalid'.encode('utf-8'))
    expected = [
        woosh.Token(woosh.ERROR, "invalid encoding: b'invalid'", 1, 0, 1, 0),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test_utf8_bom_encoding(tokenize):
    tokens = tokenize(UTF8_BOM)
    expected = [
        woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
        woosh.Token(woosh.NEWLINE, '', 1, 0, 1, 0),
        woosh.Token(woosh.EOF, '', 1, 0, 1, 0),
    ]
    assert tokens == expected
    
    
@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('encoding', [
    'ascii',
    'latin-1',
    'iso-8859-15',
])
def test_utf8_bom_encoding_non_utf8_comment_encoding(tokenize, encoding):
    source = UTF8_BOM + f'# coding={encoding}'.encode('utf-8')
    tokens = tokenize(source)
    expected = [
        woosh.Token(woosh.ERROR, f"encoding comment '{encoding}' does not match BOM (utf-8)", 1, 0, 1, 0),
    ]
    assert tokens == expected


@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
@pytest.mark.parametrize('encoding', [
    'utf-8',
    'UTF-8',
    'utf8',
    'UTF8',
])
@pytest.mark.parametrize('pre_space', [' ', '\f', '\t'])
@pytest.mark.parametrize('space_count', [0, 1, 5])
def test_utf8_bom_encoding_utf8_comment_encoding(
    tokenize,
    encoding,
    pre_space,
    space_count
):
    comment = f'#{pre_space * space_count}coding={encoding}'
    source = UTF8_BOM + comment.encode('utf-8')
    tokens = tokenize(source)
    expected = [
        woosh.Token(woosh.ENCODING, encoding, 1, 0, 1, 0),
        woosh.Token(woosh.COMMENT, comment, 1, 0, 1, len(comment)),
        woosh.Token(woosh.NEWLINE, '', 1, len(comment), 1, len(comment)),
        woosh.Token(woosh.EOF, '', 1, len(comment), 1, len(comment)),
    ]
    assert tokens == expected
