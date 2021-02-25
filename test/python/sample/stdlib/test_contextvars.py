
# python
import io
import pathlib
# pytest
import pytest
# woosh
import woosh

def tokenize_file_like(source):
    return list(woosh.tokenize(io.BytesIO(source)))

def tokenize_bytes(source):
    return list(woosh.tokenize(source))

SAMPLE_DIR = pathlib.Path(__file__).parent.absolute() / '../../' / '../../' / 'sample'

@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test(tokenize):
    with open(SAMPLE_DIR / 'stdlib/contextvars.py', 'rb') as f:
        tokens = tokenize(f.read())
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.NAME, 'from', 1, 0, 1, 4),
woosh.Token(woosh.NAME, '_contextvars', 1, 5, 1, 17),
woosh.Token(woosh.NAME, 'import', 1, 18, 1, 24),
woosh.Token(woosh.NAME, 'Context', 1, 25, 1, 32),
woosh.Token(woosh.OP, ',', 1, 32, 1, 33),
woosh.Token(woosh.NAME, 'ContextVar', 1, 34, 1, 44),
woosh.Token(woosh.OP, ',', 1, 44, 1, 45),
woosh.Token(woosh.NAME, 'Token', 1, 46, 1, 51),
woosh.Token(woosh.OP, ',', 1, 51, 1, 52),
woosh.Token(woosh.NAME, 'copy_context', 1, 53, 1, 65),
woosh.Token(woosh.NEWLINE, '\r\n', 1, 65, 2, 0),
woosh.Token(woosh.NAME, '__all__', 4, 0, 4, 7),
woosh.Token(woosh.OP, '=', 4, 8, 4, 9),
woosh.Token(woosh.OP, '(', 4, 10, 4, 11),
woosh.Token(woosh.STRING, "'Context'", 4, 11, 4, 20),
woosh.Token(woosh.OP, ',', 4, 20, 4, 21),
woosh.Token(woosh.STRING, "'ContextVar'", 4, 22, 4, 34),
woosh.Token(woosh.OP, ',', 4, 34, 4, 35),
woosh.Token(woosh.STRING, "'Token'", 4, 36, 4, 43),
woosh.Token(woosh.OP, ',', 4, 43, 4, 44),
woosh.Token(woosh.STRING, "'copy_context'", 4, 45, 4, 59),
woosh.Token(woosh.OP, ')', 4, 59, 4, 60),
woosh.Token(woosh.NEWLINE, '\r\n', 4, 60, 5, 0),
woosh.Token(woosh.EOF, '', 5, 0, 5, 0),
]
