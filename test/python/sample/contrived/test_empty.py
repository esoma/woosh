
# python
import pathlib
# woosh
import woosh

SAMPLE_DIR = pathlib.Path(__file__).parent.absolute() / '../../' / '../../' / 'sample'
def test():
    with open(SAMPLE_DIR / 'contrived/empty.py', 'rb') as f:
        tokens = list(woosh.tokenize(f))
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.NEWLINE, '', 1, 0, 1, 0),
woosh.Token(woosh.EOF, '', 1, 0, 1, 0),
]
