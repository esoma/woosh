
# this file was generated using test/python/sample/generate.py

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
    with open(SAMPLE_DIR / 'stdlib/this.py', 'rb') as f:
        tokens = tokenize(f.read())
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.NAME, 's', 1, 0, 1, 1),
woosh.Token(woosh.OP, '=', 1, 2, 1, 3),
woosh.Token(woosh.STRING, '"""Gur Mra bs Clguba, ol Gvz Crgref\r\n\r\nOrnhgvshy vf orggre guna htyl.\r\nRkcyvpvg vf orggre guna vzcyvpvg.\r\nFvzcyr vf orggre guna pbzcyrk.\r\nPbzcyrk vf orggre guna pbzcyvpngrq.\r\nSyng vf orggre guna arfgrq.\r\nFcnefr vf orggre guna qrafr.\r\nErnqnovyvgl pbhagf.\r\nFcrpvny pnfrf nera\'g fcrpvny rabhtu gb oernx gur ehyrf.\r\nNygubhtu cenpgvpnyvgl orngf chevgl.\r\nReebef fubhyq arire cnff fvyragyl.\r\nHayrff rkcyvpvgyl fvyraprq.\r\nVa gur snpr bs nzovthvgl, ershfr gur grzcgngvba gb thrff.\r\nGurer fubhyq or bar-- naq cersrenoyl bayl bar --boivbhf jnl gb qb vg.\r\nNygubhtu gung jnl znl abg or boivbhf ng svefg hayrff lbh\'er Qhgpu.\r\nAbj vf orggre guna arire.\r\nNygubhtu arire vf bsgra orggre guna *evtug* abj.\r\nVs gur vzcyrzragngvba vf uneq gb rkcynva, vg\'f n onq vqrn.\r\nVs gur vzcyrzragngvba vf rnfl gb rkcynva, vg znl or n tbbq vqrn.\r\nAnzrfcnprf ner bar ubaxvat terng vqrn -- yrg\'f qb zber bs gubfr!"""', 1, 4, 21, 67),
woosh.Token(woosh.NEWLINE, '\r\n', 21, 67, 22, 0),
woosh.Token(woosh.NAME, 'd', 23, 0, 23, 1),
woosh.Token(woosh.OP, '=', 23, 2, 23, 3),
woosh.Token(woosh.OP, '{', 23, 4, 23, 5),
woosh.Token(woosh.OP, '}', 23, 5, 23, 6),
woosh.Token(woosh.NEWLINE, '\r\n', 23, 6, 24, 0),
woosh.Token(woosh.NAME, 'for', 24, 0, 24, 3),
woosh.Token(woosh.NAME, 'c', 24, 4, 24, 5),
woosh.Token(woosh.NAME, 'in', 24, 6, 24, 8),
woosh.Token(woosh.OP, '(', 24, 9, 24, 10),
woosh.Token(woosh.NUMBER, '65', 24, 10, 24, 12),
woosh.Token(woosh.OP, ',', 24, 12, 24, 13),
woosh.Token(woosh.NUMBER, '97', 24, 14, 24, 16),
woosh.Token(woosh.OP, ')', 24, 16, 24, 17),
woosh.Token(woosh.OP, ':', 24, 17, 24, 18),
woosh.Token(woosh.NEWLINE, '\r\n', 24, 18, 25, 0),
woosh.Token(woosh.INDENT, '    ', 25, 0, 25, 4),
woosh.Token(woosh.NAME, 'for', 25, 4, 25, 7),
woosh.Token(woosh.NAME, 'i', 25, 8, 25, 9),
woosh.Token(woosh.NAME, 'in', 25, 10, 25, 12),
woosh.Token(woosh.NAME, 'range', 25, 13, 25, 18),
woosh.Token(woosh.OP, '(', 25, 18, 25, 19),
woosh.Token(woosh.NUMBER, '26', 25, 19, 25, 21),
woosh.Token(woosh.OP, ')', 25, 21, 25, 22),
woosh.Token(woosh.OP, ':', 25, 22, 25, 23),
woosh.Token(woosh.NEWLINE, '\r\n', 25, 23, 26, 0),
woosh.Token(woosh.INDENT, '        ', 26, 0, 26, 8),
woosh.Token(woosh.NAME, 'd', 26, 8, 26, 9),
woosh.Token(woosh.OP, '[', 26, 9, 26, 10),
woosh.Token(woosh.NAME, 'chr', 26, 10, 26, 13),
woosh.Token(woosh.OP, '(', 26, 13, 26, 14),
woosh.Token(woosh.NAME, 'i', 26, 14, 26, 15),
woosh.Token(woosh.OP, '+', 26, 15, 26, 16),
woosh.Token(woosh.NAME, 'c', 26, 16, 26, 17),
woosh.Token(woosh.OP, ')', 26, 17, 26, 18),
woosh.Token(woosh.OP, ']', 26, 18, 26, 19),
woosh.Token(woosh.OP, '=', 26, 20, 26, 21),
woosh.Token(woosh.NAME, 'chr', 26, 22, 26, 25),
woosh.Token(woosh.OP, '(', 26, 25, 26, 26),
woosh.Token(woosh.OP, '(', 26, 26, 26, 27),
woosh.Token(woosh.NAME, 'i', 26, 27, 26, 28),
woosh.Token(woosh.OP, '+', 26, 28, 26, 29),
woosh.Token(woosh.NUMBER, '13', 26, 29, 26, 31),
woosh.Token(woosh.OP, ')', 26, 31, 26, 32),
woosh.Token(woosh.OP, '%', 26, 33, 26, 34),
woosh.Token(woosh.NUMBER, '26', 26, 35, 26, 37),
woosh.Token(woosh.OP, '+', 26, 38, 26, 39),
woosh.Token(woosh.NAME, 'c', 26, 40, 26, 41),
woosh.Token(woosh.OP, ')', 26, 41, 26, 42),
woosh.Token(woosh.NEWLINE, '\r\n', 26, 42, 27, 0),
woosh.Token(woosh.DEDENT, '', 28, 0, 28, 0),
woosh.Token(woosh.DEDENT, '', 28, 0, 28, 0),
woosh.Token(woosh.NAME, 'print', 28, 0, 28, 5),
woosh.Token(woosh.OP, '(', 28, 5, 28, 6),
woosh.Token(woosh.STRING, '""', 28, 6, 28, 8),
woosh.Token(woosh.OP, '.', 28, 8, 28, 9),
woosh.Token(woosh.NAME, 'join', 28, 9, 28, 13),
woosh.Token(woosh.OP, '(', 28, 13, 28, 14),
woosh.Token(woosh.OP, '[', 28, 14, 28, 15),
woosh.Token(woosh.NAME, 'd', 28, 15, 28, 16),
woosh.Token(woosh.OP, '.', 28, 16, 28, 17),
woosh.Token(woosh.NAME, 'get', 28, 17, 28, 20),
woosh.Token(woosh.OP, '(', 28, 20, 28, 21),
woosh.Token(woosh.NAME, 'c', 28, 21, 28, 22),
woosh.Token(woosh.OP, ',', 28, 22, 28, 23),
woosh.Token(woosh.NAME, 'c', 28, 24, 28, 25),
woosh.Token(woosh.OP, ')', 28, 25, 28, 26),
woosh.Token(woosh.NAME, 'for', 28, 27, 28, 30),
woosh.Token(woosh.NAME, 'c', 28, 31, 28, 32),
woosh.Token(woosh.NAME, 'in', 28, 33, 28, 35),
woosh.Token(woosh.NAME, 's', 28, 36, 28, 37),
woosh.Token(woosh.OP, ']', 28, 37, 28, 38),
woosh.Token(woosh.OP, ')', 28, 38, 28, 39),
woosh.Token(woosh.OP, ')', 28, 39, 28, 40),
woosh.Token(woosh.NEWLINE, '\r\n', 28, 40, 29, 0),
woosh.Token(woosh.EOF, '', 29, 0, 29, 0),
]
