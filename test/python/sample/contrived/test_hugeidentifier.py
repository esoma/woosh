
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
    with open(SAMPLE_DIR / 'contrived/hugeidentifier.py', 'rb') as f:
        tokens = tokenize(f.read())
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.NAME, 'abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123', 1, 0, 1, 720),
woosh.Token(woosh.NEWLINE, '', 1, 720, 1, 720),
woosh.Token(woosh.EOF, '', 1, 720, 1, 720),
]
